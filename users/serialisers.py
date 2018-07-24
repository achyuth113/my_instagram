from .models import *
from rest_framework import serializers


class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ProfileSerialisers(serializers.ModelSerializer):
    user_id = UserSerialiser()

    @staticmethod
    def setup_eager_loading(queryset):
        queryset.select_related('user_id')
        return queryset

    class Meta:
        model = profile
        fields = ('avatar', 'user_id')
