from django.test import TestCase, Client
from django.contrib.auth.models import User
from chatlogs import models
from . import login


CLIENT = Client()
CLIENT_ADMIN = Client()

class SessionTestCase(TestCase):

    def setUpTestData():
        admin = User.objects.create_superuser(username='admin', email='', password='admin')
        admin.save()

        player = User.objects.create_user(username='player', email='', password='bla')
        player.save()

        game_public = models.Game(
            name='public game',
            gm='gm1',
            system='vanilla',
        )
        game_public.save()

        session1 = models.Session(
            title='session1',
            date='1990-01-01',
            game=game_public,
        )
        session1.save()

    def test_session_edit_not_superuser(self):
        CLIENT.login(username='player',password='bla')
        self.assertEqual(CLIENT.get('/game-admin/public game/session1').status_code, 401)