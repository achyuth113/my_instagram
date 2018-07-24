from django.contrib.auth.models import User
from django.db import models


class posts(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/posts/', null=True, blank=True)
    caption = models.TextField(max_length=500, blank=True)
    create_data=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user_id

class comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(posts, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, blank=True)
    create_data = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.id

class like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(posts, on_delete=models.CASCADE)
    create_data = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.id

class posts_list(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(posts, on_delete=models.CASCADE)