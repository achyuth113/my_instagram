from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic import ListView,DetailView
from django.shortcuts import *
from .models import profile, followers, following
from .forms import LoginForm, SignupForm, ProfileForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from posts.models import posts,like,comment
from django.db.models import Q



class SignupView(View):
    def get(self,request,*args,**kwargs):
        userform=SignupForm
        return render(request, template_name='accounts/signup_form.html', context={'userform':userform})
    def post ( self, request, *args, **kwargs ):
        form=SignupForm(request.POST)
        if form.is_valid():
            user=User.objects.create_user(**form.cleaned_data)
            user.save()
            profile_form=ProfileForm(data=None)
            profiles=profile_form.save(commit=False)
            profiles.user_id=user
            profiles.save()
        return redirect("users:login_form")

class LoginView(View):
    def get(self,request,*args,**kwargs):
        loginform=LoginForm
        return render(request, template_name='accounts/login_form.html', context={'loginform':loginform})
    def post ( self, request, *args, **kwargs ):
        form=LoginForm(request.POST)
        if form.is_valid ():
            user = authenticate ( username=form.cleaned_data['username'],
                                  password=form.cleaned_data['password'] )
            if user !=None:
                login(request,user)
                return redirect("posts:feed")
        return redirect("users:login_form")


class LogOutView(View):
    def get( self, request: object ) -> object:
        logout(request)
        return redirect("users:login_form")

class ListAccountView(LoginRequiredMixin,ListView):
    login_url = '/users/login/'
    context_object_name = 'userform'
    def get(self, request, *args, **kwargs):
        userform = list(User.objects.values('id','first_name','username','email').all().filter(username=kwargs['username']))
        userform = userform + list(User.objects.values('id','first_name','username','email').all().filter(is_superuser=0).filter(~Q(username=kwargs['username'])))
        for element in userform:
            element['profile']=profile.objects.all().filter(user_id=element['id'])[0]
            element['followers']=following.objects.all().filter(following_id=element['profile']).count()
            element['following'] = following.objects.all().filter(user_id=element['id']).count()
            element['is_followed']= following.objects.all().filter(user_id=request.user,following_id=element['profile']).count()
        return render(request, template_name='accounts/account_list.html',context={'userform':userform,'username':str(request.user),'title':"List of users"})


class DetailAccountView(LoginRequiredMixin,DetailView):
    login_url = '/users/login/'
    context_object_name = 'userform'
    def get(self, request, *args, **kwargs):
        userform = User.objects.values('id', 'first_name', 'username', 'email').filter(username=kwargs['username'])[0]
        profileform = profile.objects.all().filter(user_id=userform['id'])[0]
        followers_count = following.objects.all().filter(following_id=profileform).count()
        following_count = following.objects.filter(user_id=userform['id']).count()
        connected=following.objects.filter(user_id=request.user,following_id=profileform).count()
        total_posts = posts.objects.all().filter(user_id=userform['id'])
        userform['profile']=profileform
        userform['followers']=followers_count
        userform['following']=following_count
        userform['posts']=total_posts
        userform['post_count']=total_posts.count()
        return render(request, template_name='accounts/account_detail.html',
                      context={'userform': userform, 'username': str(request.user), 'connected': int(connected)})

