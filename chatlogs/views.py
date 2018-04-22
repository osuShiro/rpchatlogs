from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from chatlogs import models as chat_models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json, datetime

# Create your views here.

def export_chat_to_session(chatlog, session):
    for message in chatlog:
        if message['type'] == 'action':
            chat_models.Message(
                owner='',
                timestamp=datetime.datetime.strptime(message['timestamp'], '%B %d, %Y %I:%M%p'),
                text=message['text'],
                message_type='e',
                session=session
                ).save()
        elif message['type'] == 'description':
            chat_models.Message(
                owner='',
                timestamp=datetime.datetime.strptime(message['timestamp'], '%B %d, %Y %I:%M%p'),
                text=message['text'],
                message_type='d',
                session=session
                ).save()
        elif message['type'] == 'roll':
            chat_models.Message(
                owner=message['owner'],
                timestamp=datetime.datetime.strptime(message['timestamp'], '%B %d, %Y %I:%M%p'),
                message_type='r',
                session=session,
                formula=message['formula'],
                rolls=message['rolls'],
                result=message['result']
            ).save()
        elif message['type'] == 'skill roll':
            chat_models.Message(
                owner=message['owner'],
                timestamp=datetime.datetime.strptime(message['timestamp'], '%B %d, %Y %I:%M%p'),
                text=message['text'],
                message_type='k',
                session=session,
                details=message['roll_detail'],
                result=message['result'],
                notes=message['notes']
                ).save()
        elif message['type'] == 'attack':
            chat_models.Message(
                owner=message['owner'],
                timestamp=datetime.datetime.strptime(message['timestamp'], '%B %d, %Y %I:%M%p'),
                text=message['text'],
                message_type='t',
                session=session,
                attacks=json.dumps(message['attacks']),
                notes=message['notes']
                ).save()
        elif message['type'] == 'spell':
            chat_models.Message(
                owner=message['owner'],
                timestamp=datetime.datetime.strptime(message['timestamp'], '%B %d, %Y %I:%M%p'),
                text=message['text'],
                message_type='p',
                session=session
                ).save()
        elif message['type'] == 'ability':
            chat_models.Message(
                owner=message['owner'],
                timestamp=datetime.datetime.strptime(message['timestamp'], '%B %d, %Y %I:%M%p'),
                text=message['text'],
                message_type='a',
                session=session
                ).save()
        else:
            chat_models.Message(
                owner=message['owner'],
                timestamp=datetime.datetime.strptime(message['timestamp'], '%B %d, %Y %I:%M%p'),
                text=message['text'],
                message_type='g',
                session=session
            ).save()

def home(request):
    games = (chat_models.Game.objects.all())
    return render(request, 'chatlogs/home.html', {'game_list': games})

@login_required()
def game_admin(request):
    games = (chat_models.Game.objects.all())
    return render(request, 'chatlogs/game-admin.html', {'game_list': games})

@login_required()
def game_add(request):
    if request.method=='GET':
        return render(request, 'chatlogs/game-add.html')
    elif request.method=='POST':
        keys = request.POST.keys()
        name = request.POST['name'] if 'name' in keys else ''
        games = chat_models.Game.objects.filter(name__iexact=name)
        if games:
            return HttpResponse('ERROR: game name already in use', status=400)
        gm = request.POST['gm'] if 'gm' in keys else ''
        system = request.POST['system'] if 'system' in keys else ''
        chat_models.Game(name=name, gm=gm, system=system).save()
        return render(request, 'chatlogs/game-add-success.html', {'name': name})
    else:
        return HttpResponse(status=405)

@login_required()
def game_delete(request, name):
    if request.method=='POST':
        if not name:
            return HttpResponse(status=403)
        else:
            try:
                game = chat_models.Game.objects.get(name__iexact=name)
                game.delete()
            except ObjectDoesNotExist:
                return HttpResponse('Game not found.', status=403)
            except MultipleObjectsReturned:
                return HttpResponse(status=403)
            games = (chat_models.Game.objects.all())
            return render(request, 'chatlogs/game-admin.html', {'game_list': games})
    else:
        return HttpResponse(status=405)

def game_view(request, name):
    if not name:
        return HttpResponse(status=403)
    else:
        try:
            game = chat_models.Game.objects.get(name__iexact=name)
            sessions = chat_models.Session.objects.filter(game=game)
            if request.method=='GET':
                    return render(request, 'chatlogs/game-edit.html', {'game': game, 'action': 'view', 'sessions': sessions})
            else:
                return HttpResponse(status=405)
        except ObjectDoesNotExist:
            return HttpResponse('Game not found.', status=403)

def game_edit(request, name):
    if not name:
        return HttpResponse(status=403)
    else:
        try:
            game = chat_models.Game.objects.get(name__iexact=name)
            sessions = chat_models.Session.objects.filter(game=game)
            if request.method=='GET':
                    return render(request, 'chatlogs/game-edit.html', {'game': game, 'action': 'edit', 'sessions': sessions})
            elif request.method=='POST':
                keys = request.POST.keys()
                game.name = request.POST['name'] if 'name' in keys else game.name
                game.gm = request.POST['gm'] if 'gm' in keys else game.gm
                game.system = request.POST['system'] if 'system' in keys else game.system
                game.save()
                return render(request, 'chatlogs/game-edit.html', {'game': game, 'action': 'edit', 'sessions': sessions})
            else:
                return HttpResponse(status=405)
        except ObjectDoesNotExist:
            return HttpResponse('Game not found.', status=403)

@login_required()
def session_add(request, name):
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
                        export_chat_to_session(chatlog, session)
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
            return render(request, 'chatlogs/session_view.html', {'game': game, 'session': session, 'messages': messages})
        except:
            return HttpResponse('Game or session not found.', status=403)