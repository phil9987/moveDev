from django.shortcuts import render
from django.http import HttpResponse
import json
from game.models import PlayBoard


def index(request):
    if request.method == 'GET':
        board = PlayBoard(player1=1, player2=2)
        #init_arr = board.state
        res = []
        for i in range(0, 10):
            res.append(board.state[10 * i:10 * i + 10])
        data =  json.dumps(res)
        return HttpResponse(data, content_type='application/json')

    elif request.method == 'PUT':
        return HttpResponse({'data': 'None'}, content_type='application/json')
