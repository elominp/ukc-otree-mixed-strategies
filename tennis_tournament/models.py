# -*- coding: utf-8 -*-

from otree.api import *


doc = """
"""


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 8:
            matrix = self.get_group_matrix()
            for row in matrix:
                row.reverse()
            self.set_group_matrix(matrix)
        if self.round_number > 8:
            self.group_like_round(8)


class Group(BaseGroup):
    def set_payoffs(self):
        server = self.get_player_by_role('Server')
        receiver = self.get_player_by_role('Receiver')

        stakes_server = Constants.stakes_server_r1 if self.round_number < 8 else Constants.stakes_server_r2
        stakes_receiver = Constants.stakes_receiver_r1 if self.round_number < 8 else Constants.stakes_receiver_r2
        if server.serve_directions is True and receiver.serve_directions is True:
            server.payoff = stakes_server['Left']['Left']
            receiver.payoff = stakes_receiver['Left']['Left']
            server.is_winner = Constants.is_winning_server['Left']['Left']
            receiver.is_winner = Constants.is_winning_receiver['Left']['Left']
        elif server.serve_directions is True and receiver.serve_directions is not True:
            server.payoff = stakes_server['Left']['Right']
            receiver.payoff = stakes_receiver['Left']['Right']
            server.is_winner = Constants.is_winning_server['Left']['Right']
            receiver.is_winner = Constants.is_winning_receiver['Left']['Right']
        elif server.serve_directions is not True and receiver.serve_directions is True:
            server.payoff = stakes_server['Right']['Left']
            receiver.payoff = stakes_receiver['Right']['Left']
            server.is_winner = Constants.is_winning_server['Right']['Left']
            receiver.is_winner = Constants.is_winning_receiver['Right']['Left']
        elif server.serve_directions is not True and receiver.serve_directions is not True:
            server.payoff = stakes_server['Right']['Right']
            receiver.payoff = stakes_receiver['Right']['Right']
            server.is_winner = Constants.is_winning_server['Right']['Right']
            receiver.is_winner = Constants.is_winning_receiver['Right']['Right']
        else:
            raise NameError('Invalid input for payoff')


class Player(BasePlayer):
    serve_directions = models.BooleanField(
        choices=[
            [True, 'Left'],
            [False, 'Right']
        ]
    )
    is_winner = models.BooleanField()

    def role(self):
        return 'Server' if self.id_in_group == 1 else 'Receiver'


class Constants(BaseConstants):
    name_in_url = 'tennis_tournament'
    players_per_group = 2
    num_rounds = 16
    instructions_template = 'tennis_tournament/Instructions.html'
    stakes_server_r1 = {
        'Left': {'Left': Currency(40), 'Right': Currency(80)},
        'Right': {'Left': Currency(60), 'Right': Currency(20)}
    }
    stakes_receiver_r1 = {
        'Left': {'Left': Currency(60), 'Right': Currency(20)},
        'Right': {'Left': Currency(40), 'Right': Currency(80)}
    }
    stakes_server_r2 = {
        'Left': {'Left': Currency(40), 'Right': Currency(80)},
        'Right': {'Left': Currency(60), 'Right': Currency(20)}
    }
    stakes_receiver_r2 = {
        'Left': {'Left': Currency(60), 'Right': Currency(20)},
        'Right': {'Left': Currency(40), 'Right': Currency(80)}
    }
    is_winning_server = {
        'Left': {'Left': False, 'Right': True},
        'Right': {'Left': True, 'Right': False}
    }
    is_winning_receiver = {
        'Left': {'Left': True, 'Right': False},
        'Right': {'Left': False, 'Right': True}
    }
