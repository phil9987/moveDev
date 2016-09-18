import json

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from game.models import PlayBoard
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction
import random


@csrf_exempt
@transaction.atomic
def index(request):
    if request.method == 'GET':
        boards = PlayBoard.objects.filter(
            Q(player1=request.user) | Q(player2=request.user),
            game_id=0,
            finished_at=None
        )
        created = True
        if boards.count() == 1:
            board = boards[0]
            created = False
        elif boards.count() > 1:
            boards.delete()
            created = True
        if created:
            board = PlayBoard(player1=request.user, game_id=0, finished_at=None)
            # randomizing players positions on new boards
            board.currstate = [[{'player_id': 0, 'value': 0} for i in range(0, 10)] for i in
                               range(0, 10)]  # blank matrix
            row, col = random.randint(0, 9), random.randint(0, 9)
            board.currstate[row][col]['value'] = board.player1.profile.credits
            board.currstate[row][col]['player_id'] = board.player1.id

            board.player2 = User.objects.filter(~Q(id=request.user.id))[
                random.randint(0, User.objects.filter(~Q(id=request.user.id)).count() - 1)]
            row, col = random.randint(0, 9), random.randint(0, 9)
            board.currstate[row][col]['value'] = board.player2.profile.credits
            board.currstate[row][col]['player_id'] = board.player2.id
            board.currstate = json.dumps(board.currstate)

            board.save()
        return HttpResponse(json.dumps({"gameState": board.currstate, "gameId": board.id, "owner": request.user.id}),
                            content_type="application/json")
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
        print(int(currstate[sender_x][sender_y]['player_id']))
        print(request.user.id)
        print(int(currstate[sender_x][sender_y]['player_id']) == request.user.id)
        print(currstate)
        if int(currstate[sender_x][sender_y]['player_id']) == request.user.id:
            sender_value = currstate[sender_x][sender_y]['value']
            currstate[sender_x][sender_y]['value'] = sender_value / 2
            if int(currstate[rcvr_x][rcvr_y]['player_id']) == request.user.id or int(
                    currstate[rcvr_x][rcvr_y]['player_id']) == 0:
                currstate[rcvr_x][rcvr_y]['value'] += + sender_value / 2
                currstate[rcvr_x][rcvr_y]['player_id'] = request.user.id
            else:
                if sender_value > currstate[rcvr_x][rcvr_y]['value']:
                    currstate[rcvr_x][rcvr_y]['player_id'] = request.user.id
                currstate[rcvr_x][rcvr_y]['value'] = abs(currstate[rcvr_x][rcvr_y]['value'] - sender_value / 2)
            board.currstate = json.dumps(currstate)
            board.save()
        return HttpResponse(json.dumps({"gameState": board.currstate, "gameId": board.id, "owner": request.user.id}),
                            content_type="application/json")
    else:
        return HttpResponse(status=200)


@csrf_exempt
def update(request):
    board = PlayBoard.objects.get(id=request.GET['id'])
    currste = json.loads(board.currstate)
    p1credits = 0
    p2credits = 0
    gameFinished = False
    for row in currste:
        p1credits += reduce(lambda aku, d: aku + d['value'],
                            filter(lambda col: int(col['player_id']) == board.player1.id, row), 0)
        p2credits += reduce(lambda aku, d: aku + d['value'],
                            filter(lambda col: int(col['player_id']) == board.player2.id, row), 0)

    if p2credits == 0:
        gameFinished = True
        board.finished_at = timezone.now()
        board.save()
    return HttpResponse(json.dumps(
        {"gameState": board.currstate, "gameId": board.id, "owner": request.user.id, "gamefinished": gameFinished}),
        content_type="application/json")
