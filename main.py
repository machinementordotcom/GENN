import arcade
import sys
from MyGame import *
from util.constants import * 


def main(args):
    """ Main method """
    simultaneous_games = int(input('Enter the amount of simultaneous games: '))
    player_1_type = input("What type of player is player 1 (short, mid, or range)?")
    player_2_type = input("What type of player is player 2 (short, mid, or range)?")
    window = Game(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,simultaneous_games,player_1_type,player_2_type)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main(sys.argv)

