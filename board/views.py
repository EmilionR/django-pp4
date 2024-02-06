from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post
from crispy_forms.helper import FormHelper
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.utils.text import slugify


# Create your views here.

class PostList(generic.ListView):
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

    queryset = Post.objects.all()
    post = get_object_or_404(queryset, slug=slug)

    comments = post.comments.all().order_by("-is_sticky", "posted_on")
    comment_count = post.comments.all().count()

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