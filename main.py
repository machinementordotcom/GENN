import arcade
import sys
from MyGame import *
from util.constants import * 


def main(args):
    """ Main method """
    simultaneous_games = int(input('Enter the amount of games to be played: '))
    simulation_player_1 = input("What type of simulation do you want for player 1(fsm)?")
    if simulation_player_1 == "fsm":
            player_1_type = input("What type of player is player 1 (short, mid, or range)?")
    simulation_player_2 = input("What type of simulation do you want for player 2(fsm)?")
    if simulation_player_2 == "fsm":
        player_2_type = input("What type of player is player 2 (short, mid, or range)?")
    window = Game(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,simultaneous_games,player_1_type,player_2_type)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main(sys.argv)

