from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Entry(models.Model):
    body = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    preview = models.TextField(blank=True)

    class Meta:
        abstract = True


class Post(Entry):
    author = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name="board_posts"
    )
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    class Meta:
        ordering = ["-posted_on"]

    
    def __str__(self):
        return f"{self.title} by {self.author}"


class Comment(Entry):
    author = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name="board_replies"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )

    class Meta:
        ordering = ["posted_on"]

    def __str__(self):
        return f"Comment {self.preview} by {self.author}"
