
import numpy as np
import arcade
import os
import math
import random
import sys
import time
from arcade.arcade_types import Color
from FSMPlayers.RangePlayer import *
from FSMPlayers.MidRangePlayer import *
from FSMPlayers.ShortRangePlayer import *
from FSMPlayers.AllEnemy import *
from FSMPlayers.HumanPlayer import *
from util.inputFunctions import *
from DynamicController.DynamicController import *
from util/constants import *

class Game:
    def __init__(self,width , height, title, iterations, player_1_type, player_2_type):
        """
        Initializer
        """
        super().__init__(width, height, title)
        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.grid = np.zeros(shape = (SCREEN_HEIGHT, SCREEN_WIDTH))
        self.curtime = 0
        
        self.start = time.time()
        self.totalIterations = iterations
        self.iterations = iterations
        self.player1_type = player_1_type.lower()
        self.player2_type = player_2_type.lower()
    
        self.draws = 0

    def setup(self):
        spacer()
        print("Total iterations %d out of %d" % (abs(self.iterations - self.totalIterations) +1, self.totalIterations) )
        self.player_list = []
        self.arrow_list = []
        self.fireball_list = []
        self.knife_list = []

        # Set up the player
        if self.player1_type.lower() == 'range':
            self.player1 = RangePlayer(KNIGHT_IMAGE,1)
        elif self.player1_type.lower() == 'mid':
            self.player1 = MidRangePlayer(KNIGHT_IMAGE,1)
        elif self.player1_type.lower() == 'short':
            self.player1 = ShortRangePlayer(KNIGHT_IMAGE,1)
        elif self.player1_type.lower() == 'master':
            self.player1 = DynamicController(KNIGHT_IMAGE,1)
            self.player1.id = "player1"
            self.player1.adjusting = None
            if self.iterations == self.totalIterations:
                self.player1.adjustingWeight = 0
                self.player1.weights = [[],[]]
                self.player1.readWeights("DynamicController/masterWeights.csv")
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.shootRule = None
                self.player1.moverule = None
                chooseWeight(self.player1)
            else:
                self.player1.adjustingWeight = self.totalIterations - self.iterations
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.weights = [[],[]]
                self.player1.readWeights("DynamicController/masterWeights.csv")
                chooseWeight(self.player1)
        elif self.player1_type.lower() == 'average':
            self.player1 = DynamicController(KNIGHT_IMAGE,1)
            self.player1.id = "player1"
            self.player1.adjusting = 'both'
            if self.iterations == self.totalIterations:
                self.player1.weights = [[],[]]
                self.player1.readWeights("DynamicController/masterWeights.csv")
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.shootRule = None
                self.player1.moverule = None
                chooseWeight(self.player1)
            else:
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.weights = [[],[]]
                self.player1.readWeights()
                chooseWeight(self.player1)
        elif self.player1_type.lower() == 'random':
            self.player1 = DynamicController(KNIGHT_IMAGE,1)
            self.player1.id = "player1"
            self.player1.adjusting = 'both'
            if self.iterations == self.totalIterations:
                shootWeights = [1/21] * 21
                moveWeights = [1/7] * 14 + [1/2] * 6
                self.player1.weights = [shootWeights,moveWeights]
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.shootRule = None
                self.player1.moverule = None
                chooseWeight(self.player1)
            else:
                self.player1.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player1.benchmarkDifference = 0
                self.player1.weights = [[],[]]
                self.player1.readWeights()
                chooseWeight(self.player1)
        else:
            self.player1 = Enemy(KNIGHT_IMAGE,1)

        self.player1.append_texture(arcade.load_texture(KNIGHT_IMAGE))
        self.player1.append_texture(arcade.load_texture(KNIGHT_IMAGE))
        self.player1.center_x = random.randint(10,900)
        self.player1.center_y = random.randint(10,600)
        self.player1.score = 0
        self.player1.health = PLAYER_HEALTH
        self.player1.curtime = 0
        self.player1.total_time = 0
        self.player1.hitbox_list = []
        self.player1.arrow_list = []
        self.player1.fireball_list = []
        self.player1.knife_list = []
        self.player1.knife_num = 0
        self.player1.shield = 0
        self.player1.box = 3

        # Set up bad guy
        if self.player2_type.lower() == 'range':
            self.player2 = RangePlayer(KNIGHT_IMAGE,1)
        elif self.player2_type.lower() == 'mid':
            self.player2 = MidRangePlayer(KNIGHT_IMAGE,1)
        elif self.player2_type.lower() == 'short':
            self.player2 = ShortRangePlayer(KNIGHT_IMAGE,1)
        elif self.player2_type.lower() == 'master':
            self.player2 = DynamicController(KNIGHT_IMAGE,1)
            self.player2.id = "player2"
            self.player2.adjusting = None
            if self.iterations == self.totalIterations:
                self.player2.adjustingWeight = 0
                self.player2.weights = [[],[]]
                self.player2.readWeights("DynamicController/masterWeights.csv")
                self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player2.benchmarkDifference = 0
                self.player2.shootRule = None
                self.player2.moverule = None
                chooseWeight(self.player2)
            else:
                self.player2.adjustingWeight = self.totalIterations - self.iterations
                self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player2.benchmarkDifference = 0
                self.player2.weights = [[],[]]
                self.player2.readWeights("DynamicController/masterWeights.csv")
                chooseWeight(self.player2)
        elif self.player2_type.lower() == 'average':
            self.player2 = DynamicController(KNIGHT_IMAGE,1)
            self.player2.id = "player2"
            self.player2.adjusting = 'both'
            if self.iterations == self.totalIterations:
                self.player2.weights = [[],[]]
                self.player2.readWeights("DynamicController/masterWeights.csv")
                self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player2.benchmarkDifference = 0
                self.player2.shootRule = None
                self.player2.moverule = None
                chooseWeight(self.player2)
            else:
                self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player2.benchmarkDifference = 0
                self.player2.weights = [[],[]]
                self.player2.readWeights()
                chooseWeight(self.player2)
        elif self.player2_type.lower() == 'random':
            self.player2 = DynamicController(KNIGHT_IMAGE,1)
            self.player2.id = "player2"
            self.player2.adjusting = 'both'
            if self.iterations == self.totalIterations:
                self.player2.adjustingWeight = 0
                shootWeights = [1/21] * 21
                moveWeights = [1/7] * 14 + [1/2] * 6
                self.player2.weights = [shootWeights,moveWeights]
                self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player2.benchmarkDifference = 0
                self.player2.shootRule = None
                self.player2.moverule = None
                chooseWeight(self.player2)
            else:
                self.player2.adjustingWeight = self.totalIterations - self.iterations
                self.player2.totalHealthBenchmark = PLAYER_HEALTH * 2 - 100
                self.player2.benchmarkDifference = 0
                self.player2.weights = [[],[]]
                self.player2.readWeights()
                chooseWeight(self.player2)
        else:
            self.player2 = Enemy(KNIGHT_IMAGE,1)

        self.player2.center_x = random.randint(10,900)
        self.player2.opponent = self.player1
        self.player2.center_y = random.randint(10,600)
        self.player2.type = random.choice(["range","mid","short"])
        self.player2.health = PLAYER_HEALTH
        self.player2.score = 0
        self.player2.curtime = 0
        self.player2.total_time = 0
        self.player2.type = self.player2_type.lower()
        self.player2.knife_num = 0
        self.player2.shield = 0
        self.player_list.append(self.player2)
        self.player2.hitbox_list = []
        self.player2.arrow_list = []
        self.player2.fireball_list = []
        self.player2.knife_list = []
        self.player1.opponent_hitbox_list = self.player2.hitbox_list
        self.player2.opponent_hitbox_list = self.player1.hitbox_list
        self.player1.opponent = self.player2
        self.player2.box = 3


    def end_game(self):
        self.player1_score += self.player1.score
        self.player2_score += self.player2.score
        self.iterations -= 1

        if self.iterations == 0:
            print("player 1 (" + self.player1_type + ") :",str(self.player1_score))
            file = open("player1score.txt","w")
            file.write(str(self.player1_score))
            file.close()
            print("player 2 (" + self.player2_type + ") :",str(self.player2_score))
            file = open("player2score.txt","w")
            file.write(str(self.player2_score)) 
            file.close()
            print("Draws :",self.draws)
            print("Total Time: ",time.time() - self.start)
            print('\a')
            raise Exception("End")
            # return False
            # sys.exit()
        self.setup()

    def init_player(self):
        
        self.grid[self.player1.y][self.player1.x] = 1
        self.grid[self.player2.y][self.player2.x] = 1
    
    # There are 2 functions for each so it is easy to not interfere 
    # with each other
    def arrow1(self):
        self.arw = Arrow(self.player1.x,self.player1.y,FIREBALL_SPEED,self.player1.box)
        self.player1.arrow_list.append(self.arw)
        
    def arrow2(self):

        self.arw = Arrow(self.player2.x,self.player2.y,FIREBALL_SPEED,self.player2.box)
        self.player2.arrow_list.append(self.arw)
        
    def fire1(self):

        self.fireball = FireBall(self.player1.x,self.player1.y,ARROW_SPEED,self.player1.box)  
        self.player1.fireball_list.append(self.fireball)
        
    def fire2(self):

        self.fireball = FireBall(self.player2.x,self.player2.y,ARROW_SPEED,self.player2.box)  
        self.player2.fireball_list.append(self.fireball)
    
    def equip_shield1(self):

        self.player1.health += 50
        self.player1.shield += 1
    
    def equip_shield2(self):

        self.player2.health += 50
        self.player2.shield += 1

    def update(self):
        # sets a timer that game and perspective players use
        # not sure if necessary

        self.curtime += 1 
        self.player1.update()
        self.player2.update()
        # player 1 collision
        if self.player1.y >= self.height:
            self.player1.y = self.height
        if self.player1.y <= 0:
            self.player1.y = 0
        if self.player1.x >= self.width:
            self.player1.x = self.width
        if self.player1.x <= 0:
            self.player1.x = 0
        # player 2 collision
        if self.player2.y >= self.height:
            self.player2.y = self.height
        if self.player2.y <= 0:
            self.player2.y = 0
        if self.player2.x >= self.width:
            self.player2.x = self.width
        if self.player2.x <= 0:
            self.player2.x = 0
        
        # all idependent if statements so it doesn't pass other
        # logical statements should one of them be true
        #player 1 movement
        if self.player1.x > self.player2.x:
            self.player1.x -= self.player1.vel
        if self.player1.y > self.player2.y:
            self.player1.y -= self.player1.vel
        if self.player1.x < self.player2.x:
            self.player1.x += self.player1.vel
        if self.player1.y < self.player2.y:
            self.player1.y += self.player1.vel
    
        # player 2 movement
        if self.player2.x > self.player1.x:
            self.player2.x -= self.player2.vel
        if self.player2.y > self.player1.y:
            self.player2.y -= self.player2.vel
        if self.player2.x < self.player1.x:
            self.player2.x += self.player2.vel
        if self.player2.y < self.player1.y:
            self.player2.y += self.player2.vel
        

        # Stop at hit boxes
        # Only needs to be done for one player
        if self.player1.x - self.player1.box <= self.player2.x + self.player2.box:
            self.player1.x = self.player2.x + self.player2.box + self.player1.box
        elif self.player1.x + self.player1.box >= self.player2.x - self.player2.box:
            self.player1.x = self.player2.x - self.player2.box - self.player1.box
        if self.player1.y - self.player1.box <= self.player2.y + self.player2.box:
            self.player1.y = self.player2.y + self.player2.box + self.player1.box
        elif self.player1.y + self.player1.box >= self.player2.y - self.player2.box:
            self.player1.y = self.player2.y - self.player2.box - self.player1.box
        
        # Shields 
        if self.player1.health <= 500 and self.player1.shield <= 1:
            self.equip_shield1()
        if self.player2.health <= 500 and self.player2.shield <= 1:
            self.equip_shield2()

        # fireing
        """
        dist1_x = self.player2.x - self.player1.x
        dist1_y = self.player2.y - self.player1.y
        dist2_x = self.player1.x - self.player2.x
        dist2_y = self.player1.y - self.player2.y
        dist1 = math.sqrt(dist1_x**2 + dist1_y**2)
        dist2 = math.sqrt(dist2_x**2 + dist2_y**2)
        self.player1.angle = math.atan(dist1_x/dist1_y)
        self.player2.angle = math.atan(dist2_x/dist2_y)
        """


        #fireball movement
        for self.fireball in self.player1.fireball_list:
            self.fireball.x += self.fireball.vel*math.cos(self.player1.angle)
            self.fireball.y += self.fireball.vel*math.sin(self.player1.angle)
            #fireball collision
            if self.fireball.x - self.fireball.box <= self.player2.x + self.player2.box:
                self.player2.health -= FIREBALL_DAMAGE
            elif self.fireball.x + self.fireball.box >= self.player2.x - self.player2.box:
                self.player2.health -= FIREBALL_DAMAGE
            elif self.fireball.y + self.fireball.box <= self.player2.y - self.player2.box:
                self.player2.health -= FIREBALL_DAMAGE
            elif self.fireball.y + self.fireball.box >= self.player2.y - self.player2.box:
                self.player2.health -= FIREBALL_DAMAGE
        #fireball movement
        for self.fireball in self.player2.fireball_list:
            self.fireball.x += self.fireball.vel*math.cos(self.player2.angle)
            self.fireball.y += self.fireball.vel*math.sin(self.player2.angle)
            #fireball collision
            if self.fireball.x - self.fireball.box <= self.player1.x + self.player1.box:
                self.player1.health -= FIREBALL_DAMAGE
            elif self.fireball.x + self.fireball.box >= self.player1.x - self.player1.box:
                self.player1.health -= FIREBALL_DAMAGE
            elif self.fireball.y + self.fireball.box <= self.player1.y - self.player1.box:
                self.player1.health -= FIREBALL_DAMAGE
            elif self.fireball.y + self.fireball.box >= self.player1.y - self.player1.box:
                self.player1.health -= FIREBALL_DAMAGE
        # Arrow movement
        for self.arw in self.player1.arrow_list:
            self.arw.x += self.arw.vel*math.cos(self.player1.angle)
            self.arw.y += self.arw.vel*math.sin(self.player1.angle)
            #arw collision
            if self.arw.x - self.arw.box <= self.player2.x + self.player2.box:
                self.player2.health -= ARROW_DAMAGE
            elif self.arw.x + self.arw.box >= self.player2.x - self.player2.box:
                self.player2.health -= ARROW_DAMAGE
            elif self.arw.y + self.arw.box <= self.player2.y - self.player2.box:
                self.player2.health -= ARROW_DAMAGE
            elif self.arw.y + self.arw.box >= self.player2.y - self.player2.box:
                self.player2.health -= ARROW_DAMAGE
        # Arrow movement
        for self.arw in self.player2.arrow_list:
            self.arw.x += self.arw.vel*math.cos(self.player2.angle)
            self.arw.y += self.arw.vel*math.sin(self.player2.angle)
            #arw collision
            if self.arw.x - self.arw.box <= self.player1.x + self.player1.box:
                self.player1.health -= ARROW_DAMAGE
            elif self.arw.x + self.arw.box >= self.player1.x - self.player1.box:
                self.player1.health -= ARROW_DAMAGE
            elif self.arw.y + self.arw.box <= self.player1.y - self.player1.box:
                self.player1.health -= ARROW_DAMAGE
            elif self.arw.y + self.arw.box >= self.player1.y - self.player1.box:
                self.player1.health -= ARROW_DAMAGE
                
        # If health is zero kill them
        if self.player1.health <= 0 and self.player2.health <= 0:
            self.draws += 1
            self.end_game()
        elif self.player2.health <= 0:
            self.player2.kill()
            self.player1.score += 1 
            self.end_game()
            
        elif self.player1.health <= 0:
            self.player1.kill()  
            self.player2.score += 1 
            self.end_game()
        