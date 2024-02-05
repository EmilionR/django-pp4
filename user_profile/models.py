from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=500, default='No bio...')
    posts = models.ManyToManyField('board.Post', related_name='user_posts')
    comments = models.ManyToManyField('board.Comment', related_name='user_comments')

    def __str__(self):
        return f'{self.user.username} Profile'

class ProfileAdmin(admin.ModelAdmin):
    exclude = ('posts', 'comments')
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()