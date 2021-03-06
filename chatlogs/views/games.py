from django.shortcuts import render
from django.http import HttpResponse
from chatlogs import models as chat_models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def games(request, game_name=None):
    if request.method != 'GET':
        return HttpResponse(status=405)
    if not game_name:
        return games_home(request)
    try:
        game = chat_models.Game.objects.get(name__iexact=game_name)
    except ObjectDoesNotExist:
        return HttpResponse('Game not found.', status=404)
    except MultipleObjectsReturned:
        return HttpResponse('Multiple games exist with that name.', status=400)
    return games_view(request, game)


def games_home(request):
    games_list = (chat_models.Game.objects.all())
    return render(request, 'chatlogs/home.html', {'game_list': games_list})


def games_view(request, game):
    sessions = chat_models.Session.objects.filter(game=game)
    return render(request, 'chatlogs/game-edit.html', {'game': game, 'action': 'view', 'sessions': sessions})

