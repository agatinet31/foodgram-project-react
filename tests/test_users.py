import pytest
from django.conf import settings


class TestUsersAPI:
    url_users = '/api/users/'
    url_me = '/api/users/me/'
    url_set_password = '/api/users/set_password/'
    url_login = '/api/auth/token/login/'
    url_logout = '/api/auth/token/logout/'

    def test_settings(self):
        assert hasattr(settings, 'REST_FRAMEWORK'), (
            'Проверьте, что добавили настройку '
            '`REST_FRAMEWORK` в файл `settings.py`'
        )

        assert 'DEFAULT_AUTHENTICATION_CLASSES' in settings.REST_FRAMEWORK, (
            'Проверьте, что добавили `DEFAULT_AUTHENTICATION_CLASSES` '
            'в `REST_FRAMEWORK` файла `settings.py`'
        )
        assert (
            'rest_framework.authentication.TokenAuthentication'
            in settings.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']
        ), (
            'Проверьте, что в списке значения `DEFAULT_AUTHENTICATION_CLASSES`'
            ' в `REST_FRAMEWORK` содержится '
            '`rest_framework.authentication.TokenAuthentication`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_list_users(self, client):
        url = self.url_users
        response = client.get(url)
        assert response.status_code != 404, (
            f'Страница `{url}` не найдена, '
            'проверьте этот адрес в *urls.py*'
        )
        code_expected = 200
        assert response.status_code == code_expected, (
            f'Страница `{url}` работает не правильно'
        )

    @pytest.mark.django_db(transaction=True)
    def test_create_user_valid_request(self, client):
        url = self.url_users
        valid_data = {
            'email': 'vpupkin@yandex.ru',
            'username': 'vasya.pupkin',
            'first_name': 'Вася',
            'last_name': 'Пупкин',
            'password': 'Qwerty123@$@Qwerty756'
        }
        response = client.post(url, data=valid_data)
        code_expected = 201
        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` с валидными данными, '
            f'возвращается код {code_expected}'
        )
        fields_in_response = (
            'email', 'username', 'first_name', 'last_name', 'id'
        )
        for field in fields_in_response:
            assert field in response.json().keys(), (
                f'Убедитесь, что при запросе `{url}` с валидными данными, '
                f' в ответе возвращается код {code_expected} с ключами '
                f'{fields_in_response}, где содержатся данные пользователя'
            )

    @pytest.mark.django_db(transaction=True)
    def test_create_user_bad_request(self, client):
        url = self.url_users
        response = client.post(url)
        code_expected = 400
        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` без параметров, '
            f'возвращается код {code_expected}'
        )
        fields_invalid = (
            'email', 'username', 'first_name', 'last_name', 'password'
        )
        assert response.data['error'] is not None, (
            f'Убедитесь, что при запросе `{url}` без параметров, '
            'возвращается детализация ошибке в `errors`'
        )
        error_detail = response.data['error']
        if error_detail:
            for field in fields_invalid:
                assert field in error_detail.keys(), (
                    f'Убедитесь, что при запросе `{url}` без параметров, '
                    f'возвращается код {code_expected} с сообщением о том, '
                    'при обработке каких полей возникла ошибка.'
                    f'Не найдено поле {field}'
                )

    @pytest.mark.django_db(transaction=True)
    def test_get_user_profile_user_authorized(self, user_client, user):
        url = f'{self.url_users}{user.pk}/'
        response = user_client.get(url)
        assert response.status_code != 404, (
            f'Страница `{url}` не найдена, '
            'проверьте этот адрес в *urls.py*'
        )
        code_expected = 200
        assert response.status_code == code_expected, (
            f'Страница `{url}` работает не правильно'
        )
        fields_in_response = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        for field in fields_in_response:
            assert field in response.json().keys(), (
                f'Убедитесь, что при запросе `{url}` с валидными данными, '
                f' в ответе возвращается код {code_expected} с ключами '
                f'{fields_in_response}, где содержатся данные пользователя'
            )

    @pytest.mark.django_db(transaction=True)
    def test_get_user_profile_user_not_authorized(self, client, user):
        url = f'{self.url_users}{user.pk}/'
        response = client.get(url)
        code_expected = 401
        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` '
            'без предоставления учетных данных, '
            f'возвращается код {code_expected}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_get_user_me_authorized(self, user_client, user):
        url = self.url_me
        response = user_client.get(url)
        assert response.status_code != 404, (
            f'Страница `{url}` не найдена, '
            'проверьте этот адрес в *urls.py*'
        )
        code_expected = 200
        assert response.status_code == code_expected, (
            f'Страница `{url}` работает не правильно'
        )
        fields_in_response = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        for field in fields_in_response:
            assert field in response.json().keys(), (
                f'Убедитесь, что при запросе `{url}` с валидными данными, '
                f' в ответе возвращается код {code_expected} с ключами '
                f'{fields_in_response}, где содержатся данные пользователя'
            )

    @pytest.mark.django_db(transaction=True)
    def test_get_user_me_not_authorized(self, client, user):
        url = self.url_me
        response = client.get(url)
        code_expected = 401
        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` '
            'без предоставления учетных данных, '
            f'возвращается код {code_expected}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_set_user_password_valid_request(self, user_client):
        url = self.url_set_password
        valid_data = {
            'new_password': 'Qwerty123@$@Qwerty756',
            'current_password': '1234567'
        }
        response = user_client.post(url, data=valid_data)
        code_expected = 204
        print(response.data)
        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` с валидными данными, '
            f'возвращается код {code_expected}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_set_user_password_not_authorized(self, client):
        url = self.url_set_password
        response = client.get(url)
        code_expected = 401
        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` '
            'без предоставления учетных данных, '
            f'возвращается код {code_expected}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_set_user_password_bad_request(self, user_client):
        url = self.url_set_password
        response = user_client.post(url)
        code_expected = 400
        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` без параметров, '
            f'возвращается код {code_expected}'
        )
        fields_invalid = ('new_password', 'current_password',)
        assert response.data['error'] is not None, (
            f'Убедитесь, что при запросе `{url}` без параметров, '
            'возвращается детализация ошибке в `errors`'
        )
        error_detail = response.data['error']
        if error_detail:
            for field in fields_invalid:
                assert field in error_detail.keys(), (
                    f'Убедитесь, что при запросе `{url}` без параметров, '
                    f'возвращается код {code_expected} с сообщением о том, '
                    'при обработке каких полей возникла ошибка.'
                    f'Не найдено поле {field}'
                )

    @pytest.mark.django_db(transaction=True)
    def test_login(self, client, user):
        url = self.url_login
        response = client.post(
            url,
            data={'email': user.email, 'password': '1234567'}
        )
        assert response.status_code != 404, (
            f'Страница `{url}` не найдена, '
            'проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            f'Страница `{url}` работает не правильно'
        )
        auth_data = response.json()
        assert 'auth_token' in auth_data, (
            'Проверьте, что при POST запросе `/api/auth/token/login/` '
            'возвращаете токен'
        )

    @pytest.mark.django_db(transaction=True)
    def test_not_login(self, client, user):
        url = self.url_login
        response = client.post(
            url,
            data={'email': user.email, 'password': 'incorrect'}
        )
        assert response.status_code == 400, (
            f'Страница `{url}` работает не правильно'
        )

    @pytest.mark.django_db(transaction=True)
    def test_logout(self, user_client):
        url = self.url_logout
        response = user_client.post(url)
        assert response.status_code == 204, (
            f'Страница `{url}` работает не правильно'
        )

    @pytest.mark.django_db(transaction=True)
    def test_not_logout(self, client):
        url = self.url_logout
        response = client.post(url)
        assert response.status_code == 401, (
            f'Страница `{url}` работает не правильно'
        )
