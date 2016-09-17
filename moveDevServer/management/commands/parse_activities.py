import json

import requests
from django.conf import settings

from django.core.management import BaseCommand
from fitapp.models import UserFitbit
from moveDevServer.models import Activity
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        for u in UserFitbit.objects.all():
            if Activity.objects.filter(owner_id=u.fitbit_user).count() > 0:
                activities = json.loads(requests.get(
                    'http://api.fitbit.com/1/user/{}/activities/date/2010-03-01.json'.format(
                        u.fitbit_user,
                        timezone.now().strftime("%Y-%m-%d")
                    )
                ).content)
                for a in activities:
                    if a['activityParentId'] == 90013:
                        u.user.profile.credits += a['steps'] / settings.CREDITS_PRICE
                        Activity.objects.filter(activity_id=a['activityId']).delete()
