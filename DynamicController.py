import arcade
import math
import random
import csv
from util.constants import * 

# weights = (1/3,1/3,1/3)
# long_weight = weights[0]
# mid_weight = weights[1]
# short_weight = weights[2]

class DynamicController(arcade.Sprite):
    def writeWeights(self):
        with open("weightsDynamicController.csv", 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(self.weights)
    def readWeights(self):
        with open('weightsDynamicController.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.weights = [float(i) for i in row]
                #break
    def equipshield(self):
        self.set_texture(1)
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
        
        self.fireball_list.append(fireball)

        hit = HitBox("images/fire.png")
        hit._set_alpha(0)
        hit._set_height(math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2))
        hit._set_width(ARROW_IMAGE_HEIGHT)
        hit.angle = self.angle
        hit.center_x = self.center_x + -math.sin(math.radians(hit.angle)) * hit.height/2
        hit.center_y = self.center_y + math.cos(math.radians(hit.angle)) * hit.height/2
        
        fireball.hit = hit
        self.hitbox_list.append(hit)
    def shortattack(self):
        knife = Knife("images/knife.png",.1)
        knife.center_x = self.center_x
        knife.center_y = self.center_y
        knife.angle = self.angle-180
        self.knife_num += 1 # prevents multiple knifes from being created
        self.knife_list.append(knife)

        hit = HitBox("images/fire.png")
        hit._set_alpha(0)
        hit._set_height(5)
        hit._set_width(ARROW_IMAGE_HEIGHT)
        hit.angle = self.angle
        hit.center_x = self.center_x + -math.sin(math.radians(hit.angle)) * hit.height/2
        hit.center_y = self.center_y + math.cos(math.radians(hit.angle)) * hit.height/2
        
        knife.hit = hit
        self.hitbox_list.append(hit)
    def shootarrow(self):
        arrow = Arrow("images/arrow.png",.1)
        arrow.center_x = self.center_x
        arrow.center_y = self.center_y
        arrow.start_x = self.center_x # for tracking 
        arrow.start_y = self.center_y
        arrow.angle = self.angle-90
        arrow.change_x = -ARROW_SPEED*math.sin(math.radians(self.angle))
        arrow.change_y = ARROW_SPEED*math.cos(math.radians(self.angle))
        self.arrow_list.append(arrow)
        hit = HitBox("images/fire.png")
        hit._set_alpha(0)
        hit._set_height(math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2))
        hit._set_width(ARROW_IMAGE_HEIGHT)
        hit.angle = self.angle
        hit.center_x = self.center_x + -math.sin(math.radians(hit.angle)) * hit.height/2
        hit.center_y = self.center_y + math.cos(math.radians(hit.angle)) * hit.height/2
        arrow.hit = hit
        self.hitbox_list.append(hit)


    def update_weights(self):#health_diff, current_type, long_weight, mid_weight, short_weight, v = 1.1):
        self.writeWeights()
        learning_rate = 0.1
        v = 1.1 * (1 + learning_rate * abs(self.benchmarkDifference/100))
        health_diff = self.health - self.opponent.health
        current_type = self.type
        long_weight = self.weights[0]
        mid_weight = self.weights[1]
        short_weight = self.weights[2]
        if self.benchmarkDifference >= 0:
            if current_type == "range":
                long_weight = v * long_weight
                if long_weight >= 1:
                    long_weight = 0.99
                    mid_weight = 0.005
                    short_weight = 0.005
                else:
                    w = (1 - long_weight) / (mid_weight + short_weight)
                    mid_weight = w * mid_weight
                    short_weight = w * short_weight
            elif current_type == "mid":
                mid_weight = v * mid_weight
                if mid_weight >= 1:
                    mid_weight = 0.99
                    long_weight = 0.005
                    short_weight = 0.005
                else:
                    w = (1 - mid_weight) / (long_weight + short_weight)
                    long_weight = w * long_weight
                    short_weight = w * short_weight
            elif current_type == "short":
                short_weight = v * short_weight
                if short_weight >= 1:
                    short_weight = 0.99
                    mid_weight = 0.005
                    long_weight = 0.005
                else:
                    w = (1 - short_weight) / (mid_weight + long_weight)
                    mid_weight = w * mid_weight
                    long_weight = w * long_weight
        else:
            v = 1/v
            if current_type == "range":
                long_weight = v * long_weight
                if long_weight >= 1:
                    long_weight = 0.99
                    mid_weight = 0.005
                    short_weight = 0.005
                else:
                    w = (1 - long_weight) / (mid_weight + short_weight)
                    mid_weight = w * mid_weight
                    short_weight = w * short_weight
            elif current_type == "mid":
                mid_weight = v * mid_weight
                if mid_weight >= 1:
                    mid_weight = 0.99
                    long_weight = 0.005
                    short_weight = 0.005
                else:
                    w = (1 - mid_weight) / (long_weight + short_weight)
                    long_weight = w * long_weight
                    short_weight = w * short_weight
            elif current_type == "short":
                short_weight = v * short_weight
                if short_weight >= 1:
                    short_weight = 0.99
                    mid_weight = 0.005
                    long_weight = 0.005
                else:
                    w = (1 - short_weight) / (mid_weight + long_weight)
                    mid_weight = w * mid_weight
                    long_weight = w * long_weight
        self.weights[0] = long_weight
        self.weights[1] = mid_weight
        self.weights[2] = short_weight
        self.type = random.choices(population = ["range","mid","short"],weights = self.weights, k = 1)[0]


    def update(self):
        self.curtime += 1
        x_diff = self.opponent.center_x - self.center_x
        y_diff = self.opponent.center_y - self.center_y
        self.angle = math.degrees(math.atan2(y_diff,x_diff))-90
        self.d = math.sqrt(x_diff**2 +y_diff**2)
        long_weight = self.weights[0]
        mid_weight = self.weights[1]
        short_weight = self.weights[2]

            #####################
            #Act as a long Range#
            #####################
        if self.type == "range":
            if len(self.opponent_hitbox_list) > 0:
                if arcade.check_for_collision_with_list(self,self.opponent_hitbox_list):
                    randmove_x = random.choices([1,-1])[0]
                    randmove_y = random.choices([1,-1])[0]
                    x_change = MOVEMENT_SPEED * randmove_x
                    y_change = MOVEMENT_SPEED * randmove_y
                else:
                    y_change = 0
                    x_change = 0
                    if self.opponent.center_x - self.center_x < 0:
                        x_change += MOVEMENT_SPEED
                    else:
                        x_change -= MOVEMENT_SPEED
                    if self.opponent.center_y - self.center_y < 0:
                        y_change += MOVEMENT_SPEED
                    else:
                        y_change -= MOVEMENT_SPEED
            else:
                y_change = 0
                x_change = 0
                if self.opponent.center_x - self.center_x < 0:
                    x_change += MOVEMENT_SPEED
                else:
                    x_change -= MOVEMENT_SPEED
                if self.opponent.center_y - self.center_y < 0:
                    y_change += MOVEMENT_SPEED
                else:
                    y_change -= MOVEMENT_SPEED
            self.center_x += x_change
            self.center_y += y_change
            self.change_x = -math.cos(self.angle)*MOVEMENT_SPEED
            self.change_y = -math.sin(self.angle)*MOVEMENT_SPEED
            if self.curtime >=30:
                self.shootarrow()
                self.curtime = 0
            for arrow in self.arrow_list:
                if arrow.center_x>SCREEN_WIDTH + 10 or arrow.center_y>SCREEN_HEIGHT + 10 or arrow.center_x< -10 or arrow.center_y< -10 :
                    arrow.hit.kill()
                    arrow.kill()
            if self.health <= PLAYER_HEALTH*.5 and self.shield < 1:
                self.equipshield()
        

            ####################
            #Act as a mid Range#
            ####################
        elif self.type == "mid":
            if len(self.opponent_hitbox_list) > 0:
                if arcade.check_for_collision_with_list(self,self.opponent_hitbox_list) and self.health <PLAYER_HEALTH*.7:
                    randmove_x = random.choices([1,-1])[0]
                    randmove_y = random.choices([1,-1])[0]
                    self.center_x += (MOVEMENT_SPEED * MID_SPEED_HANDICAP) * randmove_x
                    self.center_y += (MOVEMENT_SPEED * MID_SPEED_HANDICAP) * randmove_y
                elif abs(y_diff) + abs(x_diff) != 0: 
                    self.change_x = (x_diff)/(abs(y_diff) + abs(x_diff))
                    self.change_y = (y_diff)/(abs(y_diff) + abs(x_diff))
                    if self.d > 240:
                        self.center_x += self.change_x * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                        self.center_y += self.change_y * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                    else:
                        if abs(self.center_x - 0) > 5 and abs(SCREEN_WIDTH - self.center_x) > 5:
                            self.center_x += -self.change_x * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                        else:
                            if self.center_y > SCREEN_HEIGHT/2:
                                self.center_y += (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                            else:
                                self.center_y += -(MOVEMENT_SPEED * MID_SPEED_HANDICAP)

                        if abs(self.center_y - 0) > 5 and abs(SCREEN_HEIGHT - self.center_y) > 5:
                            self.center_y += -self.change_y * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                        else:
                            if self.center_x > SCREEN_WIDTH/2:
                                self.center_x += (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                            else:
                                self.center_x += -(MOVEMENT_SPEED * MID_SPEED_HANDICAP)
            else:
                if abs(y_diff) + abs(x_diff) != 0: 
                    self.change_x = (x_diff)/(abs(y_diff) + abs(x_diff))
                    self.change_y = (y_diff)/(abs(y_diff) + abs(x_diff))
                    if self.d > 240:
                        self.center_x += self.change_x * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                        self.center_y += self.change_y * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                    else:
                        if abs(self.center_x - 0) > 5 and abs(SCREEN_WIDTH - self.center_x) > 5:
                            self.center_x += -self.change_x * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                        else:
                            if self.center_y > SCREEN_HEIGHT/2:
                                self.center_y += (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                            else:
                                self.center_y += -(MOVEMENT_SPEED * MID_SPEED_HANDICAP)

                        if abs(self.center_y - 0) > 5 and abs(SCREEN_HEIGHT - self.center_y) > 5:
                            self.center_y += -self.change_y * (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                        else:
                            if self.center_x > SCREEN_WIDTH/2:
                                self.center_x += (MOVEMENT_SPEED * MID_SPEED_HANDICAP)
                            else:
                                self.center_x += -(MOVEMENT_SPEED * MID_SPEED_HANDICAP)
            if self.curtime >=30:
                if self.d <= 300:
                    self.throwfire()
                self.curtime = 0
            for fireball in self.fireball_list:
                diff_x = fireball.start_x-fireball.center_x
                diff_y = fireball.start_y-fireball.center_y
                fireball_dist = math.sqrt(diff_x**2 + diff_y**2)
                if fireball_dist>200:
                    fireball.kill()
            if self.health <=PLAYER_HEALTH*.5 and self.shield < 1:
                self.equipshield()

            
            ######################
            #Act as a short Range#
            ######################
        else:
            if len(self.opponent_hitbox_list) > 0:
                if arcade.check_for_collision_with_list(self,self.opponent_hitbox_list) and self.health <PLAYER_HEALTH*.45:
                    randmove_x = random.choices([1,-1])[0]
                    randmove_y = random.choices([1,-1])[0]
                    self.center_x += MOVEMENT_SPEED * randmove_x
                    self.center_y += MOVEMENT_SPEED * randmove_y
                else:
                    if x_diff > 0:
                        self.center_x += (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
                    elif x_diff < 0:
                        self.center_x -= (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
                    if y_diff > 0:
                        self.center_y += (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
                    elif y_diff < 0:
                        self.center_y -= (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
            else:
                if x_diff > 0:
                    self.center_x += (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
                elif x_diff < 0:
                    self.center_x -= (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
                if y_diff > 0:
                    self.center_y += (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
                elif y_diff < 0:
                    self.center_y -= (MOVEMENT_SPEED * SHORT_SPEED_HANDICAP)
            self.angle = math.degrees(math.atan2(y_diff,x_diff))-90
            self.change_x = math.cos(self.angle)*MOVEMENT_SPEED
            self.change_y = math.sin(self.angle)*MOVEMENT_SPEED
            self.d = math.sqrt(x_diff**2 +y_diff**2)
            if self.curtime >=30:
                if self.d <= 50:
                    self.shortattack()
                self.curtime = 0
            if self.health <=PLAYER_HEALTH*.5 and self.shield < 1:
                self.equipshield()
            
        
        health_diff = self.health - self.opponent.health
        if self.health + self.opponent.health <= self.totalHealthBenchmark:
            self.benchmarkDifference = health_diff - self.benchmarkDifference
            self.totalHealthBenchmark -= 100
            self.update_weights()
            print(self.weights)













