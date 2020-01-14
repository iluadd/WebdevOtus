from Game import Game

if __name__ == "__main__":
    # make a game
    Game = Game()

    # instance players
    Me = Game.make_player(name='Ilua')
    Ai = Game.make_player(name='monstr', ai=True)

    # Start game
    Game.start()
