from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('edit_comment/<int:pk>/', views.EditComment.as_view(), name='edit_comment'),
    path('edit_post/<int:pk>/', views.EditPost.as_view(), name='edit_post'),
    path('delete/<str:entry_type>/<int:entry_id>',
         views.post_delete, name='post_delete'),
]