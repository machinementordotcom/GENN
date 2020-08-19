
import sys
import os
#sys.stdout = open(os.devnull, 'w')
from MyGame import *
import arcade
from sim import *
from util.constants import * 
from util.inputFunctions import * 
from GENN.GENNFunctions import * 
import time
import multiprocessing
from operator import add 
from ctypes import c_int
from operator import itemgetter 
import pandas as pd
import json
import re 
import matplotlib.ticker as ticker

#sys.stdout = sys.__stdout__

def runOneGame(a):
    move = 0

    x = Game(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11],a[12],a[13])
    x.setup()
    #val = True
    val = x.update(move, 0)
    print("Game Play Started...")

    while True:
        if type(val) is list:
            if val[0] == True:
                val = x.update(move, val[1])

                move += 1
#                if move % 250  == 0:  ## updates are coordinated with sim.py health updates
                    #print("Move", str(move))
#                    None
        else:
            print("Game over")
            return val
def createGraphs(playerNum):
    with open('player' + str(playerNum) + 'Trends.txt') as f:
        z = str(f.readline()).replace("}","").split("{")
    p = []
    for elm in z[1:]:
        use = elm.split(",")
        temp = [ re.sub("\D", "", x) for x  in use ] 
        p.append(temp)
    x = pd.DataFrame(p,columns = ['arrow','fire','knife','towardsOpponent','awayOpponent','movementChanges','biggestTrend'])
    fig, ax = plt.subplots()

    plt.plot(range(len(x)),x['arrow'].astype(float))    
    plt.plot(range(len(x)),x['fire'].astype(float))    
    plt.plot(range(len(x)),x['knife'].astype(float)) 
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))   


    plt.ylabel("Shot Frequency")
    plt.xlabel("Time segment")
    plt.title("Shooting trends per segment for player " + str(playerNum))
    # plt.yticks(range(len(x)))
    plt.legend(['Arrow', 'Fire', 'Knife'], loc='upper left')

    plt.savefig("player" + str(playerNum) + "ShootingTrends")

