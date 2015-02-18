#coding: utf-8
import time
import random
import sys
import os
import platform
if platform.system() == 'Windows':
	os.chdir("libtcod-1.6.0-mingw32")
else:
	if '32' in platform.architecture()[0]:
		os.chdir("libtcod-1.6.0-linux32")
	else:
		os.chdir("libtcod-1.6.0-linux64")
#os.chdir("libtcod-1.6.0-linux64")
sys.path.append("python")
import libtcodpy as libtcod
# 1.1 ########## Settings ############
# Game
SCREENWIDTH_X = 20
SCREENHEIGHT_Y = 20
GAME_SPEED = 300
WINSCORE = 30

WEIGHT_T = 5
# Graphics
LIMIT_FPS = 11

# existed dots
HEAP = []
# score
SCORE = 0
# 1.2 ########## Settings init ############
GAME_OVER = False

# 2.1########## Basic Objects #######


class Block(object):
    """basic self-propelled 1-d block"""
    # int x
    # int y

    def __init__(self, x, y):
        """
        :param x:
        :param y:
        """
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def move_left(self):
        self.x-=1
        return self
    def move_right(self):
        self.x+=1
        return self
    def move_down(self):
        self.y+=1
        return self
    # Just for rotating cases
    def move_up(self):
        self.y-=1
        return self
    def __str__(self):
        print "Block x=%d y=%d\n"% (self.x, self.y)

class Figure(object):
    """Parent of all figures"""
    # ownBlocks = []
    # copyblocks = []
    isRotated = 0
    
    def move_left(self):
        copyblocks = copy_blocks(self.ownBlocks)
        for n in copyblocks:
            n.move_left()
        if collision(copyblocks):
            pass # add unpleasant sound
        else:
            self.ownBlocks = copyblocks

    def move_right(self):
        copyblocks = copy_blocks(self.ownBlocks)
        for n in copyblocks:
            n.move_right()
        if collision(copyblocks):
            pass # add unpleasant sound
        else:
            self.ownBlocks = copyblocks

    # used in putting it down
    def move_down(self):
        copyblocks = copy_blocks(self.ownBlocks)
        for n in copyblocks:
            n.move_down()
        if collision(copyblocks):
            heap_absorb(self)
        else:
            self.ownBlocks = copyblocks

 #   @abstractmethod
  #  def rotate():

# 2.2########## Different figures #######

# __init__(self, x, y): and rotate(self): balance weight


class FigureT(Figure):
    """docstring for FigureT"""
    weight = WEIGHT_T
    def __init__(self):
        self.ownBlocks = []
        self.ownBlocks.append(Block(SCREENWIDTH_X/2, 0))
        self.ownBlocks.append(Block(SCREENWIDTH_X/2+1, 0))
        self.ownBlocks.append(Block(SCREENWIDTH_X/2+2, 0))
        self.ownBlocks.append(Block(SCREENWIDTH_X/2+1, 1))
        copyblocks = self.ownBlocks
        if collision(copyblocks):
            game_over()

    def rotate(self):
        copyblocks = copy_blocks(self.ownBlocks)
        if (self.isRotated == 0):
            copyblocks[1].move_down().move_left()
            copyblocks[2].move_down().move_down().move_left().move_left()
            copyrot = 1
        elif(self.isRotated == 1):
            copyblocks[2].move_left().move_up()
            copyrot = 2
        elif(self.isRotated == 2):
            copyblocks[3].move_down().move_left()
            copyrot = 3
        else:
            copyblocks[0].move_left().move_down()
            copyblocks[2].move_right().move_right()
            copyrot = 0

        if collision(copyblocks):
            pass # add unpleasant sound
        else:
            self.ownBlocks = list(copyblocks)
            self.isRotated = copyrot



