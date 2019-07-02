from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required()
def games_add(request):
    if not request.user.is_superuser:
        return HttpResponse(status=401)
    if request.method != 'GET':
        return HttpResponse(status=405)
    return render(request, 'chatlogs/game-add.html')