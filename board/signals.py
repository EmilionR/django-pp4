from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Post, Comment

#https://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/

# Update the latest_activity field of a post when a new comment is added
@receiver(post_save, sender=Comment)
def update_latest_activity(sender, instance, created, **kwargs):
    # Check if the comment is new
    if created:
        instance.post.latest_activity = timezone.now()
        instance.post.save(update_fields=['latest_activity'])