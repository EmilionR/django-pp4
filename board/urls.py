from . import views
from django.urls import path

urlpatterns = [
    # Post list (board) view
    path("", views.PostList.as_view(), name="home"),
    # Post detail (thread) view
    path("<slug:slug>/", views.post_detail, name="post_detail"),
    # Edit comment
    path("edit_comment/<int:pk>/",
         views.EditComment.as_view(), name="edit_comment"),
    # Edit post
    path("edit_post/<int:pk>/", views.EditPost.as_view(), name="edit_post"),
    # Delete post
    path(
        "delete/<str:entry_type>/<int:entry_id>",
        views.post_delete, name="post_delete"
    ),
    # Lke post / comment
    path("like_post/<int:object_id>/",
         views.LikePost.as_view(), name="like_post"),
    path(
        "like_comment/<int:object_id>/",
        views.LikeComment.as_view(),
        name="like_comment",
    ),
]
