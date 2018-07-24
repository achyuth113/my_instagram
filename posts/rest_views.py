from rest_framework import generics
from .serialisers import *


class LikesListApi(generics.ListCreateAPIView):
    serializer_class = LikesSerialisers

    def get_queryset(self):
        return like.objects.filter(user_id=self.request.user)
