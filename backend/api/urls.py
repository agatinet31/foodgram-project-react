from django.urls import include, path
from django.views.generic import TemplateView
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from api.views import TagViewSet, IngredientViewSet

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')

user_urlpatterns = [
    path(
        'users/',
        UserViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='users'
    ),
    path(
        'users/<int:id>/',
        UserViewSet.as_view({'get': 'retrieve'}),
        name='user-info'
    ),
    path(
        'users/me/',
        UserViewSet.as_view({'get': 'me'}),
        name='user-me'
    ),
    path(
        'users/set_password/',
        UserViewSet.as_view({'post': 'set-password'}),
        name='user_set_password'
    ),
]

urlpatterns = [
    path(
        '', include(router.urls)
    ),
    
    path(
        '', include(user_urlpatterns)
    ),
    path(
        'auth/', include('djoser.urls.authtoken')
    ),
    path(
        'docs/',
        TemplateView.as_view(template_name='api/redoc.html'),
        name='redoc'
    ),
]
