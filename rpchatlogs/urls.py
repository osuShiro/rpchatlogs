"""rpchatlogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from chatlogs import views as chat_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^game-admin/(?P<name>.+)/delete/$', chat_views.game_delete),
    url(r'^game-admin/(?P<name>.+)/session/add/$', chat_views.session_add),
    url(r'^game-admin/(?P<name>.+)/$', chat_views.game_view, {'action':'edit'}),
    url(r'^game-admin/new', chat_views.game_add),
    url(r'^game-admin', chat_views.game_admin),
    url(r'^login/$', auth_views.login, {'template_name': 'chatlogs/registration/login.html'}, name='login'),
    url(r'^(?P<name>.+)/$', chat_views.game_view, {'action':'view'}),
    url(r'^$', chat_views.home),
]
