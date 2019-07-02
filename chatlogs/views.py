from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from chatlogs import models as chat_models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json, datetime, re


def session_add(request, name):
    if not request.user.is_superuser:
        return HttpResponse(status=401)
    if not name:
        return HttpResponse(status=403)
    else:
        try:
            game = chat_models.Game.objects.get(name__iexact=name)
            if request.method == 'GET':
                return render(request, 'chatlogs/session-add.html', {'game': game})
            elif request.method == 'POST':
                keys = request.POST.keys()
                if 'title' not in keys:
                    return HttpResponse('ERROR: title cannot be empty.', status=400)
                session = chat_models.Session(title=request.POST['title'], game=game)
                session.save()
                if 'chatlog' in keys and request.POST['chatlog'] != '':
                    try:
                        chatlog = json.loads(request.POST['chatlog'])
                        session.import_chatlog(chatlog)
                        session.save()
                    except:
                        return HttpResponse('Invalid json in the chatlog.', status=400)
                return render(request, 'chatlogs/session-add.html', {'status': 'successfully added chatlog'})
            else:
                return HttpResponse(status=405)
        except ObjectDoesNotExist:
            return HttpResponse('Game not found.', status=403)


def session_view(request, name, session_name):
    if not name:
        return HttpResponse('Game not found.', status=403)
    if not session_name:
        return HttpResponse('Session does not exist.', status=403)
    else:
        try:
            game = chat_models.Game.objects.get(name__iexact=name)
            session = chat_models.Session.objects.get(title__iexact=session_name, game=game)
            messages = chat_models.Message.objects.filter(session=session)
            for message in messages:
                if message.message_type == 't':
                    message.attacks = json.loads(message.attacks)
            return render(request, 'chatlogs/session-view.html', {'game': game, 'session': session, 'messages': messages})
        except:
            return HttpResponse('Game or session not found.', status=403)

def session_edit(request, name, session_name):
    if not request.user.is_superuser:
        return HttpResponse(status=401)
    if not name:
        return HttpResponse('Game not found.', status=403)
    if not session_name:
        return HttpResponse('Session does not exist.', status=403)
    else:
        try:
            game = chat_models.Game.objects.get(name__iexact=name)
            session = chat_models.Session.objects.get(title__iexact=session_name, game=game)
            messages = chat_models.Message.objects.filter(session=session)
            for message in messages:
                if message.message_type == 't':
                    message.attacks = json.loads(message.attacks)
            if request.method == 'GET':
                return render(request, 'chatlogs/session-edit.html',
                          {'game': game, 'session': session, 'messages': messages})
            elif request.method == 'POST':
                keys = request.POST.keys()
                if 'action' not in keys:
                    return HttpResponse('No action selected', status=403)
                else:
                    # get message ids from checkbox keys
                    messages_selected = []
                    for key in keys:
                        message_id = re.search(r'message-(\d+)', key)
                        if message_id:
                            messages_selected.append(message_id.group(1))
                    if not messages_selected:
                        return HttpResponse('No messages selected.', status=403)
                    # delete exactly the selected messages
                    if request.POST['action'] == 'delete_selected':
                        try:
                            for message_id in messages_selected:
                                chat_models.Message.objects.get(id__iexact=message_id).delete()
                            messages = chat_models.Message.objects.filter(session=session)
                            return render(request,
                                          'chatlogs/session-edit.html',
                                          {'game': game, 'session': session, 'messages': messages})
                        except:
                            return HttpResponse('Error deleting message.', status=403)
                    # delete all messages for this session before the first selected message
                    elif request.POST['action'] == 'delete_before':
                        try:
                            to_delete = chat_models.Message.objects.filter(session=session, id__lte=messages_selected[0])
                            for msg in to_delete:
                                msg.delete()
                            # map(lambda msg: msg.delete(), to_delete)
                            messages = chat_models.Message.objects.filter(session=session)
                            return render(request, 'chatlogs/session-edit.html',
                                          {'game': game, 'session': session, 'messages': messages})
                        except:
                            return HttpResponse('Error deleting message.', status=403)
                    # delete all messages for this session after the last selected message
                    elif request.POST['action'] == 'delete_after':
                        try:
                            to_delete = chat_models.Message.objects.filter(session=session, id__gte=messages_selected[-1])
                            for msg in to_delete:
                                msg.delete()
                            messages = chat_models.Message.objects.filter(session=session)
                            return render(request, 'chatlogs/session-edit.html',
                                          {'game': game, 'session': session, 'messages': messages})
                        except:
                            return HttpResponse('Error deleting message.', status=403)
                    else:
                        return HttpResponse(status=403)
            else:
                return HttpResponse(status=405)
        except:
            raise
            return HttpResponse('Game or session not found.', status=403)

def session_append(request, name, session_name):
    if not request.user.is_superuser:
        return HttpResponse(status=401)
    if not name:
        return HttpResponse('Game not found.', status=403)
    if not session_name:
        return HttpResponse('Session does not exist.', status=403)
    else:
        try:
            game = chat_models.Game.objects.get(name__iexact=name)
            session = chat_models.Session.objects.get(title__iexact=session_name, game=game)
            if request.method=='GET':
                return render(request, 'chatlogs/session-append.html', {'session': session})
            elif request.method=='POST':
                try:
                    chatlog = json.loads(request.POST['chatlog'])
                    session.import_chatlog(chatlog)
                    session.save()
                except:
                    return HttpResponse('Invalid json in the chatlog.', status=400)
                return render(request, 'chatlogs/session-append.html', {'session': session})
            else:
                return HttpResponse(status=405)
        except:
            return HttpResponse('Game or session not found.', status=403)