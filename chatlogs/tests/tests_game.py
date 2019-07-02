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

    def test_game_public_view(self):
        self.assertEqual(CLIENT.get('/game/').status_code, 200)
        self.assertEqual(CLIENT.get('/game/public game/').status_code, 200)
        self.assertEqual(CLIENT.post('/game/public game/').status_code, 405)
        self.assertEqual(CLIENT.patch('/game/public game/').status_code, 405)
        self.assertEqual(CLIENT.delete('/game/public game/').status_code, 405)

    def test_game_admin_logged_out(self):
        self.assertEqual(CLIENT.get('/game-admin/public game/').status_code, 401)

    def test_game_admin_not_admin(self):
        CLIENT.login(username='player', password='bla')
        self.assertEqual(CLIENT.get('/game-admin/public game/').status_code, 401)

    def test_game_admin_home(self):
        self.assertEqual(CLIENT_ADMIN.get('/game-admin/').status_code, 200)
        self.assertEqual(CLIENT_ADMIN.post('/game-admin/').status_code, 405)
        self.assertEqual(CLIENT_ADMIN.patch('/game-admin/').status_code, 405)
        self.assertEqual(CLIENT_ADMIN.delete('/game-admin/').status_code, 405)

    def test_game_admin_post(self):
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

    def test_game_admin_add(self):
        self.assertEqual(CLIENT.get('/game-admin/add/').status_code, 401)
        CLIENT.login(username='player', password='bla')
        self.assertEqual(CLIENT.get('/game-admin/add/').status_code, 401)
        self.assertEqual(CLIENT_ADMIN.get('/game-admin/add/').status_code, 200)
        self.assertEqual(CLIENT_ADMIN.post('/game-admin/add/').status_code, 405)
        self.assertEqual(CLIENT_ADMIN.patch('/game-admin/add/').status_code, 405)
        self.assertEqual(CLIENT_ADMIN.delete('/game-admin/add/').status_code, 405)

    def test_game_admin_post_no_name(self):
        self.assertEqual(CLIENT_ADMIN.post('/game-admin/',
                                           {
                                               'gm':'gm',
                                               'system':'system',
                                           },
                                           HTTP_AUTHORIZATION = 'JWT {}'.format(login.login('admin'))).status_code,
                         401)

    def test_game_admin_post_partial_payload(self):
        self.assertEqual(CLIENT_ADMIN.post('/game-admin/',
                                           {
                                               'name':'name',
                                               'system': 'system',
                                           },
                                           HTTP_AUTHORIZATION='JWT {}'.format(login.login('admin'))).status_code,
                         201)
        self.assertEqual(CLIENT_ADMIN.post('/game-admin/',
                                           {
                                               'name': 'name',
                                               'gm': 'gm',
                                           },
                                           HTTP_AUTHORIZATION='JWT {}'.format(login.login('admin'))).status_code,
                         201)

    def test_game_admin_delete_game_not_found(self):
        self.assertEqual(CLIENT_ADMIN.post('/game-admin/',
                                           {
                                               'name': 'wrongname',
                                           },
                                           HTTP_AUTHORIZATION='JWT {}'.format(login.login('admin'))).status_code,
                         403)

    def test_game_admin_delete_multiple_games_found(self):
        game2 = models.Game(
            name='public game',
            gm='gm',
            system='system',
        )
        game2.save()
        self.assertEqual(CLIENT_ADMIN.post('/game-admin/',
                                           {
                                               'name': 'public game',
                                           },
                                           HTTP_AUTHORIZATION='JWT {}'.format(login.login('admin'))).status_code,
                         403)

    def test_game_admin_delete(self):
        self.assertEqual(CLIENT_ADMIN.post('/game-admin/',
                                           {
                                               'name': 'public game',
                                           },
                                           HTTP_AUTHORIZATION='JWT {}'.format(login.login('admin'))).status_code,
                         200)
        self.assertEqual(models.Game.objects.count(), 0)