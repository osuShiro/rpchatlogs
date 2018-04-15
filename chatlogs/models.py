from django.db import models

# Create your models here.

MESSAGE_TYPE = ('g', 'general',
                't', 'attack',
                'b', 'ability',
                'p', 'spell',
                'k', 'skill',
                'e', 'emote',
                'd', 'desc',
                'r', 'roll')

class Game(models):
    gm = models.CharField(max_length=128, blank=True, default='')
    system = models.CharField(max_length=256, blank=True, default='vanilla')

class Session(models):
    title = models.CharField(max_length=256, default='')
    date = models.DateTimeField(default=None)

    game = models.ForeignKey(Game)

class Message(models):
    owner = models.CharField(max_length=128, default='')
    timestamp = models.DateTimeField(default = None)
    text = models.TextField(default='')
    message_type = models.CharField(max_length=1, choices=MESSAGE_TYPE)

    session = models.ForeignKey(Session)

    class Meta:
        abstract = True

class General(Message):
    pass

class SkillRoll(General):
    details = models.TextField(default='')
    result = models.CharField(max_length=64, default='0')

class Attack(General):
    attacks = models.TextField(default='')
    notes = models.TextField(default='')

class Roll(Message):
    formula = models.TextField(default='')
    rolls = models.TextField(default='')
    result = models.CharField(max_length=64, default='0')
