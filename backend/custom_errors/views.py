from django.shortcuts import render


def custom_bad_request_view(request, exception=None):
    context = {
        'title': 'Error 400',
        'error_number': '400',
        'error_title': 'Bad Request',
        'error_description': 'The requested URL was not found on this server!',
    }
    response = render(request, 'errors/error_page.html', context,)
    response.status_code = 400
    return response


def custom_permission_denied_view(request, exception=None):
    context = {
        'title': 'Error 403',
        'error_number': '403',
        'error_title': 'Forbidden',
        'error_description': 'Access to this resource on the server is denied!',
    }
    response = render(request, 'errors/error_page.html', context,)
    response.status_code = 403
    return response


def custom_page_not_found_view(request, exception=None):
    context = {
        'title': 'Error 404',
        'error_number': '404',
        'error_title': 'Not Found',
        'error_description': 'The requested resource was not found on this server!',
    }
    response = render(request, 'errors/error_page.html', context,)
    response.status_code = 404
    return response


def custom_error_view(request, exception=None):
    context = {
        'title': 'Error 500',
        'error_number': '500',
        'error_title': 'Internal Server Error',
        'error_description': 'An internal server error has occurred!',
    }
    response = render(request, 'errors/error_page.html', context,)
    response.status_code = 500
    return response