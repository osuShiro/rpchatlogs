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
    if request.method == 'POST':
        return sessions_add_post(request, game)
    return HttpResponse(status=405)


@login_required()
def sessions_add_post(request, game):
    keys = request.POST.keys()

    if 'title' not in keys:
        return HttpResponse('ERROR: title cannot be empty.', status=400)
    if 'chatlog' not in keys or request.POST['chatlog'] == '':
        return HttpResponse('No chatlog to add.')

    session = chat_models.Session(title=request.POST['title'], game=game)
    session.save()
    try:
        chatlog = json.loads(request.POST['chatlog'])
        session.import_chatlog(chatlog)
        session.save()
    except:
        return HttpResponse('Invalid json in the chatlog.', status=400)

    sessions_list = chat_models.Session.objects.filter(game=game)
    return render(request, 'chatlogs/session-add.html', {'game': game}, status=201)