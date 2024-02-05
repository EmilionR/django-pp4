# your_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... other URL patterns ...
    path('profile/<username>/', views.profile, name='profile'),
]