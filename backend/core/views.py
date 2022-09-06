from django.shortcuts import render
from django.views import defaults

ERROR_400_TEMPLATE_NAME = 'core/400.html'
ERROR_403_TEMPLATE_NAME = 'core/403.html'
ERROR_403_CSRF_TEMPLATE_NAME = 'core/403csrf.html'
ERROR_404_TEMPLATE_NAME = 'core/404.html'
ERROR_500_TEMPLATE_NAME = 'core/500.html'


def bad_request(
    request, exception, template_name=ERROR_400_TEMPLATE_NAME
):
    "Рендер пользовательской страницы 400."""
    return defaults.bad_request(request, exception, template_name)


def permission_denied(
    request, exception, template_name=ERROR_403_TEMPLATE_NAME
):
    """Рендер пользовательской страницы 403."""
    return defaults.permission_denied(request, exception, template_name)


def page_not_found(
    request, exception, template_name=ERROR_404_TEMPLATE_NAME
):
    """Рендер пользовательской страницы 404."""
    return defaults.page_not_found(request, exception, template_name)


def server_error(
    request, template_name=ERROR_500_TEMPLATE_NAME
):
    """Рендер пользовательской страницы 500."""
    return defaults.server_error(request, template_name)


def csrf_failure(request, reason=''):
    """Рендер пользовательской страницы 403csrf."""
    return render(request, ERROR_403_CSRF_TEMPLATE_NAME)
