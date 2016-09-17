from __future__ import unicode_literals
import random
import time
from django.db import models
import string
import json

# Create your models here.
class PlayBoard(models.Model):
    state = models.CommaSeparatedIntegerField(max_length=4) # the gameboard
    player1_id = models.CharField(max_length=100)           # TODO: foreign key to user db
    player2_id = models.CharField(max_length=100)           # TODO: foreign key to user db
    game_id = models.CharField(max_length=100)
    game_end = models.DateTimeField()                       # TODO: check constraints, user can only participate in one
                                                            # game at the same time.

    def __init__(self, player1, player2):
        p1_score = 79           # TODO: get real scores from backend
        p2_score = -(56)        # TODO: get real scores from backend
        p1_start = random.randint(0, 100)
        p2_start = random.randint(0, 100)
        random.seed(time.localtime()[5])
        while p2_start == p1_start:
            p2_start = random.randint(0, 100)
        list = 100*[0]
        list[p1_start] = p1_score
        list[p2_start] = p2_score
        print list
        self.state = list
        self.player1_id = player1
        self.player2_id = player2


        def __str__(self):
            arr = string.split(self.state, ',')
            res = []
            for i in range(0,10):
                res.append(arr[10*i:10*i + 10])
            return json.dumps(res)

