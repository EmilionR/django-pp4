from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Entry(models.Model):
    body = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    is_sticky = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Post(Entry):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="board_posts"
    )
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    latest_activity = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Set the latest_activity field to the current time if not set
        if not self.latest_activity:
            self.latest_activity = timezone.now()
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-posted_on"]

    def get_absolute_url(self):
        # Returns a URL to access a detail view of this post.
        return reverse("post_detail", args=[str(self.slug)])

    def __str__(self):
        return f"{self.title} by {self.author}"


class Comment(Entry):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="board_replies"
    )
    post = models.ForeignKey(
            Post, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        ordering = ["posted_on"]

    def __str__(self):
        return f"Comment {self.preview} by {self.author}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True,
        blank=True, related_name="like"
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=True,
        blank=True, related_name="like"
    )

    # Ensure that only one of the foreign keys is filled
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(post__isnull=False, comment__isnull=True)
                    | models.Q(post__isnull=True, comment__isnull=False)
                ),
                name="like_post_or_comment",
            )
        ]
