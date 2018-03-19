# -*- coding: utf-8 -*-

from statistics import mean
from ._builtin import *
from .models import Constants


class Introduction(Page):
    pass


def get_instructions(round_number):
    if round_number <= Constants.num_rounds_part_1:
        return Constants.instructions_game1
    elif Constants.num_rounds_part_1 < round_number <= Constants.num_rounds_part_2:
        return Constants.instructions_game2
    else:
        return Constants.instructions_game3


class Offer(Page):
    def is_displayed(self):
        return self.player.role() == 'Employer'

    def get_form_fields(self):
        form_fields = ['wage', 'desired_effort_level']
        if Constants.num_rounds_part_1 < self.round_number <= Constants.num_rounds_part_2:
            form_fields.append('fine')
        if self.round_number > Constants.num_rounds_part_2:
            form_fields.append('bonus')
        return form_fields

    def vars_for_template(self):
        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'form_fields': self.get_form_fields(),
            'instructions': get_instructions(self.round_number)
        }

    form_model = 'group'


class OfferWaitPage(WaitPage):
    pass


class Accept(Page):
    def is_displayed(self):
        return self.player.role() == 'Worker'

    def get_form_fields(self):
        form_fields = ['effort_level_done']
        if Constants.num_rounds_part_1 < self.round_number <= Constants.num_rounds_part_2:
            form_fields.append('accepted')
        return form_fields

    def vars_for_template(self):
        additional_variables = {}
        if Constants.num_rounds_part_1 < self.round_number <= Constants.num_rounds_part_2:
            additional_variables['fine'] = self.group.fine
        if self.round_number > Constants.num_rounds_part_2:
            additional_variables['bonus'] = self.group.bonus
        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'form_fields': self.get_form_fields(),
            'instructions': get_instructions(self.round_number),
            'additional_variables': additional_variables
        }

    form_model = 'group'


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class ResultsSummary(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds_part_1 or \
               self.round_number == Constants.num_rounds_part_2 or \
               self.round_number == Constants.num_rounds

    def avg_effort(self, player):
        effort = {}
        for i in range(1, 11):
            effort[i] = []
        for i, p in enumerate(player.in_all_rounds(), 1):
            if (self.round_number == Constants.num_rounds_part_1 and i <= Constants.num_rounds_part_1) or \
                    (self.round_number == Constants.num_rounds_part_2 and
                     Constants.num_rounds_part_1 < i <= Constants.num_rounds_part_2) or \
                    (self.round_number == Constants.num_rounds and i > Constants.num_rounds_part_2):
                effort[p.wage].append(p.effort_level)
        for key, l in effort.items():
            effort[key] = mean(l) if len(l) > 0 else 0
        return effort

    def avg_payoff(self):
        payoff = {}
        for i in range(1, 11):
            payoff[i] = []
        for i, p in enumerate(self.player.in_all_rounds(), 1):
            if (self.round_number == Constants.num_rounds_part_1 and i <= Constants.num_rounds_part_1) or \
                    (self.round_number == Constants.num_rounds_part_2 and
                     Constants.num_rounds_part_1 < i <= Constants.num_rounds_part_2) or \
                    (self.round_number == Constants.num_rounds and i > Constants.num_rounds_part_2):
                payoff[p.wage].append(p.payoff)
        for key, l in payoff.items():
            payoff[key] = float(mean(l)) if len(l) > 0 else 0
        return payoff

    def get_effort(self):
        if self.round_number == Constants.num_rounds_part_1:
            effort = [eff if i <= Constants.num_rounds_part_1 else None for i, eff in
                      enumerate([p.effort_level for p in self.group.get_player_by_role('Worker').in_all_rounds()], 1)]
        elif self.round_number == Constants.num_rounds_part_2:
            effort = [eff if Constants.num_rounds_part_1 < i <= Constants.num_rounds_part_2 else None for i, eff in
                      enumerate([p.effort_level for p in self.group.get_player_by_role('Worker').in_all_rounds()], 1)]
        else:
            effort = [eff if i > Constants.num_rounds_part_2 else None for i, eff in
                      enumerate([p.effort_level for p in self.group.get_player_by_role('Worker').in_all_rounds()], 1)]
        return list(filter(None.__ne__, effort))

    def vars_for_template(self):
        return {
            'total_payoff': sum([r.payoff for r in self.player.in_all_rounds()]),
            'player_in_all_rounds': self.player.in_all_rounds(),
            'avg_effort': self.avg_effort(self.group.get_player_by_role('Worker')),
            'avg_payoff': self.avg_payoff(),
            'effort': self.get_effort(),
            'rounds': list(range(1, len(self.player.in_all_rounds()) + 1))
        }


class EndResultsSummary(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def avg_effort(self, player):
        effort = {}
        for i in range(1, 11):
            effort[i] = []
        for p in player.in_all_rounds():
            effort[p.wage].append(p.effort_level)
        for key, l in effort.items():
            effort[key] = mean(l) if len(l) > 0 else 0
        return effort

    def avg_payoff(self):
        payoff = {}
        for i in range(1, 11):
            payoff[i] = []
        for p in self.player.in_all_rounds():
            payoff[p.wage].append(p.payoff)
        for key, l in payoff.items():
            payoff[key] = float(mean(l)) if len(l) > 0 else 0
        return payoff

    def vars_for_template(self):
        return {
            'total_payoff': sum([r.payoff for r in self.player.in_all_rounds()]),
            'player_in_all_rounds': self.player.in_all_rounds(),
            'avg_effort': self.avg_effort(self.group.get_player_by_role('Worker')),
            'avg_payoff': self.avg_payoff(),
            'effort_game1': [eff if i <= Constants.num_rounds_part_1 else None for i, eff in
                             enumerate([p.effort_level for p in
                                        self.group.get_player_by_role('Worker').in_all_rounds()], 1)],
            'effort_game2': [eff if Constants.num_rounds_part_1 < i <= Constants.num_rounds_part_2 else None
                             for i, eff in enumerate([p.effort_level for p in
                                                      self.group.get_player_by_role('Worker').in_all_rounds()], 1)],
            'effort_game3': [eff if i > Constants.num_rounds_part_2 else None for i, eff in
                             enumerate([p.effort_level for p in
                                        self.group.get_player_by_role('Worker').in_all_rounds()], 1)],
            'rounds': list(range(1, len(self.player.in_all_rounds()) + 1))
        }


page_sequence = [
    Offer,
    OfferWaitPage,
    Accept,
    ResultsWaitPage,
    ResultsSummary,
    EndResultsSummary
]