class UpdateAccountView(LoginRequiredMixin,UpdateView):
    login_url = '/users/login/'
    model = profile
    template_name='accounts/add_user_profile.html'
    def get(self, request, *args, **kwargs):
        if request.user.username != kwargs['username']:
            return redirect("users:update", request.user)
        myprofile = profile.objects.get(user_id=request.user.id)
        form = ProfileForm(instance=myprofile)
        details=profile.objects.all().filter(user_id=request.user.id)[0]
        return render(request, self.template_name, {'profiledetails': details,'profileform': form,'username': str(request.user)})
    def post(self, request, *args, **kwargs):
        instance = profile.objects.get(user_id=request.user.id)
        form = ProfileForm(request.POST,request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("users:profile", request.user)
        return redirect('users:profile', request.user)


class FollowersListView(LoginRequiredMixin,ListView):
    login_url = '/users/login/'
    def get(self, request, *args, **kwargs):
        profile_id=profile.objects.all().filter(user_id__username=kwargs['username'])[0]
        list_of_users=list(item['user_id'] for item in list(following.objects.values('user_id').filter(following_id=profile_id)))
        userform = list(User.objects.values('id', 'first_name', 'username', 'email').filter(id__in=list_of_users))
        for element in userform:
            element['profile'] = profile.objects.all().filter(user_id_id=element['id'])[0]
            element['followers'] = following.objects.all().filter(following_id=element['profile']).count()
            element['following'] = following.objects.all().filter(user_id=element['id']).count()
            element['is_followed'] = following.objects.all().filter(user_id=request.user,
                                                                    following_id=element['profile']).count()
        return render(request, template_name='accounts/account_list.html',
                      context={'title':"List of followers", 'userform': userform, 'username': str(request.user)})


class FollowingListView(LoginRequiredMixin,ListView):
    login_url = '/users/login/'
    def get(self, request, *args, **kwargs):
        user_id = User.objects.all().filter(username=kwargs['username'])[0]
        list_of_users = list(
            item['following_id'] for item in list(following.objects.values('following_id').filter(user_id=user_id)))
        userform = list(User.objects.values('id', 'first_name', 'username', 'email').filter(profile__id__in=list_of_users))
        for element in userform:
            element['profile'] = profile.objects.all().filter(user_id_id=element['id'])[0]
            element['followers'] = following.objects.all().filter(following_id=element['profile']).count()
            element['following'] = following.objects.all().filter(user_id=element['id']).count()
            element['is_followed'] = 1
        return render(request, template_name='accounts/account_list.html',
                      context={'title':"List of following",'userform': userform, 'username': str(request.user)})


@login_required
def change_password(request, *args, **kwargs):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

@login_required
def follow_view(request, *args, **kwargs):
    try:
        follower = User.objects.get(username=request.user)
        temp = User.objects.get(username=kwargs['username'])
        followings = profile.objects.get(user_id=temp.id)
    except User.DoesNotExist:
        messages.warning(
            request,
            '{} is not a registered user.'.format(kwargs['username'])
        )
        return HttpResponseRedirect(reverse_lazy('home'))
    if str(follower) == str(following):
        messages.warning(
            request,
            'You cannot follow yourself.'
        )
    else:
        _, created = following.objects.get_or_create(
            user_id=follower,
            following_id=followings
        )
        if (created):
            messages.success(
                request,
                'You\'ve successfully followed {}.'.format(kwargs['username'])
            )
        else:
            messages.warning(
                request,
                'You\'ve already followed {}.'.format(kwargs['username'])
            )
    return HttpResponseRedirect(
        reverse_lazy(
            'users:profile',
            kwargs={'username': request.user}
        )
    )


@login_required
def unfollow_view(request, *args, **kwargs):
    try:
        follower = User.objects.get(username=request.user)
        temp = User.objects.get(username=kwargs['username'])
        followings = profile.objects.get(user_id=temp.id)
        if str(follower) == str(following):
            messages.warning(
                request,
                'You cannot unfollow yourself.'
            )
        else:
            status=following.objects.filter(user_id=follower,following_id=followings).delete()
            print(status)
            messages.success(
                request,
                'You\'ve just unfollowed {}.'.format(kwargs['username'])
            )
    except User.DoesNotExist:
        messages.warning(
            request,
            '{} is not a registered user.'.format(kwargs['username'])
        )
        return HttpResponseRedirect(reverse_lazy('users:profile',kwargs={'username': request.user}))
    except followers.DoesNotExist:
        messages.warning(
            request,
            'You didn\'t follow {0}.'.format(kwargs['username'])
        )
    return HttpResponseRedirect(
        reverse_lazy(
            'users:profile',
            kwargs={'username': request.user}
        )
    )

