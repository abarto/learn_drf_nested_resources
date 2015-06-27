from django.contrib.auth import get_user_model

from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()