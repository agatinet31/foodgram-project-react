from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .settings import (CATEGORY__BASENAME, CATEGORY_URL_PREFIX,
                       COMMENTS__BASENAME, COMMENTS_URL_PREFIX,
                       GENRE__BASENAME, GENRE_URL_PREFIX, REVIEW__BASENAME,
                       REVIEW_URL_PREFIX, TITLE__BASENAME, TITLE_URL_PREFIX,
                       USERS_BASENAME, USERS_URL_PREFIX, VERSION_API_V1)
from .token import CustomTokenView

app_name = 'api'

router = DefaultRouter()

urlpatterns = [
    path(
        f'{VERSION_API_V1}/',
        include(router.urls)
    ),   
    path(
        f'{VERSION_API_V1}/auth/token/',
        CustomTokenView.as_view(),
        name='get_user_jwt_token'
    ),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.authtoken')),
]
