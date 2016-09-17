from django.contrib.auth import login
from django.http import HttpResponse
from fitapp.models import UserFitbit


def cors_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)
        response['Access-Control-Allow-Origin'] = "*"

        return response

    return middleware


def authorization_middleware(get_response):
    def middleware(request):
        if request.META.get('HTTP_AUTHORIZATION', False):
            try:
                print('wut wuth')
                login(request, UserFitbit.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split(" ")[1]).user)
            except UserFitbit.DoesNotExist:
                return HttpResponse(status=403)

        response = get_response(request)

        return response
    return middleware
