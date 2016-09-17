from django.shortcuts import render
from django.http import HttpResponse
import json


def index(request):
    init_arr = []
    for i in range(0,10):
        init_arr.append([0]*10)
    print init_arr
    init_arr[0][3] = 77
    init_arr[8][8] = -68
    data = json.dumps(init_arr)
    return HttpResponse(data, content_type='application/json')