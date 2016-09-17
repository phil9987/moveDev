import json
from time import gmtime, strftime

import datetime

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
from django.utils import timezone
from fitapp.models import UserFitbit
from moveDevServer.models import UserPooledTimestamp, Activity


def subscriber(request):
    print(request.body)
    for activity in json.loads(request.body):
        Activity.objects.create(
            owner_id=activity['ownerId'],
            collection_type=activity['collectionType'],
            activity_id=activity['subscriptionI']
        )

    return HttpResponse(status=204)


class Home(TemplateView):
    template_name = 'index.html'

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            pass
        return self.render_to_response({})


class Login(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Login, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(json.dumps({
                'access_token': user.userfitbit.access_token
            }), content_type="application/json")


class StepsView(View):
    def get(self, request):
        try:
            user = User.objects.get(id=request.GET['user_id'])
        except KeyError:
            return HttpResponse({'error': 'User id is required'}, content_type="application/json")

        now = timezone.now()
        url = 'https://api.fitbit.com/1/user/{}/activities/steps/date/today/1d.json'.format(
            user.userfitbit.fitbit_user
        )
        data = json.loads(requests.get(
            url,
            headers={
                'Authorization': "Bearer {}".format(user.userfitbit.access_token)
            }
        ).content)

        latest_pooled, _ = UserPooledTimestamp.objects.get_or_create(user=user, pool_date=now, is_scraped=True)
        latest_pooled.steps = data['activities-steps'][0]['value']
        latest_pooled.save()

        user.profile.credits = reduce(lambda x, y: x + y.steps / settings.CREDITS_PRICE,
                                      UserPooledTimestamp.objects.filter(user=user), 0)
        user.profile.save()
        data = {'credits': user.profile.credits}

        return HttpResponse(json.dumps(data), content_type="application/json")


class PointView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PointView, self).dispatch(request, *args, **kwargs)

    def put(self, request):
        try:
            user = User.objects.get(id=request.GET['user_id'])
        except KeyError:
            return HttpResponse({'error': 'User id is required'}, content_type="application/json")

        if user.profile.credits > 0:
            UserPooledTimestamp.objects.create(user=user, pool_date=timezone.now(), steps=-1)
            user.profile.credits -= 1
            user.profile.save()

        return HttpResponse(json.dumps({'credits': user.profile.credits}), content_type='application/json')
