# -*- coding: utf-8 -*-

from otree.api import *


doc = """
"""


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    wage = models.IntegerField(choices=range(1, 11), widget=widgets.RadioSelectHorizontal)
    desired_effort_level = models.IntegerField(choices=range(1, 11), widget=widgets.RadioSelectHorizontal)
    effort_level_done = models.IntegerField(choices=range(1, 11), widget=widgets.RadioSelectHorizontal)
    bonus = models.IntegerField(choices=range(0, 11), widget=widgets.RadioSelectHorizontal)

    def set_payoffs(self):
        employer = self.get_player_by_role('Employer')
        worker = self.get_player_by_role('Worker')

        employer.payoff = 2 * self.desired_effort_level - self.wage + self.bonus
        worker.payoff = float(self.wage) - Constants.worker_profit_table[self.effort_level_done] - float(self.bonus)

        employer.wage = self.wage
        worker.wage = self.wage
        employer.effort_level = self.desired_effort_level
        worker.effort_level = self.effort_level_done
        employer.bonus = self.bonus
        worker.bonus = self.bonus


class Player(BasePlayer):
    wage = models.IntegerField(min=1, max=10)
    effort_level = models.IntegerField(min=1, max=10)
    bonus = models.IntegerField(min=0, max=10)

    def role(self):
        return 'Employer' if self.id_in_group == 1 else 'Worker'


class Constants(BaseConstants):
    name_in_url = 'principal_agent_relations_3'
    players_per_group = 2
    num_rounds = 4
    instructions_template = 'principal_agent_relations_3/Instructions.html'
    worker_profit_table = {1: 0.01, 2: 0.10, 3: 0.20, 4: 0.40, 5: 0.60, 6: 0.80, 7: 1.00, 8: 1.30, 9: 1.60, 10: 2.00}
