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
        response['Access-Control-Allow-Methods'] = 'POST,PUT,GET,DELETE,HEAD,OPTION'
        response['Access-Control-Allow-Headers'] = "Authorization"
        return response

    return middleware


def authorization_middleware(get_response):
    def middleware(request):
        print(request.META.get('HTTP_AUTHORIZATION'))
        if request.META.get('HTTP_AUTHORIZATION', False):
            try:
                login(request, UserFitbit.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split(" ")[1]).user)
            except UserFitbit.DoesNotExist:
                return HttpResponse(status=403)

        response = get_response(request)

        return response
    return middleware
