# -*- coding: utf-8 -*-

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

    def vars_for_template(self):
        return {
            'total_payoff': sum([r.payoff for r in self.player.in_all_rounds()]),
            'player_in_all_rounds': self.player.in_all_rounds()
        }


page_sequence = [
    Offer,
    OfferWaitPage,
    Accept,
    ResultsWaitPage,
    ResultsSummary
]
