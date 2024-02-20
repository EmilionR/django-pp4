from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from .models import Post, Comment, Like
from crispy_forms.helper import FormHelper
from .forms import PostForm, CommentForm, EditPostForm
from django.contrib import messages
from django.utils.text import slugify
from django.urls import reverse_lazy, resolve
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator

# Create your views here.

class PostList(generic.ListView):

    """
    Display a list of all posts and a posting form
    """

    template_name = "board/index.html"

    # The posts to display (all posts if no search term is provided)
    def get_queryset(self):
        # https://docs.djangoproject.com/en/5.0/topics/db/queries/#complex-lookups-with-q-objects
        queryset = Post.objects.annotate(comment_count=Count('comments'))\
                             .order_by("-is_sticky", "-posted_on")
        # Check if the user is searching for something
        search_term = self.request.GET.get('search', '')
        if search_term:
            queryset = queryset.filter(
                # Check if one of the fields contains the search term
                Q(title__icontains=search_term) |
                Q(body__icontains=search_term)                
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_form = PostForm()
        post_form.helper = FormHelper()
        context['post_form'] = post_form
        return context
    
    def post(self, request, *args, **kwargs):
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            messages.success(request, 'Thread posted successfully.')
            return redirect('home')
        else:
            messages.error(request, 'There was an error with your post. Please try again.')
            return redirect('home')


def post_detail(request, slug):
    """
    Display an individual post thread
    """
    # Retrieve all posts
    queryset = Post.objects.all()
    post = get_object_or_404(queryset, slug=slug)
    # Format the date time to exclude seconds and microseconds
    post.posted_on = post.posted_on.strftime("%b %d, %Y %H:%M")
    post.updated_on = post.updated_on.strftime("%b %d, %Y %H:%M")
    # Check if the user likes the post
    liked_post = False  # Initialize as false to avoid errors
    if request.user.is_authenticated:  # Check if the user is logged in to avoid errors
        liked_post = Like.objects.filter(user=request.user, post=post).exists()

    # Retrieve all comments
    comments = post.comments.all().order_by("-is_sticky", "posted_on")
    comment_count = post.comments.all().count()
    # Comments that are liked by the current user
    liked_comments = []

    if request.user.is_authenticated:
        for comment in comments:
            # Format the date time to exclude seconds and microseconds
            comment.posted_on = comment.posted_on.strftime("%b %d, %Y %H:%M")
            comment.updated_on = comment.updated_on.strftime("%b %d, %Y %H:%M")
            comment.liked_by_user = Like.objects.filter(user=request.user, comment=comment).exists()

    comment_form = CommentForm()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment posted successfully'
            )
            return redirect(comment.post.get_absolute_url())

    return render(
        request,
        "board/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
            "liked_post": liked_post,
            "liked_comments": liked_comments,
         },
    )


class EditMixin(UserPassesTestMixin):
    """
    Checks if the user is allowed to edit
    """
    template_name = 'board/editing.html'

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author or self.request.user.is_staff
        
    def get_success_url(self):
        if self.model == Comment:
            # Commens get the slug from the related Post
            return reverse_lazy('post_detail', kwargs={'slug': self.get_object().post.slug})
        else:
            # Posts get their own slug
            return reverse_lazy('post_detail', kwargs={'slug': self.get_object().slug})


class EditPost(EditMixin, UpdateView):
    model = Post
    form_class = EditPostForm #  Using this form from forms.py
    

class EditComment(EditMixin, UpdateView):
    model = Comment
    form_class = CommentForm # Using this form from forms.py

        

@login_required
def post_delete(request, entry_type, entry_id):
    """
    Delete a post or comment, depending on the entry_type
    then redirect to the post's detail page
    """
    EntryType = Comment if entry_type == "comment" else Post
    entry = get_object_or_404(EntryType, id=entry_id)
    
    #  Decide where to redirect after deletion
    redirect_url = entry.post.get_absolute_url() if entry_type == "comment" else reverse('home')

    if request.user != entry.author and not request.user.is_staff:
        messages.error(request, "You can not delete another user's post.")
        return redirect(redirect_url)  # Redirect if the user doesn't have permission
    if request.method == "POST":
        entry.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect(redirect_url)
    

class LikeMixin(View):
    """
    Like function refactored into a mixin to allow likes on different models
    without repeating code
    """
    model = None  # Will be set to the model being liked


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        object_id = kwargs.get('object_id')
        user = request.user
        try:
            content_object = self.model.objects.get(id=object_id)
        except self.model.DoesNotExist:
            return JsonResponse({'error': 'Content not found'}, status=404)
        # Check if it's a post or comment
        if self.model == Post:
            like = Like.objects.filter(user=user, post=content_object).first()
        else:
            like = Like.objects.filter(user=user, comment=content_object).first()
        # Check if the user has already liked the object, then like or unlike
        if like:
            like.delete()
            liked = False
            content_object.likes -= 1
        else:
            if self.model == Post:
                like = Like.objects.filter(user=user, post=content_object).first()
                Like.objects.create(user=user, post=content_object)
            else:
                like = Like.objects.filter(user=user, comment=content_object).first()
                Like.objects.create(user=user, comment=content_object)
            liked = True
            content_object.likes += 1
        content_object.save()
        return JsonResponse({'liked': liked, 'new_likes': content_object.likes})


class LikePost(LikeMixin):
    model = Post


class LikeComment(LikeMixin):
    model = Comment