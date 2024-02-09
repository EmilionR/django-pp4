from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from .models import Post, Comment
from crispy_forms.helper import FormHelper
from .forms import PostForm, CommentForm, EditPostForm
from django.contrib import messages
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# Create your views here.

class PostList(generic.ListView):

    """
    Display a list of all posts and a posting form
    """

    queryset = Post.objects.all().order_by("-is_sticky", "-posted_on")
    template_name = "board/index.html"
    
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

    comments = post.comments.all().order_by("-is_sticky", "posted_on")
    comment_count = post.comments.all().count()

    for comment in comments:
        # Format the date time to exclude seconds and microseconds
        comment.posted_on = comment.posted_on.strftime("%b %d, %Y %H:%M")
        comment.updated_on = comment.updated_on.strftime("%b %d, %Y %H:%M")

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