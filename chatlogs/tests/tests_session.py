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

    def setUp(self):
        session1 = models.Session.objects.get(title__iexact='session1')
        for i in range(0, 10):
            message = models.Message(text='message' + str(i+1), session=session1)
            message.save()

    def test_session_public_view_no_game(self):
        self.assertEqual(CLIENT.get('/game/bla/session1').status_code, 404)

    def test_session_public_view_not_exist(self):
        self.assertEqual(CLIENT.get('/game/public game/wrongname').status_code, 404)

    def test_session_actions_not_superuser(self):
        CLIENT.login(username='player', password='bla')
        self.assertEqual(CLIENT.patch('/game-admin/public game/session1').status_code, 401)
        self.assertEqual(CLIENT.post('/game-admin/public game/session1').status_code, 401)
        self.assertEqual(CLIENT.delete('/game-admin/public game/session1').status_code, 401)
        self.assertEqual(CLIENT.get('/game-admin/public game/add/').status_code, 401)

    def test_session_patch_delete_no_messages(self):
        self.assertEqual(CLIENT_ADMIN.patch('/game-admin/public game/session1/',
                                            {'action': 'delete_selected'},
                                            HTTP_AUTHORIZATION='JWT {}'.format(login.login('admin'))).status_code,
                         401)

    def test_session_patch_delete_wrong_message(self):
        self.assertEqual(CLIENT_ADMIN.patch('/game-admin/public game/session1/',
                                            {'action': 'delete_selected',
                                             'message-30': 'on',},
                                            HTTP_AUTHORIZATION='JWT {}'.format(login.login('admin'))).status_code,
                         401)

    def test_session_patch_delete_selected(self):
        self.assertEqual(CLIENT_ADMIN.patch('/game-admin/public game/session1/',
                                            {'action':'delete_selected',
                                             'message-3': 'on',
                                             'message-5': 'on'},
                                            HTTP_AUTHORIZATION='JWT {}'.format(login.login('admin'))).status_code,
                         200)
        self.assertEqual(models.Message.objects.count(), 7)

    def test_session_patch_delete_before(self):
        self.assertEqual(CLIENT_ADMIN.patch('/game-admin/public game/session1/',
                                            {'action': 'delete_before',
                                             'message-3': 'on'},
                                            HTTP_AUTHORIZATION='JWT {}'.format(login.login('admin'))).status_code,
                         200)
        self.assertEqual(models.Message.objects.count(), 6)

    def test_session_patch_delete_after(self):
        self.assertEqual(CLIENT_ADMIN.patch('/game-admin/public game/session1/',
                                            {'action': 'delete_after',
                                             'message-3': 'on'},
                                            HTTP_AUTHORIZATION='JWT {}'.format(login.login('admin'))).status_code,
                         200)
        self.assertEqual(models.Message.objects.count(), 2)

    def test_session_add_wrong_methods(self):
        self.assertEqual(CLIENT_ADMIN.patch('/game-admin/public game/add/').status_code, 405)
        self.assertEqual(CLIENT_ADMIN.post('/game-admin/public game/add/').status_code, 405)
        self.assertEqual(CLIENT_ADMIN.delete('/game-admin/public game/add/').status_code, 405)

    def test_session_add_no_chatlog(self):
        self.assertEqual(CLIENT_ADMIN.post('/game-admin/public game/',
                                           {
                                               'title': 'title',
                                           },
                                           HTTP_AUTHORIZATION='JWT {}'.format(login.login('admin'))).status_code,
                         403)
        self.assertEqual(CLIENT_ADMIN.post('/game-admin/public game/',
                                           {
                                               'title': 'title',
                                               'chatlog': '',
                                           },
                                           HTTP_AUTHORIZATION='JWT {}'.format(login.login('admin'))).status_code,
                         403)

    def test_session_append_logged_out(self):
        self.assertEqual(CLIENT.get('/game-admin/public game/session1/append').status_code, 301)

    def test_session_append_not_superuser(self):
        CLIENT.login(username='player', password='bla')
        self.assertEqual(CLIENT.get('/game-admin/public game/session1/append').status_code, 403)

    def test_session_append_wrong_methods(self):
        self.assertEqual(CLIENT.patch('/game-admin/public game/session1/append').status_code, 405)
        self.assertEqual(CLIENT.post('/game-admin/public game/session1/append').status_code, 405)
        self.assertEqual(CLIENT.delete('/game-admin/public game/session1/append').status_code, 405)
