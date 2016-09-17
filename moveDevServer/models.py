from __future__ import unicode_literals

import datetime

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserPooledTimestamp(models.Model):
    pool_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    steps = models.IntegerField(default=0)
    is_scraped = models.BooleanField(default=False)

    @property
    def get_lates_pool_date(self):
        return self.pool_date - datetime.timedelta(days=1)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    credits = models.PositiveIntegerField(default=0)


class Activity(models.Model):
    activity_id = models.CharField(max_length=16)
    collection_type = models.CharField(max_length=32)
    owner_id = models.CharField(max_length=16)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created=False, **kwarg):
    if created:
        Profile.objects.create(user=instance)
