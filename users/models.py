from django.db import models
from django.contrib.auth.models import User

class profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars",default="no_profile_pic.png", blank=True)
    bio = models.TextField(max_length=500, blank=True)
    website = models.TextField(max_length=500, blank=True)
    create_data = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user_id.username

class followers(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    follower_id = models.ForeignKey(profile, on_delete=models.CASCADE)
    create_data = models.DateTimeField(auto_now_add=True)

class following(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    following_id = models.ForeignKey(profile, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)

