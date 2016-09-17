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
from moveDevServer.models import UserPooledTimestamp


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


class StepsView(View):
    def get(self, request):
        try:
            user = User.objects.get(id=request.GET['user_id'])
        except KeyError:
            return HttpResponse({'error': 'User id is required'}, content_type="application/json")

        latest_pooled, _ = UserPooledTimestamp.objects.get_or_create(user=user)
        now = timezone.now()
        url = 'https://api.fitbit.com/1/user/{}/activities/steps/date/{}/{}d/15min/time/{}/{}.json'.format(
            user.userfitbit.fitbit_user,
            latest_pooled.get_lates_pool_date.strftime("%Y-%m-%d"),
            (now - latest_pooled.pool_date).days or 1,
            latest_pooled.pool_date.strftime("%H:%M"),
            now.strftime("%H:%M")
        )
        data = requests.get(
            url,
            headers={
                'Authorization': "Bearer {}".format(user.userfitbit.access_token)
            }
        ).content

        latest_pooled.pool_date = now
        latest_pooled.save()

        data = json.loads(data)
        steps = reduce(lambda x, y: x + int(y['value']), data['activities-steps'], 0)
        user.profile.credits += steps / settings.CREDITS_PRICE
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
            user.profile.credits -= 1
            user.profile.save()

        return HttpResponse(json.dumps({'credits': user.profile.credits}), content_type='application/json')