# 2.2########## Collision Detection #######
def collision(copyblocks):
    # after new figure init
    # after rotate
    # after movesides
    # after godown
    """Returns True if figure collides ANYTHING"""
    # if its outside playground
    for block in copyblocks:
            if block.x < 0 or block.x >= SCREENWIDTH_X or block.y >= SCREENHEIGHT_Y: # or block.y <= 0
                """TEST
                print "collision"""
                return True

    # if it collides with heap
    for i in copyblocks:
        if i in HEAP:
            return True
    return False

# 2.2########## HEAP #######
def  heap_absorb(figure):
    global SCORE
    SCORE += figure.weight
    HEAP.extend(figure.ownBlocks)
    new_random_figure_factory()

def heap_checkline():
    pass

def game_over():
    global GAME_OVER
    GAME_OVER = True

def new_random_figure_factory():
    global missile
    obj = random.choice([FigureT])
    missile = obj()

##### UTIL #####
"""This is just for fine copy of figure`s array, to use copy, not original"""
def copy_blocks(ownblocks):
    copyblocks = []
    for block in ownblocks:
            copyblocks.append(Block(block.x, block.y))
    return copyblocks

def timer():
    global timeNow
    cur_time = libtcod.sys_elapsed_milli()
    if  (timeNow + GAME_SPEED) > cur_time:
        return True
    else:
        timeNow = cur_time
        return False


######################################
# 2 ########## Graphics ############
######################################

### key control

def handle_keys():
    #movement keys
    key = libtcod.console_check_for_keypress()
    if libtcod.console_is_key_pressed(libtcod.KEY_LEFT ):
        # print missile.ownBlocks[1].x #test
        missile.move_left()
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        missile.move_right()
    elif libtcod.console_is_key_pressed(libtcod.KEY_SPACE):
        missile.rotate()
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        missile.move_down()


### render
libtcod.console_set_custom_font('data/fonts/arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREENWIDTH_X, SCREENHEIGHT_Y, 'snid1 supermegatetris', False)
libtcod.sys_set_fps(LIMIT_FPS)
timeNow = libtcod.sys_elapsed_milli()

missile = FigureT()
# Game speed control FALSE == NEXT STEP

# The Loop
"""TEST
HEAP.append(Block(10,10))"""
def clear_window():
    for y in range (SCREENHEIGHT_Y):
            for x in range (SCREENWIDTH_X):
                libtcod.console_put_char(0, x, y, ' ', libtcod.BKGND_NONE)

def game_window():
    while(True):
        clear_window()

            # rendering missile
        for block in missile.ownBlocks:
            libtcod.console_put_char(0, block.x, block.y, '@', libtcod.BKGND_NONE)
            # rendering heap
        for block in HEAP:
            libtcod.console_put_char(0, block.x, block.y, '#', libtcod.BKGND_NONE)
        ex = handle_keys()
        libtcod.console_flush()
        if not timer():
            break


while not libtcod.console_is_window_closed():
    game_window()
    missile.move_down()
    heap_checkline()
    if GAME_OVER:
        word = "GAME OVER"
        word2 = "SCORE: " + str(SCORE)
        startX = 5
        startY = SCREENHEIGHT_Y/2
        clear_window()
        for letter in word:
            libtcod.console_put_char(0, startX, startY, letter, libtcod.BKGND_NONE)
            startX+=1
        startX = 3
        for letter in word2:
            libtcod.console_put_char(0, startX, startY-2, letter, libtcod.BKGND_NONE)
            startX+=1
        libtcod.console_flush()
        time.sleep(10)
    if SCORE >= WINSCORE:
        word1 = "YOU WIN!!!"
        word2 = "SCORE: " + str(SCORE)
        startX = 3
        startY = SCREENHEIGHT_Y/2
        clear_window()
        for letter in word1:
            libtcod.console_put_char(0, startX, startY, letter, libtcod.BKGND_NONE)
            startX+=1
        startX=3
        for letter in word2:
            libtcod.console_put_char(0, startX, startY+2, letter, libtcod.BKGND_NONE)
            startX+=1
        libtcod.console_flush()
        time.sleep(10)