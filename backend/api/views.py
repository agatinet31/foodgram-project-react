import uuid

from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

#from api.filters import TitlesFilter
from api.permissions import AnyReadOnly, IsAdmin, UserAccountPermission
from api.settings import EMAIL_ADMIN, USER_ME
from api.viewsets import AdminOrReadOnlyViewSet, YamdbBaseViewSet
#from reviews.models import Category, Genre, Review, Title


User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def new_user_registration(request):
    """Регистрация нового пользователя."""
    pass


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet-класс для просмотра информации по пользователям."""
    pass
