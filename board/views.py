from django.shortcuts import render
from django.views import generic
from .models import Post, Comment

# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.all().order_by("-posted_on")
    template_name = "board.html"