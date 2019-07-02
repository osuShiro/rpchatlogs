from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from chatlogs.views import games, games_admin, games_add
from chatlogs.views import sessions, sessions_add, sessions_append

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name': 'chatlogs/registration/login.html'}, name='login'),
    url(r'^game-admin/new/$', games_add),
    url(r'^game-admin/(?P<game_name>.+)/session/add/$', sessions_add),
    url(r'^game-admin/(?P<game_name>.+)/session/(?P<session_name>.+)/append/$', sessions_append),
    url(r'^game-admin/(?P<game_name>.+)/session/(?P<session_name>.+)/$', sessions),
    url(r'^game-admin/(?P<game_name>.+)/$', games_admin),
    url(r'^game-admin/$', games_admin),
    url(r'^game/(?P<game_name>.+)/session/(?P<session_name>.+)/$', sessions),
    url(r'^game/(?P<game_name>.+)/$', games),
    url(r'^game/$', games),
]