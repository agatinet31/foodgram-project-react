import csv

from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser

EMPTY_ARGS_MESSAGE = '"--{arg}" argument was not provided'
UNKNOW_MODEL_MESSAGE = "Unknow model {model} was provided"


def import_categories(file_path):
    with open(file_path, 'r', encoding='utf-8') as records:
        reader = csv.reader(records)
        next(reader)
        objects = [
            Category(
                id=row[0], name=row[1], slug=row[2]
            ) for row in reader
        ]
        Category.objects.bulk_create(objects)


def import_genres(file_path):
    with open(file_path, 'r', encoding='utf-8') as records:
        reader = csv.reader(records)
        next(reader)
        objects = [
            Genre(
                id=row[0], name=row[1], slug=row[2]
            ) for row in reader
        ]
        Genre.objects.bulk_create(objects)


def import_comments(file_path):
    with open(file_path, 'r', encoding='utf-8') as records:
        reader = csv.reader(records)
        next(reader)
        objects = [
            Comment(
                id=row[0], review_id=row[1], text=row[2],
                author=CustomUser.objects.get(id=row[3]),
                pub_date=row[4]
            ) for row in reader
        ]
        Comment.objects.bulk_create(objects)


def import_users(file_path):
    with open(file_path, 'r', encoding='utf-8') as records:
        reader = csv.reader(records)
        next(reader)
        objects = [
            CustomUser(
                id=row[0], username=row[1], email=row[2], role=row[3],
                bio=row[4], first_name=row[5], last_name=row[6],
            ) for row in reader
        ]
        CustomUser.objects.bulk_create(objects)


def import_titles(file_path):
    with open(file_path, 'r', encoding='utf-8') as records:
        reader = csv.reader(records)
        next(reader)
        objects = [
            Title(
                id=row[0], name=row[1], year=row[2],
                category=Category.objects.get(id=row[3]),
            ) for row in reader
        ]
        Title.objects.bulk_create(objects)


def import_reviews(file_path):
    with open(file_path, 'r', encoding='utf-8') as records:
        reader = csv.reader(records)
        next(reader)
        objects = [
            Review(
                id=row[0], title_id=row[1], text=row[2],
                author=CustomUser.objects.get(id=row[3]),
                score=row[4], pub_date=row[5],
            ) for row in reader
        ]
        Review.objects.bulk_create(objects)


MODELS = {
    'Category': import_categories,
    'Comment': import_comments,
    'CustomUser': import_users,
    'Genre': import_genres,
    'Title': import_titles,
    'Review': import_reviews
}


class Command(BaseCommand):
    """
    Команда для импорта данных из csv-файла в записи моделей Django.
    Имеет два обязатлеьных параметра:
    --path - полный путь до csv-файла
    --model - имя модели, в которую импортируем данные
    ВАЖНО:
    Поскольку происходит импорт в модели Django важен порядок импорта,
    во избежание ошибок при создании записи на несуществующий объект.
    Порядок импорта моделей:
    1. Category,
    2. Genre,
    3. Users,
    4. Title,
    5. Review,
    6. Comment
    Пример вызова:
    python manage.py import_csv_to_django_model `
     --path '/f/Dev/GroupProject/test_data_1/titles.csv' --model Title
    При таком вызове произойдет запись данных в модель Title.
    """
    help = (
        'Load data from a csv file into Django model records. '
        'Model import order: 1. Category, 2. Genre, 3. Users, '
        '4. Title, 5. Genre_Title, 6. Review, 7. Comment'
    )

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        parser.add_argument('--model', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs.get('path')
        if not path:
            raise KeyError(EMPTY_ARGS_MESSAGE.format(arg='path'))
        model = kwargs.get('model')
        if not model:
            raise KeyError(EMPTY_ARGS_MESSAGE.format(arg='model'))

        importer = MODELS.get(model)
        if not importer:
            raise KeyError(UNKNOW_MODEL_MESSAGE.format(arg=model))
        importer(path)
