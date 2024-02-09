from .models import Profile
from django import forms

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('about',) #  Fields that user can write to
        widgets = {
            'about': forms.Textarea(attrs={'rows': 5})
        }