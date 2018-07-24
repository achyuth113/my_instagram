from .models import *
from rest_framework import serializers


class LikesSerialisers(serializers.ModelSerializer):
    class Meta:
        model = like
        fields = ['post_id_id']

