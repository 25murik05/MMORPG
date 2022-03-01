from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('post/', PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('my_posts/<int:pk>/', MyPostDetail.as_view(), name='my_post_detail'),
    path('logout/',
         LogoutView.as_view(template_name='logout.html'),
         name='logout'),
    path('profile/', ProfileView.as_view()),
    path('my_posts/', my_post, name='my_post_list'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('my_posts/<int:post_pk>/comments', CommentsMyList.as_view(), name='my_comments_list'),
    path('post/<int:post_pk>/comments', CommentsList.as_view(), name='comments_list'),
    path('post/<int:post_pk>/create_comment', CommentCreate.as_view(), name='comment_create'),
    path('my_post/<int:post_pk>/comments/<int:comment_pk>/accept', CommentAccept.as_view(), name='comment_accept'),
    path('my_post/<int:post_pk>/comments/<int:comment_pk>/reject', CommentReject.as_view(), name='comment_reject'),
    path('comments/<int:comment_pk>/delete', CommentDelete.as_view(), name='comment_delete'),
]
