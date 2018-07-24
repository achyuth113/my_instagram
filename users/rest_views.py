from rest_framework import generics
from .serialisers import *
from django.contrib.auth.models import User

class SearchApi(generics.ListCreateAPIView):
    serializer_class = ProfileSerialisers
    def get_queryset(self):
        userid=list(item['id'] for item in list(User.objects.values('id').filter(username__icontains=self.kwargs['slug'])))
        queryset = profile.objects.filter(user_id__in=userid)
        queryset =self.get_serializer_class().setup_eager_loading(queryset=queryset)
        return queryset
