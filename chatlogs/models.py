from django.db import models

# Create your models here.

MESSAGE_TYPE = (('g', 'general'),
                ('t', 'attack'),
                ('b', 'ability'),
                ('p', 'spell'),
                ('k', 'skill'),
                ('e', 'emote'),
                ('d', 'desc'),
                ('r', 'roll'))

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
