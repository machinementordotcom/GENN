import sys
import csv 
import arcade

class GENN(arcade.Sprite):
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
      inputs = [self.center_x,self.center_y,self.opponent.center_x,self.opponent.center_x,self.health,self.opponent.health,self.total_time,self.shield,self.opponent.shield,self.curtime,self.opponent_hitbox_list, opp_proj_1_x, opp_proj_1_y, opp_proj_2_x, opp_proj_2_y, opp_proj_3_x, opp_proj_3_y]



      nn_choices = {
      'nb_neurons': [64, 128, 256, 512, 768, 1024],
      'nb_layers': [1, 2, 3, 4],
      'activation': ['relu', 'elu', 'tanh', 'sigmoid'],
      'optimizer': ['sgd', 'rmsprop', 'adam',  'adagrad',
                    'adadelta', 'adamax', 'nadam']
                    }