from django.urls import include, path
from django.views.generic import TemplateView
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from api.views import (FavoriteViewSet, IngredientViewSet, ShoppingCartViewSet,
                       SubscribeViewSet, TagViewSet, UserListViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(
    'tags', TagViewSet, basename='tags'
)
router.register(
    'ingredients', IngredientViewSet, basename='ingredients'
)

user_urlpatterns = [
    path(
        'users/',
        UserListViewSet.as_view({'get': 'list', 'post': 'create'}),
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
        name='user-set-password'
    ),
    path(
        'users/subscriptions/',
        SubscribeViewSet.as_view({'get': 'list'}),
        name='subscriptions'
    ),
    path(
        'users/<int:id>/subscribe/',
        SubscribeViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='subscribe'
    ),
]

add_recipe_urlpatterns = [
    path(
        'recipes/<int:id>/favorite/',
        FavoriteViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='favorite'
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        ShoppingCartViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='shopping-cart-detail'
    ),
    path(
        'recipes/download_shopping_cart/',
        ShoppingCartViewSet.as_view({'get': 'download_shopping_cart'}),
        name='shopping-cart-download'
    ),
]

urlpatterns = [
    path(
        '', include(router.urls)
    ),
    path(
        '', include(add_recipe_urlpatterns)
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
