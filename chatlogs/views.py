from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from chatlogs import models as chat_models

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
        gm = request.POST['gm'] if 'gm' in keys else ''
        system = request.POST['system'] if 'system' in keys else ''
        chat_models.Game(name=name, gm=gm, system=system).save()
        return HttpResponse('game added')