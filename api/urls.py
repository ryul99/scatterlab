from django.urls import path
from api import views

urlpatterns = [
    path('posts/', views.article),
    path('posts/<int:post_id>', views.specific_article),
    path('posts/<int:post_id>/comment', views.comment),
    path('posts/<int:post_id>/like', views.like_post),
    path('posts/<int:post_id>/hate', views.hate_post),
    path('comments/<int:comment_id>/like', views.like_comment),
    path('comments/<int:comment_id>/hate', views.hate_comment),
]