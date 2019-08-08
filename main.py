import arcade
import sys
from MyGame import *
#from Game import *
#from SimulatedGame import * 
from sim import *
from util.constants import * 
from util.inputFunctions import * 
import time
import multiprocessing

def runOneGame(a):
    x = Game(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7])
    x.setup()
    val = True
    while val == True:
        val = x.update()
    return val

def main(args):
    """ Main method """

    graphics = 'no'
    # games = int(input('Enter the amount of games to be played: '))
    spacer()
    conCurrentGame = get_int_choice('How many games would you like played at the same time:',1,multiprocessing.cpu_count())
    iterations = get_int_choice('Enter the amount of iterations to be played: ',1,5000)
    simulation_player_1 = get_str_choice("What type of simulation do you want for player 1?",'fsm','freeplay','dc')
    if simulation_player_1.lower() == "freeplay":
        player_1_type = "human"
        graphics = 'yes'
    elif simulation_player_1.lower() == "fsm":
        player_1_type = get_str_choice("What type of player is player 1 ?",'short','mid','range','pq')
    elif simulation_player_1.lower() == "dc":
        player_1_type = get_str_choice("What type of dynamic controller is player 1 ?",'master','average','random','train')
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
        start = time.time()
        player1Wins = 0
        player2Wins = 0
        draws = 0
        for game in range(iterations):
            spacer()
            print("Total iterations %d out of %d" % (game + 1, iterations) )
            p = multiprocessing.Pool(multiprocessing.cpu_count())
            result = p.map(runOneGame,[ x for x in [[SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,1,player_1_type,player_2_type,iterations,game]] * conCurrentGame])
            player1Wins += result.count("player 1")
            player2Wins += result.count("player 2")
            draws += result.count("draw")
            p.close()
            p.join()
        print("player 1 (" + player_1_type + ") :",player1Wins)
        print("player 2 (" + player_2_type + ") :",player2Wins)
        print("Draws: ",draws)
        print("Total Time: ",time.time() - start)
        
        # runOneGame(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,iterations,player_1_type,player_2_type)
        # x = Game(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,iterations,player_1_type,player_2_type)
        # x.setup()
        # val = True
        # while val:
        #     val = x.update()
        
if __name__ == "__main__":
    main(sys.argv)

