import arcade
import tensorflow as tf
import numpy as np
from tensorflow import keras
import multiprocessing

SPRITE_SCALING = 0.5
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Adaptive AI"
ARROW_IMAGE_HEIGHT = 7.9
MOVEMENT_SPEED = 3#7.5 
ARROW_SPEED = 12  #20
ANGLE_SPEED = 4
#variables for making walls for arcade viewing and a* algo
VERT_WALL_START=1
VERT_WALL_END=1
VERT_CENTER = 465 # X value
HOR_WALL_START=1
HOR_WALL_END=1
HOR_CENTER = 200 # y value
BOX = 3


PLAYER_HEALTH = 1000#80
SCALING_ADJUSTMENT = PLAYER_HEALTH/80

ARROW_HITS_UNTIL_DEATH = 5.2 * SCALING_ADJUSTMENT #5.5
ARROW_DAMAGE = PLAYER_HEALTH / ARROW_HITS_UNTIL_DEATH
FIREBALL_HITS_UNTIL_DEATH = 5.4 * SCALING_ADJUSTMENT
FIREBALL_DAMAGE = PLAYER_HEALTH / FIREBALL_HITS_UNTIL_DEATH
KNIFE_HITS_UNTIL_DEATH = 3.2 * SCALING_ADJUSTMENT
KNIFE_DAMAGE = PLAYER_HEALTH / KNIFE_HITS_UNTIL_DEATH


SHORT_SPEED_HANDICAP = .145#.955
MID_SPEED_HANDICAP = .09#1




MAGE_IMAGE = 'images/mage.png'
KNIGHT_IMAGE = 'images/lilknight.png'

# def decideWinner(num):
#     health = float(num)
#     if health < 
class Counter(object):
    def __init__(self, initval=0):
        self.val = multiprocessing.RawValue('i', initval)
        self.lock = multiprocessing.Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    @property
    def value(self):
        return self.val.value
class HitBox(arcade.Sprite):
    z = 500
    y = ARROW_IMAGE_HEIGHT
class Knife(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
class Arrow(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
class Fireball(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
class ArrowSimulated:
    def __init__(self, x, y, v, box):
        self.x = x 
        self.y = y
        self.vel = v
        self.box = box
class FireballSimulated:
    def __init__(self, x, y, v, box):
        self.x = x 
        self.y = y
        self.vel = v
        self.box = box
class Layer:
    def __init__(self, weights):
        self.weights = weights
class Network:
    def __init__(self, layers):
        self.layers = layers
        tensors = []
        layer = tf.keras.layers.Dense(1, input_shape=(17,1))
        inputs = keras.Input(shape=(17,))
        for i in range(len(layers)): 
            if i == 0:
                h = tf.keras.layers.Dense(len(layers[i].weights[0]), activation='relu')(inputs)
                # h.set_weights()
            elif i < len(layers) - 1:
                h = tf.keras.layers.Dense(len(layers[i].weights[0]), activation='relu')
            else:
                move_x = tf.keras.layers.Dense(1,activation='relu')
                move_x = tf.keras.layers.Dense(1,activation='relu')
                shoot1 = tf.keras.layers.Dense(1,activation='softmax')
                shoot2 = tf.keras.layers.Dense(1,activation='softmax')
                shoot3 = tf.keras.layers.Dense(1,activation='softmax')
                # if i == 0: 
                #     temp = h(inputs)
                # else: 
                #     temp = h(layers[i-1])
                # print(np.asarray(weights).shape)
                # print(len(weights),len(weights[0]))
                # print(np.asarray(np.zeros( np.asarray(weights).shape[1]) ))
                # h.set_weights([np.asarray(weights),np.asarray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])])#np.asarray(np.zeros( np.asarray(weights).shape[1],) )])
    # def buildNetwork



