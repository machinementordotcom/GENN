import arcade
import os
import math
import random
import time
import sys
import collections
import heapq

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Sprite Move with Walls Example"

PLAYER_START_X = 10
PLAYER_START_Y = 10

ENEMY_START_X = 900
ENEMY_START_Y = 600


MOVEMENT_SPEED = 5
ARROW_SPEED = 20
ANGLE_SPEED = 2
#variables for making walls for arcade viewing and a* algo
VERT_WALL_START=1
VERT_WALL_END=1
VERT_CENTER = 465 # X value
HOR_WALL_START=1
HOR_WALL_END=1
HOR_CENTER = 200 # y value
class Arrow(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
class Fireball(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
class Enemy(arcade.Sprite):
    def throwfire(self):
        fireball = Fireball("fire.png", .1)
        fireball.center_x = self.center_x
        fireball.center_y = self.center_y
        fireball.start_x = self.center_x # for tracking 
        fireball.start_y = self.center_y # fireball distance
        fireball.angle = self.angle-90
        fireball.change_x = -ARROW_SPEED*math.sin(math.radians(self.angle))
        fireball.change_y = ARROW_SPEED*math.cos(math.radians(self.angle))
        
        self.fireball_list.append(fireball)
    def shootarrow(self):
        arrow = Arrow("arrow.png",.1)
        arrow.center_x = self.center_x
        arrow.center_y = self.center_y
        arrow.angle = self.angle-90
        arrow.change_x = -ARROW_SPEED*math.sin(math.radians(self.angle))
        arrow.change_y = ARROW_SPEED*math.cos(math.radians(self.angle))
        self.arrow_list.append(arrow)
    def equipshield():
        pass
    def update(self):
        self.curtime += 1 
        x_diff = self.opponent.center_x - self.center_x
        y_diff = self.opponent.center_y - self.center_y
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle = math.degrees(math.atan2(y_diff,x_diff))-90
        self.change_x = math.cos(self.angle)*MOVEMENT_SPEED
        self.change_y = math.sin(self.angle)*MOVEMENT_SPEED
        self.d = math.sqrt(x_diff**2 +y_diff**2)
        if self.curtime >=30:
            
            if self.d <= 200:
                self.throwfire()
            else:
                self.shootarrow()
            self.curtime = 0
        #if self.health <=50:
            #self.equipshield()

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
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
        
        # Set up the player
        self.player_sprite = arcade.Sprite("mage.png",SPRITE_SCALING)
        self.player_sprite.append_texture(arcade.load_texture("a_shield_round.png"))
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_sprite.angle = 0
        self.player_sprite.score = 0
        self.player_sprite.health = 100
        self.player_sprite.shield = 0
        self.player_list.append(self.player_sprite)
        
        # Set up bad guy
        self.enemy = Enemy('lilknight.png',1)
        self.enemy.center_x = 800
        self.enemy.opponent = self.player_sprite
        self.enemy.center_y = 600
        self.enemy.health = 100
        self.enemy.score = 0
        self.enemy.curtime = 0
        self.player_list.append(self.enemy)
        self.enemy.arrow_list = arcade.SpriteList()
        self.enemy.fireball_list = arcade.SpriteList()
        
        """
        This is unneccessary if we are just doing an arena style for now
        # -- Set up the walls
        # Create a row of boxes
        for x in range(173, 650, 64):
            wall = arcade.Sprite("bricks.png", .3)
            wall.center_x = x
            wall.center_y = 200
            self.wall_list.append(wall)

        # Create a column of boxes
        for y in range(273, 500, 64):
            wall = arcade.Sprite("bricks.png", .3)
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
    # Long attack
    def shootarrow(self):
        arrow = Arrow("arrow.png",.1)
        arrow.center_x = self.player_sprite.center_x
        arrow.center_y = self.player_sprite.center_y
        arrow.angle = self.player_sprite.angle-90
        arrow.change_x = -ARROW_SPEED*math.sin(math.radians(self.player_sprite.angle))
        arrow.change_y = ARROW_SPEED*math.cos(math.radians(self.player_sprite.angle))
        self.arrow_list.append(arrow)
    # Shorter attack
    def throwfire(self):
        fireball = Fireball("fire.png", .1)
        fireball.center_x = self.player_sprite.center_x
        fireball.center_y = self.player_sprite.center_y
        fireball.start_x = self.player_sprite.center_x # for tracking 
        fireball.start_y = self.player_sprite.center_y # fireball distance
        fireball.angle = self.player_sprite.angle-90
        fireball.change_x = -ARROW_SPEED*math.sin(math.radians(self.player_sprite.angle))
        fireball.change_y = ARROW_SPEED*math.cos(math.radians(self.player_sprite.angle))
        
        self.fireball_list.append(fireball)
    
    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        
        self.wall_list.draw()
        self.player_list.draw()
        self.arrow_list.draw()
        self.fireball_list.draw()
        self.enemy.arrow_list.draw()
        self.enemy.fireball_list.draw()
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


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        # spatial
        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
        # Rotational
        elif key == arcade.key.LEFT:
            self.player_sprite.change_angle = ANGLE_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_angle = -ANGLE_SPEED
                
        # Arrow
        elif key == arcade.key.SPACE:
            self.shootarrow()
        # Fireball
        elif key == arcade.key.E:
            self.throwfire()
        # Calls shield (will simplify and replace with arc that is always in front of player later) can be used 3 times (can be modified if need to)
        if self.player_sprite.shield <= 3:
            if key == arcade.key.Q:
                self.player_sprite.set_texture(1)
                self.player_sprite.health += 50
                self.player_sprite.shield +=1
                

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0

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
        
        
        #print("Health: ", self.enemy.health)
        for fireball in self.fireball_list:
            diff_x = fireball.start_x-fireball.center_x
            diff_y = fireball.start_y-fireball.center_y
            fireball_dist = math.sqrt(diff_x**2 + diff_y**2)
            if fireball_dist>200:
                fireball.kill()
            print("fireball distance: ",diff_x, diff_y)
       
        # Hit function for fireball
        fireball_hit1 = arcade.check_for_collision_with_list(self.enemy, self.fireball_list)
        for fireball in fireball_hit1:
            fireball.kill()
            self.enemy.health -= 20

        fireball_hit2 = arcade.check_for_collision_with_list(self.player_sprite, self.enemy.fireball_list)
        for fireball in fireball_hit2:
            fireball.kill()
            self.player_sprite.health -= 20
       
        # Hit function for arrrow
        arrow_hit1 = arcade.check_for_collision_with_list(self.enemy, self.arrow_list) # for bad guy
        for arrow in arrow_hit1:
            arrow.kill()
            self.enemy.health -= 10
        arrow_hit2 = arcade.check_for_collision_with_list(self.player_sprite, self.enemy.arrow_list) # for bad guy
        for arrow in arrow_hit2:
            arrow.kill()
            self.player_sprite.health -= 10
        
        #goodguyscore = open('goodguyscore.txt','w')
        #badguyscore = open('badguyscore.txt','w')
        
        # If health is zero kill them
        if self.enemy.health <= 0:
            self.enemy.kill()
            self.player_sprite.score += 1 # If enemy dies give good guy a point
            file = open("goodguyscore.txt","w")
            file.write(str(self.player_sprite.score))
            sys.exit()
            
        if self.player_sprite.health <= 0:
            self.player_sprite.kill()  
            self.enemy.score += 1 
            file = open("goodguyscore.txt","w")
            file.write(str(self.enemy.score)) 
            sys.exit()
       
def main():
    """ Main method """
   
    simultaneous_games = int(input('Enter the amount of simultaneous games: '))
    #will run multiple games at once.
    for g in range(0,simultaneous_games):
        window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        window.setup()
        arcade.run() 
        


if __name__ == "__main__":
    main()
