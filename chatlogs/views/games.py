from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from chatlogs import models as chat_models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json, datetime, re


def games(request, name=None):
    if request.method != 'GET':
        return HttpResponse(status=405)
    if not name:
        return games_home(request)
    return games_view(request, name)


def games_home(request):
    games_list = (chat_models.Game.objects.all())
    return render(request, 'chatlogs/home.html', {'game_list': games_list})


def games_view(request, name):
    try:
        game = chat_models.Game.objects.get(name__iexact=name)
        sessions = chat_models.Session.objects.filter(game=game)
        if request.method == 'GET':
            return render(request, 'chatlogs/game-edit.html', {'game': game, 'action': 'view', 'sessions': sessions})
        else:
            return HttpResponse(status=405)
    except ObjectDoesNotExist:
        return HttpResponse('Game not found.', status=403)
