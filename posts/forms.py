from __future__ import absolute_import

from django import forms
from .models import *


class UpdatePostForm(forms.ModelForm):
    class Meta:
        fields = ('caption', )
        model = posts

class CreatePostForm(forms.ModelForm):
    class Meta:
        fields = ('file', 'caption', )
        model = posts

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model=comment
        fields=('comment',)