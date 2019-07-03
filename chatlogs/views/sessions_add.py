from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from chatlogs import models as chat_models
from django.core.exceptions import ObjectDoesNotExist
import json


@login_required()
def sessions_add(request, game_name):
    if not request.user.is_superuser:
        return HttpResponse(status=401)
    if not game_name:
        return HttpResponse(status=403)

    try:
        game = chat_models.Game.objects.get(name__iexact=game_name)
    except ObjectDoesNotExist:
        return HttpResponse('Game not found.', status=404)

    if request.method == 'GET':
        return render(request, 'chatlogs/session-add.html', {'game': game})
    return HttpResponse(status=405)
