from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from chatlogs import models as chat_models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json, datetime, re


@login_required()
def games_admin(request, name=None):
    if not request.user.is_superuser:
        return HttpResponse(status=401)
    if request.method == 'POST':
        return games_admin_post(request)
    if not name:
        return games_admin_home(request)
    if request.method == 'GET':
        return games_admin_get(request, name)
    if request.method == 'PATCH':
        return games_admin_patch(request, name)
    if request.method == 'DELETE':
        return games_admin_delete(request, name)


def games_admin_home(request):
    if request.method != 'GET':
        return HttpResponse(status=405)
    games_list = (chat_models.Game.objects.all())
    return render(request, 'chatlogs/game-admin.html', {'game_list': games_list})


def games_admin_get(request, name):
    try:
        game = chat_models.Game.objects.get(name__iexact=name)
    except ObjectDoesNotExist:
        return HttpResponse('Game not found.', status=403)
    sessions = chat_models.Session.objects.filter(game=game)
    return render(request, 'chatlogs/game-edit.html', {'game': game, 'action': 'view', 'sessions': sessions})


def games_admin_patch(request, name):
    try:
        game = chat_models.Game.objects.get(name__iexact=name)
    except ObjectDoesNotExist:
        return HttpResponse('Game not found.', status=403)
    sessions = chat_models.Session.objects.filter(game=game)
    keys = request.POST.keys()
    game.name = request.POST['name'] if 'name' in keys else game.name
    game.gm = request.POST['gm'] if 'gm' in keys else game.gm
    game.system = request.POST['system'] if 'system' in keys else game.system
    game.save()
    return render(request, 'chatlogs/game-edit.html', {'game': game, 'action': 'edit', 'sessions': sessions})


def games_admin_post(request):
    keys = request.POST.keys()
    name = request.POST['name'] if 'name' in keys else None
    if not name:
        return HttpResponse('Game name missing.', status=401)
    games = chat_models.Game.objects.filter(name__iexact=name)
    if games:
        return HttpResponse('ERROR: game name already in use', status=400)
    gm = request.POST['gm'] if 'gm' in keys else ''
    system = request.POST['system'] if 'system' in keys else ''
    chat_models.Game(name=name, gm=gm, system=system).save()
    games_list = (chat_models.Game.objects.all())
    return render(request, 'chatlogs/game-admin.html', {'game_list': games_list}, status=201)

def games_admin_delete(request, name):
    try:
        game = chat_models.Game.objects.get(name__iexact=name)
    except ObjectDoesNotExist:
        return HttpResponse('Game not found.', status=403)
    except MultipleObjectsReturned:
        return HttpResponse('Multiple games found.', status=403)
    game.delete()
    games = (chat_models.Game.objects.all())
    return render(request, 'chatlogs/game-admin.html', {'game_list': games})
