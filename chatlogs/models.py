from django.db import models
import datetime, json

# Create your models here.

MESSAGE_TYPE = (('g', 'general'),
                ('t', 'attack'),
                ('b', 'ability'),
                ('p', 'spell'),
                ('k', 'skill'),
                ('e', 'emote'),
                ('d', 'desc'),
                ('r', 'roll')
                )

def message_type_to_db(message):
    pass

class Game(models.Model):
    name = models.CharField(max_length=128, default='')
    gm = models.CharField(max_length=128, default='')
    system = models.CharField(max_length=256, blank=True, default='vanilla')

class Session(models.Model):
    title = models.CharField(max_length=256, default='')
    date = models.DateTimeField(default=None, null=True)

    game = models.ForeignKey(Game)

    def __str__(self):
        return self.game.name + ': ' + self.title

    def import_chatlog(self, chatlog):
        for message in chatlog:
            if 'text' not in message.keys():
                message['text'] = ''
            # the only unchanged fields are owner, text, timestamp and session
            new_message = Message(
                owner = message['owner'],
                timestamp = datetime.datetime.strptime(message['timestamp'], '%B %d, %Y %I:%M%p'),
                text = message['text'],
                session = self,
            )
            if message['type'] == 'action':
                new_message.message_type = 'e'
            elif message['type'] == 'description':
                new_message.message_type = 'd'
            elif message['type'] == 'roll':
                new_message.message_type = 'r'
                new_message.formula = message['formula']
                new_message.rolls = message['rolls']
                new_message.result = message['result']
            elif message['type'] == 'skill roll':
                new_message.message_type = 'k'
                new_message.details = message['roll_detail']
                new_message.result = message['result']
                new_message.notes = message['notes']
            elif message['type'] == 'attack':
                new_message.message_type = 't'
                new_message.attacks = json.dumps(message['attacks'])
                new_message.notes = message['notes']
            elif message['type'] == 'spell':
                new_message.message_type = 'p'
            elif message['type'] == 'ability':
                new_message.message_type = 'a'
            else:
                new_message.message_type = 'g'
            new_message.save()

class Message(models.Model):
    owner = models.CharField(max_length=128, default='')
    timestamp = models.DateTimeField(default = None)
    text = models.TextField(default='')
    message_type = models.CharField(max_length=1, choices=MESSAGE_TYPE)
    details = models.TextField(default='')
    formula = models.TextField(default='')
    rolls = models.TextField(default='')
    result = models.CharField(max_length=64, default='0')
    notes = models.TextField(default='')
    attacks = models.TextField(default='')

    session = models.ForeignKey(Session)
