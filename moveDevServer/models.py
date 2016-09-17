from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class UserPooledTimestamp(models.Model):
    pool_date = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
