import arcade
import sys
from MyGame import *
#from Game import *
from SimulatedGame import * 
from util.constants import * 
from util.inputFunctions import * 
import time



def main(args):
    """ Main method """

    graphics = 'no'
    # games = int(input('Enter the amount of games to be played: '))
    spacer()
    iterations = get_int_choice('Enter the amount of iterations to be played: ',1,5000)
    simulation_player_1 = get_str_choice("What type of simulation do you want for player 1?",'fsm','freeplay','dc')
    if simulation_player_1.lower() == "freeplay":
        player_1_type = "human"
        graphics = 'yes'
    elif simulation_player_1.lower() == "fsm":
        player_1_type = get_str_choice("What type of player is player 1 ?",'short','mid','range','pq')
    elif simulation_player_1.lower() == "dc":
        player_1_type = get_str_choice("What type of dynamic controller is player 1 ?",'master','average','random')
    simulation_player_2 = get_str_choice("What type of simulation do you want for player 2?",'fsm','dc','freeplay')
    if simulation_player_2 == "freeplay":
        player_2_type = "human"
        graphics = 'yes'
    if simulation_player_2 == "fsm":
        player_2_type = get_str_choice("What type of player is player 2?",'short','mid','range','pq')
    elif simulation_player_2.lower() == "dc":
        player_2_type = get_str_choice("What type of dynamic controller is player 2 ?",'master','average','random')
    if graphics == 'no':
        graphics = get_str_choice('Run Graphically?: ','yes','no')


    if graphics == 'yes':
        window = MyGame(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,iterations,player_1_type,player_2_type)
        window.setup()
        try:
            arcade.run()
        except:
            pass
    elif graphics == 'no':
        window = SimulatedGame(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,iterations,player_1_type,player_2_type)
        window.setup()
        try:
            while window:
                window.on_draw()
                window.update(1/60)
        except:
            pass

if __name__ == "__main__":
    main(sys.argv)

