from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .settings import (CATEGORY__BASENAME, CATEGORY_URL_PREFIX,
                       COMMENTS__BASENAME, COMMENTS_URL_PREFIX,
                       GENRE__BASENAME, GENRE_URL_PREFIX, REVIEW__BASENAME,
                       REVIEW_URL_PREFIX, TITLE__BASENAME, TITLE_URL_PREFIX,
                       USERS_BASENAME, USERS_URL_PREFIX, VERSION_API_V1)
from .token import CustomTokenView
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet,
                    new_user_registration)

app_name = 'api'

router = DefaultRouter()

router.register(
    COMMENTS_URL_PREFIX,
    CommentViewSet,
    basename=COMMENTS__BASENAME
)

router.register(
    CATEGORY_URL_PREFIX,
    CategoryViewSet,
    basename=CATEGORY__BASENAME
)
router.register(
    GENRE_URL_PREFIX,
    GenreViewSet,
    basename=GENRE__BASENAME
)
router.register(
    REVIEW_URL_PREFIX,
    ReviewViewSet,
    basename=REVIEW__BASENAME
)
router.register(
    TITLE_URL_PREFIX,
    TitleViewSet,
    basename=TITLE__BASENAME
)
router.register(
    USERS_URL_PREFIX,
    UserViewSet,
    basename=USERS_BASENAME
)

urlpatterns = [
    path(
        f'{VERSION_API_V1}/',
        include(router.urls)
    ),
    path(
        f'{VERSION_API_V1}/auth/signup/',
        new_user_registration,
        name='new_user_registration'
    ),
    path(
        f'{VERSION_API_V1}/auth/token/',
        CustomTokenView.as_view(),
        name='get_user_jwt_token'
    ),
]
