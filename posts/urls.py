from __future__ import absolute_import

from django.conf.urls import url
from django.urls import path

from .views import *
from .rest_views import *

urlpatterns = [
    url(r'feed/$', NewsFeed.as_view(), name='feed'),
    url(r'create/$',CreatePostView.as_view(),name='add_post'),
    url(r'(?P<username>[-\w]{1,100})/(?P<slug>\d+)/$',DetailPostView.as_view(),name='view'),
    url(r'(?P<pk>\d+)/edit/$',EditPost.as_view(), name="edit_post"),
    url(r'(?P<pk>\d+)/delete/$', DeletePost.as_view(), name="delete_post"),
    path('<int:pk>/likes', LikesList, name="post_likes"),
    path('<int:pk>/comment', addComment, name="post_add_comment"),
    path('likes/api/', LikesListApi.as_view(), name="user_likes_api"),
    path('like/<int:post_id>', LikesToggle.as_view(), name="like_toggle"),
]
