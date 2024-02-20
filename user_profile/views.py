from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from django.contrib import messages
from django.shortcuts import redirect
import cloudinary.uploader
from board.models import Post, Comment


@login_required
def profile(request, username):
    """
    A view to display a user's profile, and update it if the user is logged in    
    """
    # Fetch the user
    user = get_object_or_404(User, username=username)
    # Fetch the user's profile
    profile = get_object_or_404(Profile, user=user)
    # Fetch the the user's posts and comments
    posts = Post.objects.filter(author=user).order_by('-posted_on')
    comments = Comment.objects.filter(author=user).order_by('-posted_on')

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

    # Pass the posts to the template context
    context = {
        'profile': profile,
        'profile_form': profile_form,
        'posts': posts,  # Include the user's posts in the context
        'comments': comments,  # Include the user's comments in the context
    }

    return render(request, 'profile.html', context)


def delete_account(request):
    if request.method == 'POST':
        messages.success(request, "Account deleted successfully")
        request.user.delete()
        # Redirect to home page
        return redirect('home')
    else:
        # Render the confirmation template
        return render(request, 'confirm_delete.html')