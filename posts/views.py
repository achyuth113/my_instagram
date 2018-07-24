from __future__ import absolute_import
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from django.views.generic import ListView,DetailView
from .models import posts, like,comment
from users.models import profile,following
from .forms import CreatePostForm, UpdatePostForm
from django.db.models import Q
from django.shortcuts import *

class NewsFeed(LoginRequiredMixin,ListView):
    login_url = '/users/login/'
    model = posts
    context_object_name = 'feeds'
    template_name = 'posts/feeds.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = list(item['following_id_id'] for item in following.objects.values('following_id_id').filter(user_id=self.request.user))
        follower_ids= list(item['user_id_id'] for item in profile.objects.values('user_id_id').filter(Q(id__in=profile_id)))
        feeds = posts.objects.filter(Q(user_id_id__in=follower_ids) | Q(user_id=self.request.user)).order_by(
            '-update_date')
        feedData = []

        for feed in feeds:
            likes_count = like.objects.filter(post_id=feed).count()
            comments=comment.objects.all().filter(post_id=feed)[:2]
            feedData.append({'feed': feed, 'likesCount': likes_count,'comment':comments})

        liked_posts = like.objects.filter(user_id=self.request.user).values_list('post_id')
        liked_posts = [value[0] for value in liked_posts]

        context.update({
            'username': str(self.request.user),
            'liked_posts': liked_posts,
            'feedsData': feedData,
        })
        return context

class DetailPostView(LoginRequiredMixin,DetailView):
    login_url = '/users/login/'
    context_object_name = 'userform'
    def get(self, request, *args, **kwargs):
        postform=dict()
        post = posts.objects.all().filter(id=kwargs['slug'])[0]
        userform = User.objects.values('id', 'first_name', 'username', 'email').filter(username=kwargs['username'])[0]
        profileform = profile.objects.all().filter(user_id=userform['id'])[0]
        likes_count = like.objects.all().filter(post_id=post).count()
        hasLiked=like.objects.all().filter(post_id=post, user_id=request.user).count()
        total_comments = comment.objects.all().filter(post_id=post)
        postform['post']=post
        postform['userform']=userform
        postform['profileform']=profileform
        postform['likes_count']=likes_count
        postform['comments']=total_comments
        postform['profileform']=profileform
        postform['hasLiked']=hasLiked
        return render(request, template_name='posts/post_detail.html',
                      context={'postform': postform, 'username': str(request.user),})


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/users/login/'
    template_name = 'posts/post_form.html'
    def get(self, request,*args,**kwargs):
        form = CreatePostForm()
        return render(request, self.template_name, {'postform': form,'username':request.user})
    def post(self, request,*args,**kwargs):
        form = CreatePostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user_id=request.user
            post.save()
        return redirect('users:profile',request.user)



class EditPost(LoginRequiredMixin, UpdateView):
    login_url = '/users/login/'
    model=posts
    template_name = 'posts/post_form.html'
    def get(self, request, *args, **kwargs):
        post=posts.objects.get(id=kwargs['pk'])
        print(post.user_id.id)
        if post.user_id.id == request.user.id:
            form = UpdatePostForm(instance=post)
            return render(request, self.template_name, {'postform': form, 'username': str(request.user)})
        else:
            return redirect('users:profile', request.user)
    def post(self, request, *args, **kwargs):
        instance = posts.objects.get(id=kwargs['pk'])
        form = UpdatePostForm(request.POST, instance=instance)
        if form.is_valid():
            if instance.user_id.id==request.user.id:
                form.save()
            return redirect("users:profile", request.user)
        return redirect('users:profile', request.user)

class DeletePost(LoginRequiredMixin, DeleteView):
    login_url = '/users/login/'
    model = posts
    def get(self, request, *args, **kwargs):
        post = posts.objects.get(id=kwargs['pk'])
        print(post.user_id.id)
        if post.user_id.id == request.user.id:
            post.delete()
            return redirect('users:profile', request.user)
        else:
            return redirect('users:profile', request.user)



@login_required(login_url='/users/login/')
def LikesList(request, **kwargs):
    post = posts.objects.get(id=kwargs['pk'])
    list_of_users = list(item['user_id'] for item in list(like.objects.values('user_id').filter(post_id=post)))
    userform = list(User.objects.values('id', 'first_name', 'username', 'email').all().filter(id__in=list_of_users))
    for element in userform:
        element['profile'] = profile.objects.all().filter(user_id=element['id'])[0]
        element['followers'] = following.objects.all().filter(following_id=element['profile']).count()
        element['following'] = following.objects.all().filter(user_id=element['id']).count()
        element['is_followed'] = following.objects.all().filter(user_id=request.user,
                                                                following_id=element['profile']).count()
    args = {
        'title':"liked people",'userform': userform, 'username': str(request.user)
    }
    return render(request, 'accounts/account_list.html', args)



@csrf_exempt
def addComment(request,**kwargs):
    if request.method == "POST":
        post = posts.objects.get(id=kwargs['pk'])
        comments = comment.objects.create(
            post_id=post,
            comment=request.POST["comment"],
            user_id=request.user
        )
    response = str(request.user.username)+":"+request.POST["comment"]
    return HttpResponse(response)


class LikesToggle(View):
    def get(self,*args,**kwargs):
        post = posts.objects.get(id=self.kwargs.get('post_id'))
        user = self.request.user
        like_obj = like.objects.filter(user_id=user,post_id=post)
        response = 0
        if like_obj.count():
            like_obj.delete()
        else:
            like.objects.create(user_id=user,post_id=post)
            response = 1
        likes_count = like.objects.filter(post_id=post).count()
        response = str(response)+","+str(likes_count)
        return HttpResponse(response)
