from itertools import count
from random import random, randint

from Config import AI_FAULT_PROBABILLITY, AUTO_CROSS


class Player():
    """
    Base Player class

    ...

    Attributes
    ----------
    name : str
    id : int
    cards : list[Card,..]

    Methods
    -------
    add_card(card=None)
        Add card to player

    show_cards()
        Display player's cards

    match_cards(number, cb)
        Player 'strike's out' number, and check if player fail

    """
    newid = count().__next__

    def __init__(self, name):
        self.name = name
        self.id = Player.newid()
        self.cards = []

    def add_card(self, card=None):
        self.cards += [card]

    def show_cards(self):
        for crd_i in self.cards:
            print(crd_i)
            print('\n')

    def match_cards(self, number, cb):

        if AUTO_CROSS:
            crossed_number = number
        else:
            # let player cross a number ..
            crossed_number = int(input(f'number {number} ! '))
        print(f'{self.name} crossed {crossed_number}')

        # check if wrong number
        if crossed_number != number:
            cb(looser=self)

        for crd_i in self.cards:
            crd_i.match_card(crossed_number, cb, self)

    def __repr__(self):
        return f'Player # {self.id}: {self.name}'


class AiPlayer(Player):
    """
    Ai Player class

    ...

    Attributes
    ----------
    name : str

    Methods
    -------
    match_cards(number, cb)
        Ai Player 'strike's out' number, and check if player fail

    """
    def __init__(self, name='Default'):
        name = 'Ai ' + name
        super().__init__(name)

    def match_cards(self, number, cb):

        # let ai player cross a number

        if random() < AI_FAULT_PROBABILLITY:
            # let ai miss
            crossed_number = randint(1, 100)
        else:
            crossed_number = number

        print(f'{self.name} crossed {crossed_number}')

        # check if wrong number
        if crossed_number != number:
            cb(looser=self)

        for crd_i in self.cards:
            crd_i.match_card(crossed_number, cb, self)

    def __repr__(self):
        return 'Ai ' + super().__repr__()
