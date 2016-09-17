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
    if request.method == 'GET':
        p1_score = 79  # TODO: get real scores from backend
        p2_score = -(56)  # TODO: get real scores from backend
        p1_start = random.randint(0, 99)
        p2_start = random.randint(0, 99)
        random.seed(time.localtime()[5])
        while p2_start == p1_start:
            p2_start = random.randint(0, 100)
        list = 100 * [0]
        list[p1_start] = p1_score
        list[p2_start] = p2_score
        print list

        board = PlayBoard.objects.create(player1_id=1, player2_id=2, game_id=0, currstate=list)
        print board.currstate
        res = []
        for i in range(0, 10):
            res.append(board.currstate[10 * i:10 * i + 10])
        print len(PlayBoard.objects.all())
        print str(board)
        data = json.dumps(res)
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
        sender_idx = sender_y*10 + sender_x
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
