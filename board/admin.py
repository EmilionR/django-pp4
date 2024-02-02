from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    fields = ('title', 'slug', 'author', 'body')
    list_display = ('title', 'slug', 'author')
    exclude = ('posted_on', 'updated_on')
    search_fields = ['title']
    summernote_fields = ('body',)
    prepopulated_fields = {'slug': ('title',)}


# Register your models here.
admin.site.register(Comment)