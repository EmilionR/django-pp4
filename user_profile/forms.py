from .models import Profile
from django import forms


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('avatar', 'about',)  # Fields that can be updated
        widgets = {
            #  Accept only image files
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}),
            'about': forms.Textarea(attrs={'rows': 5}),
        }
