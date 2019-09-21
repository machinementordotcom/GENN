import sys
import csv 
import arcade
import numpy as np
from util.constants import *
class GENN(arcade.Sprite):
    def shootarrow(self):
      arrow = Arrow("images/arrow.png",.1)
      arrow.center_x = self.center_x
      arrow.center_y = self.center_y
      arrow.start_x = self.center_x # for tracking 
      arrow.start_y = self.center_y
      arrow.angle = self.angle-90
      arrow.change_x = -ARROW_SPEED*math.sin(math.radians(self.angle))
      arrow.change_y = ARROW_SPEED*math.cos(math.radians(self.angle))
      arrow.vel = ARROW_SPEED
      arrow.box = BOX

      self.arrow_list.append(arrow)

      hit = HitBox("images/fire.png")
      hit._set_alpha(0)
      hit._set_height(math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2))
      hit._set_width(ARROW_IMAGE_HEIGHT)
      hit.angle = self.angle
      hit.center_x = self.center_x + -math.sin(math.radians(hit.angle)) * hit.height/2
      hit.center_y = self.center_y + math.cos(math.radians(hit.angle)) * hit.height/2
      hit.vel = ARROW_SPEED
      hit.box = BOX
      arrow.hit = hit
      self.hitbox_list.append(hit)
    def equipshield(self):
      self.health += PLAYER_HEALTH*.5
      self.shield +=1
    def throwfire(self):
      fireball = Fireball("images/fire.png", .1)
      fireball.center_x = self.center_x
      fireball.center_y = self.center_y
      fireball.start_x = self.center_x # for tracking 
      fireball.start_y = self.center_y # fireball distance
      fireball.angle = self.angle-90
      fireball.change_x = -ARROW_SPEED*math.sin(math.radians(self.angle))
      fireball.change_y = ARROW_SPEED*math.cos(math.radians(self.angle))
      fireball.vel = ARROW_SPEED
      fireball.box = BOX
      self.fireball_list.append(fireball)

      hit = HitBox("images/fire.png")
      hit._set_alpha(0)
      hit._set_height(math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2))
      hit._set_width(ARROW_IMAGE_HEIGHT)
      hit.angle = self.angle
      hit.center_x = self.center_x + -math.sin(math.radians(hit.angle)) * hit.height/2
      hit.center_y = self.center_y + math.cos(math.radians(hit.angle)) * hit.height/2
      hit.vel = ARROW_SPEED
      hit.box = BOX

      fireball.hit = hit
      self.hitbox_list.append(hit)

    def shortattack(self):
      knife = Knife("images/knife.png",.1)
      knife.center_x = self.center_x
      knife.center_y = self.center_y
      knife.angle = self.angle-180
      knife.box = BOX 
      self.knife_num += 1 # prevents multiple knifes from being created
      self.knife_list.append(knife)
      # self.hitbox_list.append(hit)

    def writeWeights(self):
      with open("GENN/weightsDynamicController" + self.id + "-" + str(self.conCurrentGameId) + ".csv", 'w') as myfile:
         wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
         for i in range(2):
            wr.writerow(self.weights[i])
    def readWeights(self,path = None):
     tempWeights = [[],[]] 
     if path == None:
         for i in range(self.conGames):
            with open('GENN/weightsDynamicController' + self.id + "-" + str(self.conCurrentGameId) + '.csv') as csvfile:
                 reader = csv.reader(csvfile)
                 weightType = 0
                 for row in reader:
                     tempWeights[weightType].append([float(i) for i in row])
                     weightType +=1
         self.weights[0] = np.average(np.array(tempWeights[0]),axis = 0).tolist()
         self.weights[1] = np.average(np.array(tempWeights[1]),axis = 0).tolist()
     else:
         with open(path) as csvfile:
            reader = csv.reader(csvfile)
            weightType = 0
            for row in reader:
               self.weights[weightType] = [float(i) for i in row]
               weightType +=1
    def update(self):
      if len(self.opponent_hitbox_list) >= 3:
        opp_proj_1_x = self.opponent_hitbox_list[0].center_x
        opp_proj_1_y = self.opponent_hitbox_list[0].center_y
        opp_proj_2_x = self.opponent_hitbox_list[1].center_x
        opp_proj_2_y = self.opponent_hitbox_list[1].center_y
        opp_proj_3_x = self.opponent_hitbox_list[2].center_x
        opp_proj_3_y = self.opponent_hitbox_list[2].center_y
      elif len(self.opponent_hitbox_list) == 2:
        opp_proj_1_x = self.opponent_hitbox_list[0].center_x
        opp_proj_1_y = self.opponent_hitbox_list[0].center_y
        opp_proj_2_x = self.opponent_hitbox_list[1].center_x
        opp_proj_2_y = self.opponent_hitbox_list[1].center_y
        opp_proj_3_x = 0
        opp_proj_3_y = 0
      elif len(self.opponent_hitbox_list) == 1:
        opp_proj_1_x = self.opponent_hitbox_list[0].center_x
        opp_proj_1_y = self.opponent_hitbox_list[0].center_y
        opp_proj_2_x = 0
        opp_proj_2_y = 0
        opp_proj_3_x = 0
        opp_proj_3_y = 0
      else:
        opp_proj_1_x = 0
        opp_proj_1_y = 0
        opp_proj_2_x = 0
        opp_proj_2_y = 0
        opp_proj_3_x = 0
        opp_proj_3_y = 0
      inputs = [[self.center_x,self.center_y,self.opponent.center_x,self.opponent.center_x,self.health,self.opponent.health,self.total_time,self.shield,self.opponent.shield,self.curtime,len(self.opponent_hitbox_list), opp_proj_1_x, opp_proj_1_y, opp_proj_2_x, opp_proj_2_y, opp_proj_3_x, opp_proj_3_y]]
      # temp =  self.net.createNetwork()
      # for layer in temp.layers:
      #   print(layer.output_shape)
      # print(np.asarray([inputs]),np.asarray([inputs]).shape)
      # print(np.random.randint(250,size =(1,17)),np.random.randint(250,size =(1,17)).shape)
      choices = self.model.predict(np.asarray(inputs))
      # print(self.health)

      self.center_x += choices[0][0][0]
      self.center_y += choices[1][0][0]

      if self.center_y >= SCREEN_HEIGHT:
          self.center_y = SCREEN_HEIGHT
      if self.center_y <= 0:
          self.center_y = 0
      if self.center_x >= SCREEN_WIDTH:
          self.center_x = SCREEN_WIDTH
      if self.center_x <= 0:
          self.center_x = 0

      if self.curtime >=30:
        if choices[2][0][0] > choices[3][0][0] and choices[2][0][0] > choices[4][0][0]:
          self.shootarrow()
        elif choices[3][0][0] > choices[4][0][0]:
          self.throwfire()
        else:
          self.shortattack()
        self.curtime = 0


      nn_choices = {
      'nb_neurons': [64, 128, 256, 512, 768, 1024],
      'nb_layers': [1, 2, 3, 4],
      'activation': ['relu', 'elu', 'tanh', 'sigmoid'],
      'optimizer': ['sgd', 'rmsprop', 'adam',  'adagrad',
                    'adadelta', 'adamax', 'nadam']
                    }