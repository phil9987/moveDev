from __future__ import unicode_literals
import random
import time

from django.conf import settings
from django.db import models
import string
import json


# Create your models here.
class PlayBoard(models.Model):
    currstate = models.CommaSeparatedIntegerField(max_length=1000, null=True, blank=True)  # the gameboard
    player1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player1')
    player2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player2', null=True, blank=True)
    game_id = models.CharField(max_length=100)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return json.dumps(self.currstate)
