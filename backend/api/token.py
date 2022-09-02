from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers
from rest_framework_simplejwt import serializers as ser
from rest_framework_simplejwt import tokens, views

User = get_user_model()


def verify_credentials(username, confirmation_code):
    """Проверка кода подтверждения пользователя."""
    user = get_object_or_404(
        User,
        username=username
    )
    if not confirmation_code == user.confirmation_code:
        raise serializers.ValidationError('Неверный код')
    if user.confirmation_code:
        user.confirmation_code = 0
        user.save()
        return user
    return None


class CustomTokenObtainSerializer(ser.TokenObtainSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()
        del self.fields['password']

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'confirmation_code': attrs['confirmation_code'],
        }
        self.user = verify_credentials(**authenticate_kwargs)
        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        return {}


class CustomTokenObtainPairSerializer(CustomTokenObtainSerializer):
    """Генерирование токена."""
    @classmethod
    def get_token(cls, user):
        return tokens.RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['token'] = str(refresh.access_token)
        return data


class CustomTokenView(views.TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
