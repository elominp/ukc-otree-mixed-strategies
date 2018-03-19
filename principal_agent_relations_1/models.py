# -*- coding: utf-8 -*-

from otree.api import *
from random import random


doc = """
"""


class Subsession(BaseSubsession):
    pass


def set_payoffs_1(self):
    employer = self.get_player_by_role('Employer')
    worker = self.get_player_by_role('Worker')

    employer.payoff = 2 * self.desired_effort_level - self.wage
    worker.payoff = float(self.wage) - Constants.worker_profit_table[self.effort_level_done]

    employer.wage = self.wage
    worker.wage = self.wage
    employer.effort_level = self.desired_effort_level
    worker.effort_level = self.effort_level_done


def set_payoffs_2(self):
    employer = self.get_player_by_role('Employer')
    worker = self.get_player_by_role('Worker')

    if self.accepted is False:
        employer.payoff = 0
        worker.payoff = 0
    else:
        fine = True if random() >= 0.5 else False
        if self.effort_level_done >= self.desired_effort_level or fine is False:
            employer.payoff = 2 * self.desired_effort_level - self.wage
            worker.payoff = float(self.wage) - Constants.worker_profit_table[self.effort_level_done]
        else:
            employer.payoff = 2 * self.desired_effort_level - self.wage + self.fine
            worker.payoff = float(self.wage) - Constants.worker_profit_table[self.effort_level_done] - \
                            float(self.fine)

    employer.wage = self.wage
    worker.wage = self.wage
    employer.effort_level = self.desired_effort_level
    worker.effort_level = self.effort_level_done
    employer.fine = self.fine
    worker.fine = self.fine
    employer.accepted = self.accepted
    worker.accepted = self.accepted


def set_payoffs_3(self):
    employer = self.get_player_by_role('Employer')
    worker = self.get_player_by_role('Worker')

    employer.payoff = 2 * self.desired_effort_level - self.wage
    worker.payoff = float(self.wage) - Constants.worker_profit_table[self.effort_level_done]
    if self.bonus_given is True:
        employer.payoff -= self.bonus
        worker.payoff += float(self.bonus)

    employer.wage = self.wage
    worker.wage = self.wage
    employer.effort_level = self.desired_effort_level
    worker.effort_level = self.effort_level_done
    employer.bonus = self.bonus
    worker.bonus = self.bonus


set_payoffs_fcts = [set_payoffs_1, set_payoffs_2, set_payoffs_3]


class Group(BaseGroup):
    wage = models.IntegerField(choices=range(1, 11), widget=widgets.RadioSelectHorizontal)
    desired_effort_level = models.IntegerField(choices=range(1, 11), widget=widgets.RadioSelectHorizontal)
    effort_level_done = models.IntegerField(choices=range(1, 11), widget=widgets.RadioSelectHorizontal)
    fine = models.IntegerField(choices=range(0, 11), widget=widgets.RadioSelectHorizontal)
    accepted = models.BooleanField(widget=widgets.RadioSelectHorizontal, choices=[[True, 'Yes'], [False, 'No']])
    bonus = models.IntegerField(choices=range(0, 11), widget=widgets.RadioSelectHorizontal)
    bonus_given = models.BooleanField(widget=widgets.RadioSelectHorizontal, choices=[[True, 'Yes'], [False, 'No']])

    def set_payoffs(self):
        if self.round_number <= Constants.num_rounds_part_1:
            set_payoffs_fcts[0](self)
        elif self.round_number <= Constants.num_rounds_part_2:
            set_payoffs_fcts[1](self)
        else:
            set_payoffs_fcts[2](self)


class Player(BasePlayer):
    wage = models.IntegerField(min=1, max=10)
    effort_level = models.IntegerField(min=1, max=10)
    fine = models.IntegerField(min=0, max=10)
    accepted = models.BooleanField(choices=[
        [True, 'Yes'],
        [False, 'No']
    ])
    bonus = models.IntegerField(min=0, max=10)

    def role(self):
        return 'Employer' if self.id_in_group == 1 else 'Worker'


class Constants(BaseConstants):
    name_in_url = 'principal_agent_relations_1'
    players_per_group = 2
    num_rounds = 12
    num_rounds_part_1 = int(num_rounds / 2)
    num_rounds_part_2 = num_rounds_part_1 + int(num_rounds / 4)
    instructions_template = 'principal_agent_relations_1/Instructions.html'
    worker_profit_table = {1: 0.01, 2: 0.10, 3: 0.20, 4: 0.40, 5: 0.60, 6: 0.80, 7: 1.00, 8: 1.30, 9: 1.60, 10: 2.00}
    instructions_game1 = """
        <p><b>Game 1</b>: If you are an <b>employer</b> then you choose a <b>wage = w</b> and a <b>desired effort level = 
        de</b>. The wage can be any number between 1 and 10 and desired effort level can be any number between 1 and 10.
        If you are a <b>worker</b> then you will see the wage and desired effort level chosen by the employer and then
        choose yourself an <b>effort level = e</b> which can be any number between 1 and 10.</b></p>
    """
    instructions_game2 = """
        <p><b>Game 2</b>: This is the same as game 1 with the following exceptions:</p>
        
        <p>If you are an employer then you also choose a <b>fine = F</b> (as wel as a wage and a desired effort level).
        The fine can be any number between 0 and 10.</p>
        
        <p>If you are a worker then you can either <b>reject or accept the employer's offer</b>. If the employer's offer
        is rejected then both worker and employer will get a profit of 0.</p>
        
        <p>If the employer's offer is accepted and the worker chooses an <b>effort level equal or above the desired
        effort level, e >= de</b>, then payoffs are as in game1.</p>
        
        <p>If the employer's offer is accepted and the worker chooses an <b>effort level below the desired effort level,
        e < de</b>, then <b>chance will decide whether the worker gets fined</b>. With a 50% chance profits will be as
        in game 1. With 50% chance the worker will be fined by the amount F.</p>
    """
    instructions_game3 = """
        <p><b>Game 3</b>: This is the same as game 1 with the following exceptions:</p>
        
        <p>If you are an employer then when choosing a wage and desired effort level you also choose a <b>bonus = B</b>.
        The bonus can be any number between 0 and 10.</p>
        
        <p>Once the worker has chosen his level of effort the employer will be told the level of effort and then have
        the possibility to give the bonus to the worker.</p>
    """

