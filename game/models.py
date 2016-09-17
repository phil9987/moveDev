from __future__ import unicode_literals
import random
import time
from django.db import models
import string
import json


# Create your models here.
class PlayBoard(models.Model):
    currstate = models.CommaSeparatedIntegerField(max_length=1000) # the gameboard
    player1_id = models.CharField(max_length=100)           # TODO: foreign key to user db
    player2_id = models.CharField(max_length=100)           # TODO: foreign key to user db
    game_id = models.CharField(max_length=100)
    #game_end = models.DateTimeField()                       # TODO: check constraints, user can only participate in one
                                                            # game at the same time.


    def __str__(self):
        res = []
        for i in range(0,10):
            res.append(self.currstate[10*i:10*i + 10])
        return json.dumps(res)

