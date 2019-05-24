import arcade
import os
import math
import random
import time
import sys
import collections
import heapq

from numbers import Number
from typing import Callable
from typing import Union
from arcade.arcade_types import Color
from pynput.keyboard import Key, Controller


SPRITE_SCALING = 0.5

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Adaptive AI"




MOVEMENT_SPEED = 5
ARROW_SPEED = 20
ANGLE_SPEED = 4
#variables for making walls for arcade viewing and a* algo
VERT_WALL_START=1
VERT_WALL_END=1
VERT_CENTER = 465 # X value
HOR_WALL_START=1
HOR_WALL_END=1
HOR_CENTER = 200 # y value

ARROW_DAMAGE = 10
FIREBALL_DAMAGE = 20
KNIFE_DAMAGE = 25


class Arrow(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
class Fireball(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
class Knife(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

class RangePlayer(arcade.Sprite):
    def equipshield(self):
        self.set_texture(1)
        self.health += 50
        self.shield +=1
    def shootarrow(self):
        arrow = Arrow("images/arrow.png",.1)
        arrow.center_x = self.center_x
        arrow.center_y = self.center_y
        arrow.angle = self.angle-90
        arrow.change_x = -ARROW_SPEED*math.sin(math.radians(self.angle))
        arrow.change_y = ARROW_SPEED*math.cos(math.radians(self.angle))
        self.arrow_list.append(arrow)
    def update(self):
        self.curtime += 1
        x_diff = self.opponent.center_x - self.center_x
        y_diff = self.opponent.center_y - self.center_y
        self.d = math.sqrt(x_diff**2 +y_diff**2)
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
        self.angle = math.degrees(math.atan2(y_diff,x_diff))-90
        self.change_x = -math.cos(self.angle)*MOVEMENT_SPEED
        self.change_y = -math.sin(self.angle)*MOVEMENT_SPEED
        self.d = math.sqrt(x_diff**2 +y_diff**2)
        if self.curtime >=20:
            self.shootarrow()
            self.curtime = 0
        if self.health <=50 and self.shield <= 1:
            self.equipshield()

class midRangePlayer(arcade.Sprite):
    def equipshield(self):
        self.set_texture(1)
        self.health += 50
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
    def update(self):
        self.curtime += 1
        x_diff = self.opponent.center_x - self.center_x
        y_diff = self.opponent.center_y - self.center_y
        self.angle = math.degrees(math.atan2(y_diff,x_diff))-90
        self.d = math.sqrt(x_diff**2 +y_diff**2)

        if abs(y_diff) + abs(x_diff) != 0: 
            self.change_x = abs(x_diff)/(abs(y_diff) + abs(x_diff))
            self.change_y = abs(y_diff)/(abs(y_diff) + abs(x_diff))
            if self.d > 250:
                self.center_x += self.change_x * MOVEMENT_SPEED
                self.center_y += self.change_y * MOVEMENT_SPEED
            else:
                if abs(self.center_x - 0) > 5 and abs(SCREEN_WIDTH - self.center_x) > 5:
                    self.center_x += -self.change_x * MOVEMENT_SPEED
                else:
                    if self.center_y > SCREEN_HEIGHT/2:
                        self.center_y += MOVEMENT_SPEED
                    else:
                        self.center_y += -MOVEMENT_SPEED

                if abs(self.center_y - 0) > 5 and abs(SCREEN_HEIGHT - self.center_y) > 5:
                    self.center_y += -self.change_y * MOVEMENT_SPEED
                else:
                    if self.center_x > SCREEN_WIDTH/2:
                        self.center_x += MOVEMENT_SPEED
                    else:
                        self.center_x += -MOVEMENT_SPEED
        
        
        if self.curtime >=30:
            if self.d <= 250:
                pass
                self.throwfire()
            self.curtime = 0

        for fireball in self.fireball_list:
            diff_x = fireball.start_x-fireball.center_x
            diff_y = fireball.start_y-fireball.center_y
            fireball_dist = math.sqrt(diff_x**2 + diff_y**2)
            if fireball_dist>200:
                fireball.kill()
        if self.health <=50 and self.shield <= 1:
            self.equipshield()
class shortRangePlayer(arcade.Sprite):
    def equipshield(self):
        self.set_texture(1)
        self.health += 50
        self.shield +=1
    def shortattack(self):
        knife = Knife("images/knife.png",.1)
        knife.center_x = self.center_x
        knife.center_y = self.center_y
        knife.angle = self.angle-180
        self.knife_num += 1 # prevents multiple knifes from being created
        self.knife_list.append(knife)
    def update(self):
        self.curtime += 1
        x_diff = self.opponent.center_x - self.center_x
        y_diff = self.opponent.center_y - self.center_y
        shortRangeSpeedHandicap = 0.8
        if x_diff > 0:
            self.center_x += (MOVEMENT_SPEED * shortRangeSpeedHandicap)
        elif x_diff < 0:
            self.center_x -= (MOVEMENT_SPEED * shortRangeSpeedHandicap)
        if y_diff > 0:
            self.center_y += (MOVEMENT_SPEED * shortRangeSpeedHandicap)
        elif y_diff < 0:
            self.center_y -= (MOVEMENT_SPEED * shortRangeSpeedHandicap)
        self.angle = math.degrees(math.atan2(y_diff,x_diff))-90
        self.change_x = math.cos(self.angle)*MOVEMENT_SPEED
        self.change_y = math.sin(self.angle)*MOVEMENT_SPEED
        self.d = math.sqrt(x_diff**2 +y_diff**2)
        if self.curtime >=30:
            if self.d <= 50:
                self.shortattack()
            self.curtime = 0
        if self.health <=50 and self.shield <= 1:
            self.equipshield()

class Enemy(arcade.Sprite):
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
    def shootarrow(self):
        arrow = Arrow("images/arrow.png",.1)
        arrow.center_x = self.center_x
        arrow.center_y = self.center_y
        arrow.angle = self.angle-90
        arrow.change_x = -ARROW_SPEED*math.sin(math.radians(self.angle))
        arrow.change_y = ARROW_SPEED*math.cos(math.radians(self.angle))
        self.arrow_list.append(arrow)
    def equipshield(self):
        self.set_texture(1)
        self.health += 50
        self.shield +=1
    def shortattack(self):
        knife = Knife("images/knife.png",.1)
        knife.center_x = self.center_x
        knife.center_y = self.center_y
        knife.angle = self.angle-180
        self.knife_num += 1 # prevents multiple knifes from being created
        self.knife_list.append(knife)
    def update(self):
        self.curtime += 1 
        x_diff = self.opponent.center_x - self.center_x
        y_diff = self.opponent.center_y - self.center_y
        self.angle = math.degrees(math.atan2(y_diff,x_diff))-90
        self.change_x = math.cos(self.angle)*MOVEMENT_SPEED
        self.change_y = math.sin(self.angle)*MOVEMENT_SPEED
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        self.d = math.sqrt(x_diff**2 +y_diff**2)
        if self.curtime >=30:
            if self.d <= 400:
                
                self.throwfire()
            
            elif self.d <=250 and self.knife_num == 0:
                
                self.shortattack()
            else:
            
                self.shootarrow()
            
            self.curtime = 0
        if self.health <=50 and self.shield <= 1:
            self.equipshield()

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title,simultaneous_games):
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
        
        self.simultaneous_games = simultaneous_games

        # Sprite lists
        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.arrow_list = None
        self.fireball_list = None

        
        # Set up the player
        self.enemy_sprite = None
        self.player_sprite = None
        self.physics_engine = None
        self.player1_score = 0
        self.player2_score = 0

        

    def end_game(self):
        self.player1_score += self.player_sprite.score
        self.player2_score += self.enemy.score
        self.simultaneous_games -= 1
        if self.simultaneous_games == 0:
            file = open("player1score.txt","w")
            file.write(str(self.player1_score))
            file.close()
            file = open("player2score.txt","w")
            file.write(str(self.player2_score)) 
            file.close()
            sys.exit()
        self.setup()
    def setup(self):
        """ Set up the game and initialize the variables. """
        # inputs for testing
        #player1_type = input("Give player type\nbalanced,short,long, defensive, neural net: ")
        #player2_type = input("Give player type\nbalanced,short,long, defensive, neural net: ")
        #simultaneous_games = int(input("How many simultaneous games?: "))
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.arrow_list = arcade.SpriteList()
        self.fireball_list = arcade.SpriteList()
        self.knife_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = RangePlayer('images/mage.png')#arcade.Sprite("images/mage.png",SPRITE_SCALING)
        self.player_sprite.append_texture(arcade.load_texture("images/a_shield_round.png"))
        self.player_sprite.center_x = random.randint(10,900)
        self.player_sprite.center_y = random.randint(10,600)
        self.player_sprite.score = 0
        self.player_sprite.health = 100
        self.player_sprite.curtime = 0
        self.player_sprite.arrow_list = arcade.SpriteList()
        self.player_sprite.fireball_list = arcade.SpriteList()
        self.player_sprite.knife_list = arcade.SpriteList()
        self.player_sprite.knife_num = 0
        self.player_sprite.shield = 0

        # Set up bad guy
        self.enemy = RangePlayer('images/lilknight.png',1)
        self.enemy.append_texture(arcade.load_texture('images/a_shield_round.png'))
        self.enemy.append_texture(arcade.load_texture('images/knife.png'))
        self.enemy.center_x = random.randint(10,900)
        self.enemy.opponent = self.player_sprite
        self.enemy.center_y = random.randint(10,600)
        self.enemy.health = 100
        self.enemy.score = 0
        self.enemy.curtime = 0
        self.enemy.knife_num = 0
        self.enemy.shield = 0
        self.player_list.append(self.enemy)
        self.enemy.arrow_list = arcade.SpriteList()
        self.enemy.fireball_list = arcade.SpriteList()
        self.enemy.knife_list = arcade.SpriteList()
        self.player_sprite.opponent = self.enemy
        self.player_list.append(self.player_sprite)


        
        """
        This is unneccessary if we are just doing an arena style for now
        # -- Set up the walls
        # Create a row of boxes
        for x in range(173, 650, 64):
            wall = arcade.Sprite("images/bricks.png", .3)
            wall.center_x = x
            wall.center_y = 200
            self.wall_list.append(wall)

        # Create a column of boxes
        for y in range(273, 500, 64):
            wall = arcade.Sprite("images/bricks.png", .3)
            wall.center_x = 465
            wall.center_y = y
            
            self.wall_list.append(wall)
        for wall in self.wall_list:
            points = wall.get_points()
            print("centerx: ",wall.center_x)
            print("centery: ",wall.center_y)
            print("points", points[0:4])
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        self.player1cont=AStar(1000,700,self.wall_list,(self.player_sprite.center_x,self.player_sprite.center_y),(self.enemy.center_x,self.enemy.center_y))
        """
        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)
    # # Long attack
    # def shootarrow(self):
    #     arrow = Arrow("images/arrow.png",.1)
    #     arrow.center_x = self.player_sprite.center_x
    #     arrow.center_y = self.player_sprite.center_y
    #     arrow.angle = self.player_sprite.angle-90
    #     arrow.change_x = -ARROW_SPEED*math.sin(math.radians(self.player_sprite.angle))
    #     arrow.change_y = ARROW_SPEED*math.cos(math.radians(self.player_sprite.angle))
    #     self.arrow_list.append(arrow)
    # # Shorter attack
    # def throwfire(self):
    #     fireball = Fireball("images/fire.png", .1)
    #     fireball.center_x = self.player_sprite.center_x
    #     fireball.center_y = self.player_sprite.center_y
    #     fireball.start_x = self.player_sprite.center_x # for tracking 
    #     fireball.start_y = self.player_sprite.center_y # fireball distance
    #     fireball.angle = self.player_sprite.angle-90
    #     fireball.change_x = -ARROW_SPEED*math.sin(math.radians(self.player_sprite.angle))
    #     fireball.change_y = ARROW_SPEED*math.cos(math.radians(self.player_sprite.angle))
        
    #     self.fireball_list.append(fireball)
    # def equipshield(self):
    #     self.player_sprite.set_texture(1)
    #     self.player_sprite.health += 50
    #     self.player_sprite.shield +=1

    # def shortattack(self):
    #     knife = Knife("images/knife.png",.1)
    #     knife.center_x = self.player_sprite.center_x+20
    #     knife.center_y = self.player_sprite.center_y+20
    #     knife.angle = self.player_sprite.angle+180
    #     self.player_sprite.knife_num += 1
    #     self.knife_list.append(knife)
    
    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        
        self.wall_list.draw()
        self.player_list.draw()
        self.player_sprite.arrow_list.draw()
        self.player_sprite.fireball_list.draw()
        self.enemy.arrow_list.draw()
        self.enemy.fireball_list.draw()
        self.knife_list.draw()
        self.enemy.knife_list.draw()
        # Draw player health
        x = self.player_sprite.center_x
        y = self.player_sprite.center_y
        arcade.draw_rectangle_filled(x, y - 16, 24, 4, (255, 0, 0))
        arcade.draw_rectangle_filled(x - math.ceil((24 - (self.player_sprite.health / 4.16)) / 2), y - 16, math.ceil(self.player_sprite.health / 4.16), 4, (0, 255, 0))
         
        # Draw enemy health
        x = self.enemy.center_x
        y = self.enemy.center_y
        arcade.draw_rectangle_filled(x, y - 16, 24, 4, (255, 0, 0))
        arcade.draw_rectangle_filled(x - math.ceil((24 - (self.enemy.health / 4.16)) / 2), y - 16, math.ceil(self.enemy.health / 4.16), 4, (0, 255, 0))


    # def on_key_press(self, key, modifiers):
    #     """Called whenever a key is pressed. """
    #     # spatial
    #     if key == arcade.key.W:
    #         self.player_sprite.change_y = MOVEMENT_SPEED
    #     elif key == arcade.key.S:
    #         self.player_sprite.change_y = -MOVEMENT_SPEED
    #     elif key == arcade.key.A:
    #         self.player_sprite.change_x = -MOVEMENT_SPEED
    #     elif key == arcade.key.D:
    #         self.player_sprite.change_x = MOVEMENT_SPEED
    #     # Rotational
    #     elif key == arcade.key.LEFT:
    #         self.player_sprite.change_angle = ANGLE_SPEED
    #     elif key == arcade.key.RIGHT:
    #         self.player_sprite.change_angle = -ANGLE_SPEED
                
    #     # Arrow
    #     elif key == arcade.key.SPACE:
    #         self.shootarrow()
    #     # Fireball
    #     elif key == arcade.key.E:
    #         self.throwfire()
            # Knife
        # elif key == arcade.key.R and self.player_sprite.knife_num == 0:
        #     self.shortattack()
            
        # # Calls shield (will simplify and replace with arc that is always in front of player later) can be used 3 times (can be modified if need to)
        # if self.player_sprite.shield <= 3:
        #     if key == arcade.key.Q:
        #         self.equipshield()
                

    # def on_key_release(self, key, modifiers):
    #     """Called when the user releases a key. """

    #     if key == arcade.key.W or key == arcade.key.S:
    #         self.player_sprite.change_y = 0
    #     elif key == arcade.key.A or key == arcade.key.D:
    #         self.player_sprite.change_x = 0
    #     elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
    #         self.player_sprite.change_angle = 0

    # Functions that change with time
    def update(self, delta_time):
        """ Movement and game logic """
        # Call update on all sprites
        self.arrow_list.update()
        self.player_list.update()
        #self.physics_engine.update()
        self.fireball_list.update()
        self.enemy.fireball_list.update()
        self.enemy.arrow_list.update()
        self.player_sprite.fireball_list.update()
        self.player_sprite.arrow_list.update()



        current_state = {"player1_x" : self.player_sprite.center_x, "player1_y": self.player_sprite.center_y, "player2_x" : self.enemy.center_x, "player2_y" :self.enemy.center_x,
                        "player1_health" : self.player_sprite.health, "player2_health" : self.enemy.health,
                        "player1_fireballs" : self.fireball_list, "player2_fireballs" : self.enemy.fireball_list, "player1_arrows" : self.arrow_list, "player2_arrows": self.enemy.arrow_list}
        # printState(current_state)
           # if self.writer != 'na':
        #     self.writer.write(str(sys.getsizeof(current_state)))
        #     self.writer.write(str(current_state))

        #player collision
        if self.player_sprite.center_x <= 0:
            self.player_sprite.center_x = 0
        if self.player_sprite.center_x >= SCREEN_WIDTH:
            self.player_sprite.center_x = SCREEN_WIDTH
        if self.player_sprite.center_y <= 0:
            self.player_sprite.center_y = 0
        if self.player_sprite.center_y >= SCREEN_HEIGHT:
            self.player_sprite.center_y = SCREEN_HEIGHT
        #enemy collision
        if self.enemy.center_x <= 0:
            self.enemy.center_x = 0
        if self.enemy.center_x >= SCREEN_WIDTH:
            self.enemy.center_x = SCREEN_WIDTH
        if self.enemy.center_y <= 0:
            self.enemy.center_y = 0
        if self.enemy.center_y >= SCREEN_HEIGHT:
            self.enemy.center_y = SCREEN_HEIGHT


        for knife in self.knife_list:
            knife.center_x = self.player_sprite.center_x
            knife.center_y = self.player_sprite.center_y
            knife.angle = self.player_sprite.angle+180
        
        for knife in self.enemy.knife_list:
            knife.center_x = self.enemy.center_x
            knife.center_y = self.enemy.center_y
            knife.angle = self.enemy.angle+180
            
        #print("Health: ", self.enemy.health)
        for fireball in self.fireball_list:
            diff_x = fireball.start_x-fireball.center_x
            diff_y = fireball.start_y-fireball.center_y
            fireball_dist = math.sqrt(diff_x**2 + diff_y**2)
            if fireball_dist>200:
                fireball.kill()
       
        # Hit function for fireball)
        fireball_hit1 = arcade.check_for_collision_with_list(self.enemy, self.player_sprite.fireball_list)
        for fireball in fireball_hit1:
            fireball.kill()
            self.enemy.health -= FIREBALL_DAMAGE

        fireball_hit2 = arcade.check_for_collision_with_list(self.player_sprite, self.enemy.fireball_list)
        for fireball in fireball_hit2:
            fireball.kill()
            self.player_sprite.health -= FIREBALL_DAMAGE
       
        # Hit function for arrrow
        arrow_hit1 = arcade.check_for_collision_with_list(self.enemy, self.player_sprite.arrow_list) # for bad guy
        for arrow in arrow_hit1:
            arrow.kill()
            self.enemy.health -= ARROW_DAMAGE
        arrow_hit2 = arcade.check_for_collision_with_list(self.player_sprite, self.enemy.arrow_list) # for bad guy
        for arrow in arrow_hit2:
            arrow.kill()
            self.player_sprite.health -= ARROW_DAMAGE
        # Hit function for knife
        knife_hit1 = arcade.check_for_collision_with_list(self.enemy, self.player_sprite.knife_list) # for bad guy
        for knife in knife_hit1:
            knife.kill()
            self.enemy.health -= KNIFE_DAMAGE
            self.player_sprite.knife_num = 0
            
        knife_hit2 = arcade.check_for_collision_with_list(self.player_sprite, self.enemy.knife_list) # for bad guy
        for knife in knife_hit2:
            knife.kill()
            self.player_sprite.health -= KNIFE_DAMAGE
            self.enemy.knife_num = 0
        
        # If health is zero kill them
        if self.enemy.health <= 0:
            self.enemy.kill()
            self.player_sprite.score += 1 
            self.end_game()
            
        if self.player_sprite.health <= 0:
            self.player_sprite.kill()  
            self.enemy.score += 1 
            self.end_game()
       
def main(args):
    """ Main method """
    if len(args) > 3:
        raise Exception("Usage: python main.py <program_for_player_1> <program_for_player_2>")
    simultaneous_games = int(input('Enter the amount of simultaneous games: '))
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,simultaneous_games)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main(sys.argv)

