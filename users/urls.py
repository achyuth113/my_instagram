from django.urls import path
from django.conf.urls import url
from .views import *
from .rest_views import *
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm
app_name = "users"

urlpatterns = [
    url(r'^signup/$', SignupView.as_view(), name='signup_form'),
    url(r'^login/$', LoginView.as_view(), name='login_form'),
    url(r'^(?P<username>[-\w]{1,50})/profile/$', DetailAccountView.as_view(), name='profile'),
    url(r'^logout/$', LogOutView.as_view(), name='logout_form'),
    url(r'^(?P<username>[-\w]{1,50})/users/$',ListAccountView.as_view(),name='user_list'),
    url(r'^(?P<username>[-\w]{1,50})/update/$',UpdateAccountView.as_view(),name='update'),
    url(r'^(?P<username>[-\w]{1,50})/update/password/$',change_password,name='change_password'),
    url(r'^(?P<username>[-\w]{1,50})/followers$',FollowersListView.as_view(),name='followers'),
    url(r'^(?P<username>[-\w]{1,50})/following/$',FollowingListView.as_view(),name='following'),
    url(r'^(?P<username>[-\w]{1,50})/follow/$',follow_view,name='follow'),
    url(r'^(?P<username>[-\w]{1,50})/unfollow/$',unfollow_view,name='unfollow'),
    path('users/api/<slug:slug>', SearchApi.as_view(), name="search_api"),
]

