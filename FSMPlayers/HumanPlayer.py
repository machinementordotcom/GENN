import arcade
import math
import random
from util.constants import * 

class HumanPlayer(arcade.Sprite):
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
            # Knife
        elif key == arcade.key.R and self.player_sprite.knife_num == 0:
            self.shortattack()
        elif key == arcade.key.ESCAPE:
            sys.exit()

        # Calls shield (will simplify and replace with arc that is always in front of player later) can be used 3 times (can be modified if need to)
        if self.player_sprite.shield <= 3:
            if key == arcade.key.Q:
                self.equipshield()
                
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0
    