import json
from time import gmtime, strftime

import datetime

import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.
from django.views.generic import TemplateView, View
from fitapp.models import UserFitbit
from fitapp.utils import create_fitbit
from fitapp.views import get_data
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
        now = datetime.datetime.now()
        data = requests.get(
            'https://api.fitbit.com/1/user/{}/activities/steps/date/{}/{}.json'.format(
                user.userfitbit.fitbit_user,
                latest_pooled.pool_date.strftime("%Y-%m-%d"),
                now.strftime("%Y-%m-%d")
            ),
            headers={
                'Authorization': "Bearer {}".format(user.userfitbit.access_token)
            }
        ).content

        latest_pooled.pool_date = now
        latest_pooled.save()

        return HttpResponse(data, content_type="application/json")