def main(args):
    """ Main method """

    #Remove the Log File first otherwise it for avoiding merge log data for every run
    if os.path.exists('player_1_log.csv'):
        os.remove('player_1_log.csv')
    else:
        pass

    if os.path.exists('player_2_log.csv'):
        os.remove('player_2_log.csv')
    else:
        pass

    graphics = 'no'
    graphOutput = 'no'
    train = 'yes'
    trendTracking = 'no'
    evolutions = False
    spacer()

    if train == 'yes':
        # Game/Network will be played in the same time per generation
        conCurrentGame = 10
        # Total Generation 
        generations = 10
        simulation_player_1 = 'agenn'
        simulation_player_2 = 'fsm'
        player_2_type = 'short'
        graphics = 'no'
        player_1_type = 'genn'
        trendTracking = 'no'
        graphOutput = 'no'
        games_per_network = 9
        
        print("All the variables set")
    else:
        conCurrentGame = get_int_choice('How many games would you like played at the same time (Recommended amount based on computer cores '+str(multiprocessing.cpu_count())+"):",1,1000)
        generations = get_int_choice('Enter the amount of rounds to be played: ',1,500)
        games_per_network = get_int_choice('Enter the amount of games to play per network: ',1,5000)
        trendTracking = get_str_choice("Would you like to track trends",'yes','no')
        graphOutput = get_str_choice("Would you like to create graphical outputs?",'yes','no')
        simulation_player_1 = get_str_choice("What type of simulation do you want for player 1?",'fsm','freeplay','dc','genn','agenn')
        if simulation_player_1.lower() == "freeplay":
            player_1_type = "human"
            graphics = 'yes'
        elif simulation_player_1.lower() == "fsm":
            player_1_type = get_str_choice("What type of player is player 1 ?",'short','mid','range','pq')
        elif simulation_player_1.lower() == "dc":
            player_1_type = get_str_choice("What type of dynamic controller is player 1 ?",'master','average','random','train')
        elif simulation_player_1.lower() == "genn":
            player_1_type = "genn"
        elif simulation_player_1.lower() == "agenn":
            player_1_type = "agenn"
        simulation_player_2 = get_str_choice("What type of simulation do you want for player 2?",'fsm','dc','freeplay','genn')
        if simulation_player_2 == "freeplay":
            player_2_type = "human"
            graphics = 'yes'
        if simulation_player_2 == "fsm":
            player_2_type = get_str_choice("What type of player is player 2?",'short','mid','range','pq')
        elif simulation_player_2.lower() == "dc":
            player_2_type = get_str_choice("What type of dynamic controller is player 2 ?",'master','average','random')
        elif simulation_player_2.lower() == "genn":
            player_2_type = "genn"
        if graphics == 'no':
            graphics = get_str_choice('Run Graphically?: ','yes','no')

    if (player_1_type == 'genn' or player_1_type == 'agenn') and train == 'yes':
        evolutions = True
        player_1_nets = createNets(conCurrentGame)
    elif (player_1_type == 'genn' or player_1_type == 'agenn') and train == 'no':
        player_1_nets = readNets(conCurrentGame)
    else: player_1_nets = None
    if (player_2_type == 'genn' or player_2_type == 'agenn') and train == 'yes':
        evolutions = True
        player_2_nets = createNets(conCurrentGame)
    elif (player_2_type == 'genn' or player_2_type == 'agenn') and train == 'no':
        player_2_nets = readNets(conCurrentGame)
    else: player_2_nets = None
    if graphics == 'yes':
        window = MyGame(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,generations,player_1_type,player_2_type)
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
        for rounds in range(generations):
            spacer()
            print("Total rounds %d out of %d" % (rounds + 1, generations))
            print("Player1 Nets lenght:", str(len(player_1_nets)))
            print(player_1_nets)
            if evolutions == True and train == 'yes':
                if player_1_type is 'genn' or player_1_type is 'agenn':
                    #if rounds % 9 == 0 and rounds != 0:
                    if rounds != 0:
                        print(evolutionHealth)
                        bestIndexs = sorted(range(len(evolutionHealth)), key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.2//1):]
                        evolutionHealth = []
                        newNets = list(itemgetter(*bestIndexs)(player_1_nets))
                        temp = createChildNets(newNets,conCurrentGame - len(newNets))
                        player_1_nets = newNets + temp
                        player_1_nets = mutateNets(player_1_nets)
                if player_2_type is 'genn' or player_2_type is 'agenn':
                    #if rounds % 9 == 0 and rounds != 0:
                    if rounds != 0:
                        bestIndexs = sorted(range(len(evolutionHealth)), key=lambda i: evolutionHealth[i])[-int(conCurrentGame*.2//1):]
                        evolutionHealth = []
                        newNets = list(itemgetter(*bestIndexs)(player_2_nets))
                        temp = createChildNets(newNets,conCurrentGame - len(newNets))
                        player_2_nets = newNets + temp
                        player_2_nets = mutateNets(player_2_nets)
            p = multiprocessing.Pool(conCurrentGame)
                # map will always return the results in order, if order is not important in the future use pool.imap_unordered()
            """
            if train == 'yes':
                if rounds % 9 < 3: player_2_type = 'short'
                elif rounds % 9 < 6: player_2_type = 'mid'
                else: player_2_type = 'range'
            """
            result = p.map(runOneGame,[ x + [i - 1]  \
                                       for i,x in enumerate([x for x in \
                                                             [[SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,
                                                             games_per_network,player_1_type,player_2_type,
                                                             conCurrentGame,rounds,player_1_nets,
                                                             player_2_nets, trendTracking,
                                                             simulation_player_1,simulation_player_2]] *conCurrentGame  ],1) ])
            
            if rounds == 0 or rounds % 3 == 0: evolutionHealth = [float(i) for i in result]
            else: evolutionHealth = list(map(add, [float(i) for i in result], evolutionHealth)) 
            player1Wins += sum(int(i) > 0 for i in [int(i) for i in result]) 
            player2Wins += sum(int(i) < 0 for i in [int(i) for i in result])
            """
            if train == 'yes':
                if rounds % 9 < 3: shortWins += sum(int(i) < 0 for i in [int(i) for i in result])
                elif rounds % 9 < 6: midWins += sum(int(i) < 0 for i in [int(i) for i in result])
                else: rangeWins += sum(int(i) < 0 for i in [int(i) for i in result])
            """
            draws += sum(int(i) == 0 for i in [int(i) for i in result])  
            leftOverHealth += sum([float(i) for i in result])
            p.close()
            p.join()
        if player_1_type is 'genn' or player_1_type is 'agenn':
            writeNetworks(player_1_nets)
        if player_2_type is 'genn' or player_2_type is 'agenn':
            writeNetworks(player_2_nets)
        print("player 1 (" + player_1_type + "):",player1Wins)
        print("player 2 (" + player_2_type + "):",player2Wins)
        """
        if train == 'yes':
            print("\t Short Wins: ",shortWins)
            print("\t mid Wins: ",midWins)
            print("\t range Wins: ",rangeWins)
        """
        print("Draws: ",draws)
        print("Average Health Difference: ",round(abs(leftOverHealth) / (conCurrentGame * generations),4))
        print("Total Time: ",round(time.time() - start,4))
    if graphOutput =='yes':
        if player_1_type not in ['short','mid','range']:
            createGraphs(1)
        if player_2_type not in ['short','mid','range']:
            createGraphs(2)
      
if __name__ == "__main__":
    main(sys.argv)

