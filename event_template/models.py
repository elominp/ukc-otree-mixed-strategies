# -*- coding: utf-8 -*-

from otree.api import *


doc = """
"""


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class Constants(BaseConstants):
    name_in_url = 'template'
    players_per_group = None
    num_rounds = 1
    instructions_template = 'templates/Instructions.html'
