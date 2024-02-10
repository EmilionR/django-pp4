from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from django.contrib import messages
from django.shortcuts import redirect
import cloudinary.uploader


@login_required
def profile(request, username):
    """
    A view to display a user's profile, and update it if the user is logged in    
    """
    
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
             # Check if an image file is included in the request
            if 'avatar' in request.FILES:
                # Upload the image to Cloudinary
                result = cloudinary.uploader.upload(request.FILES['avatar'])
                # Update the image URL in the form's cleaned data
                profile_form.cleaned_data['avatar'] = result['url']
            profile_form.save()
            messages.add_message(request, messages.SUCCESS, "Profile updated successfully")
            return redirect('profile', username=username)
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'profile': profile, 'profile_form': profile_form})