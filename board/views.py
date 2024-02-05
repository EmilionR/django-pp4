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

    return render(
        request,
        "board/post_detail.html",
        {"post": post},
    )