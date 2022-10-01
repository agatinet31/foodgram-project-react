import os

from django.conf import settings


class TestRequirements:

    def test_requirements(self):
        try:
            with open(
                f'{os.path.join(settings.BASE_DIR, "requirements.txt")}', 'r'
            ) as f:
                requirements = f.read()
        except FileNotFoundError:
            assert False, 'Проверьте, что добавили файл requirements.txt'

        pip_package = (
            'django',
            'django_colorfield',
            'django-extra-fields',
            'django-filter',
            'djangorestframework',
            'djoser',
            'gunicorn',
            'Pillow',
            'pytest-django',
            'psycopg2-binary',
            'python-dotenv',
            'reportlab',
            'webcolors'
        )
        for package_name in pip_package:
            assert package_name in requirements, (
                f'Проверьте, что добавили {package_name} '
                'в файл requirements.txt'
            )
