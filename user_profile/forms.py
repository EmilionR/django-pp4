from .models import Profile
from django import forms

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('avatar', 'about',) # Fields that can be updated
        widgets = {
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}), #  Accept only image files
            'about': forms.Textarea(attrs={'rows': 5}),
        }
