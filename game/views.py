import json
import random
import string

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from game.models import PlayBoard
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
import random
import string


@csrf_exempt
@transaction.atomic
def index(request):
    if request.method == 'GET':
        board, created = PlayBoard.objects.get_or_create(
            player1=request.user,
            game_id=0,
            finished_at=None
        )
        if created:
            # randomizing players positions on new boards
            board.currstate = [[0 for i in range(0, 10)] for i in range(0, 10)]  # blank matrix
            row, col = random.randint(0, 9), random.randint(0, 9)
            board.currstate[row][col] = board.player1.profile.credits
            row, col = random.randint(0, 9), random.randint(0, 9)
            board.player2 = User.objects.filter(~Q(id=request.user.id))[
                random.randint(0, User.objects.filter(~Q(id=request.user.id)).count() - 1)]
            board.currstate[row][col] = board.player2.profile.credits

            board.save()
        return HttpResponse(json.dumps({"gameState": board.currstate, "gameId": board.id}), content_type="application/json")
    else:
        return HttpResponse({})


@csrf_exempt
def play(request):
    if request.method == 'POST':
        data = request.POST
        sender_x = int(data['sender[x]'])
        sender_y = int(data['sender[y]'])
        rcvr_x = int(data['reciever[x]'])
        rcvr_y = int(data['reciever[y]'])

        board = PlayBoard.objects.get(id=request.GET['id'])
        currstate = json.loads(board.currstate)
        sender_value = currstate[sender_x][sender_y]
        currstate[rcvr_x][rcvr_y] = sender_value / 2
        currstate[sender_x][sender_y] = sender_value / 2
        board.currstate = json.dumps(currstate)
        print(currstate)
        print(rcvr_x, rcvr_y)
        print(sender_x, sender_y)
        board.save()
        return HttpResponse(json.dumps({"gameState": board.currstate, "gameId": board.id}), content_type="application/json")
    else:
        return HttpResponse(status=200)
