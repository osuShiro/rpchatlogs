from django.conf.urls import url
from django.contrib import admin
#from chatlogs import views as chat_views
from django.contrib.auth import views as auth_views
from chatlogs.views import games, games_admin, games_add

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name': 'chatlogs/registration/login.html'}, name='login'),
    url(r'^game-admin/(?P<name>.+)/session/add/$', chat_views.session_add),
    url(r'^game-admin/(?P<name>.+)/session/(?P<session_name>.+)/append/$', chat_views.session_append),
    url(r'^game-admin/(?P<name>.+)/session/(?P<session_name>.+)/$', chat_views.session_edit),
    url(r'^game-admin/(?P<name>.+)/$', games_admin),
    url(r'^game-admin/new', games_add),
    url(r'^game-admin', games_admin),
    url(r'^game/(?P<name>.+)/session/(?P<session_name>.+)/$', chat_views.session_view),
    url(r'^game/(?P<name>.+)/$', games),
    url(r'^game/$', games),
]
