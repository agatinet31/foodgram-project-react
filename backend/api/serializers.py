from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from api.settings import USER_ME
#from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser
