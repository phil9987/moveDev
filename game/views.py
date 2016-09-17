from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
import json
from game.models import PlayBoard
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
import random
import time
import string


@csrf_exempt
@transaction.atomic
def index(request):
    if request.user.is_anonymous():
        return HttpResponse(status=403)
    if request.method == 'GET':
        board, created = PlayBoard.objects.get_or_create(
            player1=request.user,
            player2=User.objects.filter(~Q(id=request.user.id))[
                random.randint(0, User.objects.filter(~Q(id=request.user.id)).count() - 1)],
            game_id=0,
            finished_at=None
        )
        if created:
            # randomizing players positions on new boards
            board.currstate = [[0 for i in range(0, 10)] for i in range(0, 10)]  # blank matrix
            row, col = random.randint(0, 9), random.randint(0, 9)
            board.currstate[row][col] = board.player1.profile.credits
            row, col = random.randint(0, 9), random.randint(0, 9)
            board.currstate[row][col] = board.player2.profile.credits
            board.save()
        return HttpResponse(str(board), content_type="application/json")

    elif request.method == 'POST':
        data = request.POST
        sender_x = int(data['sender[x]'])
        sender_y = int(data['sender[y]'])
        rcvr_x = int(data['reciever[x]'])
        rcvr_y = int(data['reciever[x]'])
        board = PlayBoard.objects.filter(game_id=0)[0]
        curr_state = board.currstate
        old_state = [int(x) for x in string.split(curr_state[1:-1], ',')]
        print old_state
        sender_idx = sender_y * 10 + sender_x
        print sender_idx
        print old_state[sender_idx]
        sender_score = int(old_state[sender_idx])
        print sender_score
        rcvr_idx = rcvr_y * 10 + rcvr_x
        receiver_score = int(old_state[rcvr_idx])
        print receiver_score
        sender_score = sender_score / 2
        receiver_score += sender_score
        old_state[sender_idx] = sender_score
        old_state[rcvr_idx] = receiver_score
        board.currstate = old_state
        return HttpResponse(str(board), content_type="application/json")
    else:
        return HttpResponse(status=200)
