from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from chatlogs.views import games, games_admin, games_add
from chatlogs.views import sessions, sessions_add

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name': 'chatlogs/registration/login.html'}, name='login'),
    url(r'^game-admin/(?P<name>.+)/session/add/$', sessions_add),
    url(r'^game-admin/(?P<name>.+)/session/(?P<session_name>.+)/append/$', sessions_add),
    url(r'^game-admin/(?P<name>.+)/session/(?P<session_name>.+)/$', sessions),
    url(r'^game-admin/(?P<name>.+)/$', games_admin),
    url(r'^game-admin/new', games_add),
    url(r'^game-admin', games_admin),
    url(r'^game/(?P<name>.+)/session/(?P<session_name>.+)/$', sessions),
    url(r'^game/(?P<name>.+)/$', games),
    url(r'^game/$', games),
]