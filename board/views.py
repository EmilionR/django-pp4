from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Comment

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

    comments = post.comments.all().order_by("posted_on")
    comment_count = post.comments.all().count()


    return render(
        request,
        "board/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
         },
    )