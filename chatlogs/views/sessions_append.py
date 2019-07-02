from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from chatlogs import models as chat_models
from django.core.exceptions import ObjectDoesNotExist


@login_required()
def sessions_append(request, game_name, session_name):
    if not request.user.is_superuser:
        return HttpResponse(status=401)

    if not game_name:
        return HttpResponse('Game not found.', status=404)
    try:
        game = chat_models.Game.objects.get(name__iexact=game_name)
    except ObjectDoesNotExist:
        return HttpResponse('Game not found.', status=404)

    if not session_name:
        return HttpResponse('No session selected.', status=404)
    try:
        session = chat_models.Session.objects.get(title__iexact=session_name, game=game)
    except ObjectDoesNotExist:
        return HttpResponse('Session not found.', status=404)

    if request.method != 'GET':
        return HttpResponse(status=405)

    return render(request, 'chatlogs/session-append.html', {'session': session})
