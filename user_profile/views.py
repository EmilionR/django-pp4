from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from django.contrib import messages
from django.shortcuts import redirect


@login_required
def profile(request, username):
    
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.add_message(request, messages.SUCCESS, "Profile updated successfully")
            return redirect('profile', username=username)
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'profile': profile, 'profile_form': profile_form})
