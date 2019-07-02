from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from chatlogs import models as chat_models
from django.core.exceptions import ObjectDoesNotExist
import json


@login_required()
def sessions_add(request, game_name, session_name=None):
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

    try:
        session = chat_models.Session.objects.get(title__iexact=session_name, game=game)
    except ObjectDoesNotExist:
        return HttpResponse('Session not found', status=404)

    if request.method == 'POST':
        return sessions_add_append(request, game, session)


def sessions_add_append(request, game, session):
    try:
        chatlog = json.loads(request.POST['chatlog'])
    except:
        return HttpResponse('Invalid json in the chatlog.', status=400)
    session.import_chatlog(chatlog)
    session.save()
    messages = chat_models.Message.objects.filter(session=session)
    return render(request, 'chatlogs/session-edit.html', {'game': game, 'session': session, 'messages': messages})