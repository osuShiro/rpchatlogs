from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from chatlogs import models as chat_models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# Create your views here.

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

@login_required()
def game_edit(request, name):
    if not name:
        return HttpResponse(status=403)
    else:
        try:
            game = chat_models.Game.objects.get(name__iexact=name)
            if request.method=='GET':
                return render(request, 'chatlogs/game-edit.html', {'game': game})
            elif request.method=='POST':
                keys = request.POST.keys()
                game.name = request.POST['name'] if 'name' in keys else game.name
                game.gm = request.POST['gm'] if 'gm' in keys else game.gm
                game.system = request.POST['system'] if 'system' in keys else game.system
                game.save()
                return render(request, 'chatlogs/game-edit.html', {'game': game})
            else:
                return HttpResponse(status=405)
        except ObjectDoesNotExist:
            return HttpResponse('Game not found.', status=403)
