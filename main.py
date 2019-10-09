import sys
import os
sys.stdout = open(os.devnull, 'w')
from MyGame import *
import arcade
from sim import *
from util.constants import * 
from util.inputFunctions import * 
from GENNFunctions import * 
import time
import multiprocessing
from operator import add 
from ctypes import c_int
from operator import itemgetter 
sys.stdout = sys.__stdout__

def runOneGame(a):
    x = Game(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10])
    x.setup()
    val = True
    while val == True:
        val = x.update()
    return val

def main(args):
    """ Main method """

    graphics = 'no'
    evolutions = False
    spacer()

    # conCurrentGame = 100
    # iterations = 999 
    # simulation_player_1 = 'genn'
    # simulation_player_2 = 'fsm'
    # player_2_type = 'mid'
    # graphics = 'no'
    # player_1_type = 'genn'

    conCurrentGame = get_int_choice('How many games would you like played at the same time (Recommended amount based on computer cores '+str(multiprocessing.cpu_count())+"):",1,1000)
    iterations = get_int_choice('Enter the amount of generations to be played: ',1,5000)
    simulation_player_1 = get_str_choice("What type of simulation do you want for player 1?",'fsm','freeplay','dc','genn')
    if simulation_player_1.lower() == "freeplay":
        player_1_type = "human"
        graphics = 'yes'
    elif simulation_player_1.lower() == "fsm":
        player_1_type = get_str_choice("What type of player is player 1 ?",'short','mid','range','pq')
    elif simulation_player_1.lower() == "dc":
        player_1_type = get_str_choice("What type of dynamic controller is player 1 ?",'master','average','random','train')
    elif simulation_player_1.lower() == "genn":
        player_1_type = "genn"
    simulation_player_2 = get_str_choice("What type of simulation do you want for player 2?",'fsm','dc','freeplay','genn')
    if simulation_player_2 == "freeplay":
        player_2_type = "human"
        graphics = 'yes'
    if simulation_player_2 == "fsm":
        player_2_type = get_str_choice("What type of player is player 2?",'short','mid','range','pq')
    elif simulation_player_2.lower() == "dc":
        player_2_type = get_str_choice("What type of dynamic controller is player 2 ?",'master','average','random')
    if graphics == 'no':
        graphics = get_str_choice('Run Graphically?: ','yes','no')

    if player_1_type == 'genn':
        evolutions = True
        player_1_nets = createNets(conCurrentGame)
    else: player_1_nets = None
    if player_2_type == 'genn':
        evolutions = True
        player_2_nets = createNets(conCurrentGame)
    else: player_2_nets = None
    # count = Counter()
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
        shortWins = 0
        midWins = 0
        rangeWins = 0
        draws = 0
        leftOverHealth = 0
        evolutionHealth = []
        for game in range(iterations):
            spacer()
            print("Total iterations %d out of %d" % (game + 1, iterations) )
            if evolutions == True:
                if player_1_type == 'genn':
                    if game % 9 == 0 and game != 0:
                        print(evolutionHealth)
                        bestIndexs = sorted(range(len(evolutionHealth)), key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.2//1):]
                        evolutionHealth = []
                        newNets = list(itemgetter(*bestIndexs)(player_1_nets))
                        temp = createChildNets(newNets,conCurrentGame - len(newNets))
                        player_1_nets = newNets + temp
                        player_1_nets = mutateNets(player_1_nets)
                if player_2_type == 'genn':
                    if game % 9 == 0 and game != 0:
                        bestIndexs = sorted(range(len(evolutionHealth)), key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.2//1):]
                        evolutionHealth = []
                        newNets = list(itemgetter(*bestIndexs)(player_2_nets))
                        temp = createChildNets(newNets,conCurrentGame - len(newNets))
                        player_2_nets = newNets + temp
                        player_2_nets = mutateNets(player_2_nets)

            p = multiprocessing.Pool(multiprocessing.cpu_count())
                # map will always return the results in order, if order is not important in the future use pool.imap_unordered()
            if game % 9 < 3: player_2_type == 'short'
            elif game % 9 < 6: player_2_type == 'mid'
            else: player_2_type == 'range'
            result = p.map(runOneGame,[ x + [i - 1]  for i,x in enumerate([ x for x in [[SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,1,player_1_type,player_2_type,conCurrentGame,game,player_1_nets,player_2_nets]] *conCurrentGame  ],1) ])
            if game == 0 or game % 3 == 0: evolutionHealth = [float(i) for i in result]
            else: evolutionHealth = list(map(add, [float(i) for i in result], evolutionHealth)) 
            player1Wins += sum(int(i) > 0 for i in [int(i) for i in result]) 
            player2Wins += sum(int(i) < 0 for i in [int(i) for i in result])
            if game % 9 < 3: shortWins += sum(int(i) < 0 for i in [int(i) for i in result])
            elif game % 9 < 6: midWins += sum(int(i) < 0 for i in [int(i) for i in result])
            else: rangeWins += sum(int(i) < 0 for i in [int(i) for i in result])
            draws += sum(int(i) == 0 for i in [int(i) for i in result])  
            leftOverHealth += sum([float(i) for i in result])
            p.close()
            p.join()
        if player_1_type == 'genn':
            writeNetworks(player_1_nets)
        if player_2_type == 'genn':
            writeNetworks(player_2_nets)
        print("player 1 (" + player_1_type + "):",player1Wins)
        print("player 2 (" + player_2_type + "):",player2Wins)
        print("\t Short Wins: ",shortWins)
        print("\t mid Wins: ",midWins)
        print("\t range Wins: ",rangeWins)
        print("Draws: ",draws)
        print("Average Health Difference: ",round(abs(leftOverHealth) / (conCurrentGame * iterations),4))
        print("Total Time: ",round(time.time() - start,4))
        
if __name__ == "__main__":
    main(sys.argv)

