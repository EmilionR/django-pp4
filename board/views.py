from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post
from .forms import CommentForm
from django.contrib import messages


# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.all().order_by("-is_sticky", "-posted_on")
    template_name = "board/index.html"

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