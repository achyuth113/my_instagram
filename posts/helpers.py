from django.db.models import Prefetch

from .models import posts, like
from users.models import followers, profile
from django.contrib.auth.models import User


def get_posts(user=None, wall=False):
    if not user:
        return None

    if isinstance(user, str):
        user = User.objects.get(username=user)

    if not user.is_authenticated():
        return None

    users = [user, ]

    if wall:
        users += followers.objects \
                           .filter(follower__username=user) \
                           .values_list('following', flat=True)

    posts = posts.objects \
                .select_related('author') \
                .prefetch_related(
                    Prefetch(
                        'liked_post',
                        queryset=Like.objects.select_related('user'),
                        to_attr='liker'
                    )) \
                .filter(author__in=users) \
                .order_by('-date_created')

    for post in posts:
        post.liker = [liker.user for liker in post.liker]

    return posts


def get_post(slug=None):
    if not slug:
        return None

    post = Post.objects \
               .select_related('author') \
               .prefetch_related(
                   Prefetch(
                       'liked_post',
                       queryset=Like.objects.select_related('user'),
                       to_attr='liker'
                       )) \
               .get(slug=slug)

    post.liker = [liker.user for liker in post.liker]

    return post
