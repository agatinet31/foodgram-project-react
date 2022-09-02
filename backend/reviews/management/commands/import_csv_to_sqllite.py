import csv
import os
import sqlite3

from django.core.management import BaseCommand

EMPTY_ARGS_MESSAGE = '"--{arg}" argument was not provided'


class Command(BaseCommand):
    """
    Команда для импорта данных из csv-файла в таблицу базы данных.
    Имя файла обязательно должно совпадать с именем таблицы
    (без имени приложения в названии). Имеет два обязатлеьных параметра:
    --path - полный путь до csv-файла
    --app - имя приложения

    Пример вызова:
    python manage.py import_csv_to_sqllite `
    --path '/f/Dev/GroupProject/test_data/genre.csv' --app 'reviews'

    При таком вызове произойдет запись данных в таблицу reviews_genre.
    """
    help = 'Load data from a csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        parser.add_argument('--app', type=str)

    def handle(self, *args, **kwargs):
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        path = kwargs.get('path')
        if not path:
            raise KeyError(EMPTY_ARGS_MESSAGE.format(arg='path'))
        app = kwargs.get('app')
        if not app:
            raise KeyError(EMPTY_ARGS_MESSAGE.format(arg='app'))
        # Формирование имени таблицы из имени файла и имени приложения
        file_name = os.path.basename(path)
        table = f'{app}_{os.path.splitext(file_name)[0]}'
        with open(path, 'rt', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Формирование строки для вставки вида:
            # "INSERT INTO t (col1, col2) VALUES (?, ?);"
            # где t - имя таблицы, (col1, col2) - имена столбцов,
            # (?, ?) - подстановка для записи значений,
            # количество знаков ? соответствует количеству столбцов
            for row in reader:
                headers = row
                values = f"({', '.join(['?']*len(row))})"
                break
            rows = f"({', '.join(headers)})"
            insert_command = f"INSERT INTO {table} {rows} VALUES{values}"
            cursor.executemany(insert_command, reader)
        connection.commit()
        connection.close()
