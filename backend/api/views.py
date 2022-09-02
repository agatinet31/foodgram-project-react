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

from api.filters import TitlesFilter
from api.permissions import AnyReadOnly, IsAdmin, UserAccountPermission
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleGetSerializer, TitlePostSerializer,
                             UserSerializer)
from api.settings import EMAIL_ADMIN, USER_ME
from api.viewsets import AdminOrReadOnlyViewSet, YamdbBaseViewSet
from reviews.models import Category, Genre, Review, Title
from users.settings import USER

User = get_user_model()


class GenreViewSet(AdminOrReadOnlyViewSet):
    """ViewSet-класс для просмотра информации по жанрам."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(AdminOrReadOnlyViewSet):
    """ViewSet-класс для просмотра информации по категориям."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(YamdbBaseViewSet):
    """ViewSet-класс для просмотра информации по произведениям."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter
    permission_classes = [AnyReadOnly | IsAdmin]

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitlePostSerializer
        return TitleGetSerializer


class ReviewViewSet(YamdbBaseViewSet):
    """ViewSet-класс для просмотра информации по отзывам."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer, **kwargs):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(YamdbBaseViewSet):
    """ViewSet-класс для просмотра информации по коментариям."""
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer, **kwargs):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def new_user_registration(request):
    """Регистрация нового пользователя."""
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    if not User.objects.filter(username=username, email=email).exists():
        user = User.objects.create_user(
            username=username,
            email=email
        )
    else:
        user = get_object_or_404(
            User,
            username=username,
            email=email
        )
    code = uuid.getnode()
    user.confirmation_code = code
    user.save()
    mail = EmailMessage(
        subject='Confirmation code',
        body=str(code),
        from_email=EMAIL_ADMIN,
        to=[email]
    )
    mail.send(fail_silently=True)
    return Response({'username': username, 'email': email})


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet-класс для просмотра информации по пользователям."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^username',)
    permission_classes = [UserAccountPermission]

    def get_object(self):
        username = self.kwargs.get('username')
        if username.upper() == USER_ME:
            return self.request.user
        return get_object_or_404(User, username=username)

    def perform_update(self, serializer):
        if self.request.user.role == USER:
            serializer.save(role=self.request.user.role)
        else:
            super().perform_update(serializer)
