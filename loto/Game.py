from random import shuffle

from CardDispenser import CardDispenser
from Config import CARD_RULES, CARDS_PER_PLAYER
from Player import Player, AiPlayer


class Game():
    """
    Class describing game and players

    ...

    Attributes
    ----------
    players : list[Player,..]

    Methods
    -------
    start()
        Setting up the game a run it via Gameloop class

    add_players(*args)
        Adding multiple players to game

    add_player(plr)
        Adding single player to game

    make_player(name=None, ai=False)
        Creating player, ai or not.

    players_iter()
        Players generator

    print_all_players()
        Printing players in a nice way

    """
    def __init__(self):
        self.players = []

    def start(self):
        CD = CardDispenser()
        CD.set_rules(CARD_RULES)
        # TODO get  qtty_for_win

        for plr_i in self.players:
            for crd_i in range(CARDS_PER_PLAYER):
                card = CD.get_proper_card()
                plr_i.add_card(card)

        game_loop = GameLoop(self)
        game_loop.start_loop()

    def add_players(self, *args):
        [self.players.append(pl) for pl in args]

    def add_player(self, plr):
        self.players.append(plr)

    def make_player(self, name=None, ai=False):
        if ai:
            newplayer = AiPlayer(name)
        else:
            newplayer = Player(name)

        self.add_player(newplayer)
        return newplayer

    def players_iter(self):
        return (plr for plr in self.players)

    def print_all_players(self):
        pretty_output = ''
        for plr_i in self.players:
            pretty_output += (f'\t Player # {plr_i.id} : {plr_i.name} \n')

        print(pretty_output)


class GameLoop():
    """
    GameLoop class run a game with player's interactions

    ...

    Attributes
    ----------
    game : Game instance
    stop_loop : boolean
    winner : Player instance

    Methods
    -------
    start_loop()
        Running main loop for the game. It decide when to stop the game

    match_number(number=None)
        Match provided number with Card Cell's values

    player_status()
        Displaing Card status

    check_card_is_closed()
        Checking stop_loop value

    stop_loop_true()
        Callback, which sended to Card in match_number method

    """
    def __init__(self, game):
        self.game = game
        self.stop_loop = False
        self.winner = None

    def start_loop(self):
        print('\n Starting new game !')
        print('__________________________')
        self.game.print_all_players()

        self.player_status()

        numbers_to_show = list(range(1, 90))
        shuffle(numbers_to_show)

        while True:

            # The number is commming !!
            current_num = numbers_to_show.pop()
            # current_num = int(input(f'number {numbers_to_show.pop()} ! '))

            self.match_number(current_num)

            self.player_status()

            if self.check_card_is_closed():

                if self.winner:
                    print(f'{self.winner}\'s card is closed')
                else:
                    print(f'{self.looser}\'s crossed wrong one')

                break

            if current_num == 0:
                print('Ending game')
                break

    def match_number(self, number=None):
        for plr_i in self.game.players_iter():
            plr_i.match_cards(number, self.stop_loop_true)

    def player_status(self):
        for plr_i in self.game.players_iter():
            print(f'{plr_i.name}')
            plr_i.show_cards()

    def check_card_is_closed(self):
        if self.stop_loop:
            return True

    def stop_loop_true(self, winner=None, looser=None):
        if winner:
            self.winner = winner
        elif looser:
            self.looser = looser
        else:
            raise Exception("winner and looser didn't provided")

        self.stop_loop = True
