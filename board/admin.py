from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    fields = ('title', 'slug', 'author', 'body', 'is_sticky')
    list_display = ('title', 'slug', 'author', 'posted_on')
    search_fields = ['title', 'body']
    list_filter = ['posted_on', 'author']
    summernote_fields = ('body',)
    prepopulated_fields = {'slug': ('title',)}


# Register your models here.
admin.site.register(Comment)