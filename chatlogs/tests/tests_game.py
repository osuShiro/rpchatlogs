from django.test import TestCase, Client
from django.contrib.auth.models import User
from chatlogs import models
from . import login


CLIENT = Client()
CLIENT_ADMIN = Client()


class GameTestCase(TestCase):

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

    def setUp(self):
        CLIENT_ADMIN.login(username='admin', password='admin')

    def test_view_public_game(self):
        self.assertEqual(CLIENT.get('/game/public game/').status_code, 200)
        self.assertEqual(CLIENT.post('/game/public game/').status_code, 405)
        self.assertEqual(CLIENT.patch('/game/public game/').status_code, 405)
        self.assertEqual(CLIENT.delete('/game/public game/').status_code, 405)

    def test_edit_game_logged_out(self):
        self.assertEqual(CLIENT.get('/game-admin/public game/').status_code, 401)

    def test_edit_game_not_admin(self):
        CLIENT.login(username='player', password='bla')
        self.assertEqual(CLIENT.get('/game-admin/public game/').status_code, 401)

    def test_edit_game(self):
        self.assertEqual(CLIENT_ADMIN.post('/game-admin/public game/',
                                            {'name':'edited',
                                             'gm':'edited',
                                             'system':'edited',
                                             },
                                            HTTP_AUTHORIZATION='JWT {}'.format(login.login('admin'))).status_code,
                         200)
        game_public = models.Game.objects.get(name__iexact='edited')
        self.assertEqual(game_public.gm, 'edited')
        self.assertEqual(game_public.system, 'edited')

    #TODO: check if editing a game name properly edits the game's session