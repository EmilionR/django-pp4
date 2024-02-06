from .models import Post, Comment
from django import forms


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'body',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'body': forms.Textarea(attrs={'placeholder': 'Your content here...'}),
        }


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Your comment here...'}),
        }