from .models import Profile
from django import forms
from django_summernote.widgets import SummernoteWidget
from django.core.exceptions import ValidationError
import cloudinary.api


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('avatar', 'about',)  # Fields that can be updated
        widgets = {
            #  Accept only image files
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}),
            'about': SummernoteWidget(attrs={"class": "form-control"}),
        }

    #  Validate file size
    def clean_avatar(self):
        file = self.cleaned_data.get('avatar')
        if file:
            # Assuming 'file' is a CloudinaryResource object
            resource = cloudinary.api.resource(file.public_id)
            max_size =  524288  #  0.5 MB in bytes
            if resource['bytes'] > max_size:
                raise ValidationError(f'File size must be less than {max_size /  1024 /  1024} MB.')
        return file
