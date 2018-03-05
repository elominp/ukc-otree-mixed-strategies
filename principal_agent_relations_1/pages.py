# -*- coding: utf-8 -*-

from statistics import mean
from ._builtin import *
from .models import Constants


class Introduction(Page):
    pass


class Offer(Page):
    def is_displayed(self):
        return self.player.role() == 'Employer'

    def vars_for_template(self):
        return {
            'player_in_previous_rounds': self.player.in_previous_rounds()
        }

    form_model = 'group'
    form_fields = ['wage', 'desired_effort_level']


class OfferWaitPage(WaitPage):
    pass


class Accept(Page):
    def is_displayed(self):
        return self.player.role() == 'Worker'

    def vars_for_template(self):
        return {
            'player_in_previous_rounds': self.player.in_previous_rounds()
        }

    form_model = 'group'
    form_fields = ['effort_level_done']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class ResultsSummary(Page):
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
            'effort': [p.effort_level for p in self.group.get_player_by_role('Worker').in_all_rounds()],
            'rounds': list(range(1, len(self.player.in_all_rounds()) + 1))
        }


page_sequence = [
    Offer,
    OfferWaitPage,
    Accept,
    ResultsWaitPage,
    ResultsSummary
]
