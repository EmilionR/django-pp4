from .models import Post, Comment
from django import forms
from django_summernote.widgets import SummernoteWidget

# https://github.com/summernote/django-summernote?tab=readme-ov-file#form

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'body',) #  Fields that user can write to
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control",}),
            'body': SummernoteWidget(attrs={"class": "form-control",}),
        }


class EditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('body',) #  Fields that user can write to
        widgets = {
            'body': SummernoteWidget(attrs={"class": "form-control"}),
        }


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('body',) #  Fields that user can write to
        widgets = {
            'body': SummernoteWidget(attrs={"class": "form-control"}),
        }