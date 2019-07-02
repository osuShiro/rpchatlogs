from django.shortcuts import render
from django.http import HttpResponse
from chatlogs import models as chat_models
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import json, re


def sessions(request, game_name, session_name=None):
    if not game_name:
        return HttpResponse('Game not found.', status=404)

    try:
        game = chat_models.Game.objects.get(name__iexact=game_name)
    except ObjectDoesNotExist:
        return HttpResponse('Game not found.', status=404)

    try:
        session = chat_models.Session.objects.get(title__iexact=session_name, game=game)
    except ObjectDoesNotExist:
        return HttpResponse('Session not found.', status=404)

    if request.method == 'GET':
        return sessions_get(request, game, session)

    # further methods require admin
    if not request.user.is_superuser:
        return HttpResponse(status=401)
    if request.method == 'POST':
        return sessions_post(request, game, session)
    if request.method == 'PUT':
        return sessions_put(request, game, session)
    return HttpResponse(status=405)


@login_required()
def sessions_get(request, game, session):
    messages = chat_models.Message.objects.filter(session=session)
    for message in messages:
        if message.message_type == 't':
            message.attacks = json.loads(message.attacks)
    return render(request, 'chatlogs/session-edit.html', {'game': game, 'session': session, 'messages': messages})


@login_required()
def sessions_patch(request, game, session):
    messages = chat_models.Message.objects.filter(session=session)
    for message in messages:
        if message.message_type == 't':
            message.attacks = json.loads(message.attacks)
    keys = request.POST.keys()

    # get message ids from checkbox keys
    messages_selected = []
    for key in keys:
        message_id = re.search(r'message-(\d+)', key)
        if message_id:
            messages_selected.append(message_id.group(1))
    if not messages_selected:
        return HttpResponse('No messages selected.', status=400)

    # delete exactly the selected messages
    if request.POST['action'] == 'delete_selected':
        session_patch_delete_selected(messages_selected)

    # delete all messages for this session before the first selected message included
    elif request.POST['action'] == 'delete_before':
        session_patch_delete_before(session, messages_selected)

    # delete all messages for this session after the last selected message included
    elif request.POST['action'] == 'delete_after':
        session_patch_delete_after(session, messages_selected)

    else:
        return HttpResponse(status=400)

    messages = chat_models.Message.objects.filter(session=session)
    return render(request, 'chatlogs/session-edit.html',
                  {'game': game, 'session': session, 'messages': messages})


@login_required()
def sessions_post(request, game, session):
    keys = request.POST.keys()
    if 'action' in keys:
        return sessions_patch(request, game, session)

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
    return render(request, 'chatlogs/game-admin.html', {'game': game, 'sessions': sessions_list}, status=201)



def sessions_put(request, game, session):
    try:
        chatlog = json.loads(request.POST['chatlog'])
    except:
        return HttpResponse('Invalid json in the chatlog.', status=400)
    session.import_chatlog(chatlog)
    session.save()
    messages = chat_models.Message.objects.filter(session=session)
    return render(request, 'chatlogs/session-edit.html', {'game': game, 'session': session, 'messages': messages})


def session_patch_delete_selected(messages_selected):
    try:
        for message_id in messages_selected:
            chat_models.Message.objects.get(id__iexact=message_id).delete()
    except ObjectDoesNotExist:
        return HttpResponse('Error deleting message.', status=401)


def session_patch_delete_before(session, messages_selected):
    try:
        to_delete = chat_models.Message.objects.filter(session=session, id__lte=messages_selected[0])
        for msg in to_delete:
            msg.delete()
    except ObjectDoesNotExist:
        return HttpResponse('Error deleting message.', status=401)


def session_patch_delete_after(session, messages_selected):
    try:
        to_delete = chat_models.Message.objects.filter(session=session, id__gte=messages_selected[-1])
        for msg in to_delete:
            msg.delete()
    except ObjectDoesNotExist:
        return HttpResponse('Error deleting message.', status=403)