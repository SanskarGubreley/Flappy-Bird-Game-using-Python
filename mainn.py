# from asyncio import events
# from http.client import HTTPS_PORT
from asyncio.windows_utils import pipe
import imp
# from multiprocessing import Pipe
# from multiprocessing.context import get_spawning_popen
# from os import SCHED_BATCH
# from platform import python_branch
import random
# from readline import get_history_length
# from re import T # for generating random numbers
import sys
from webbrowser import get
# from tkinter import SW
# from tkinter.tix import MAIN
# from turtle import Screen
# from unicodedata import name
# from webbrowser import get
# from pip import main
# import pip  # we will use sys.exit to exit the program
import pygame 
from pygame.locals import *  #basic pygame imports


# global variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))  # by this statement pygame will gave us a screen of these width & height
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery\ sprites\ bird'
BACKGROUND = 'gallery\ sprites\ background'
PIPE = 'gallery\ sprites\ pipe'

def welcomeScreen():
    """
    shows welcome images on the screen
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()))/2 # to keep the bird in center.
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()))/2
    messagey = int((SCREENHEIGHT*0.13))
    basex =  0
    while True:
        for event in pygame.events.get():
            # pygame.locals.get() tells every action taken through keyboard or mouse from user
            #if user press the close button to exit the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if the user press the space or upkey, start the game 
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0 ))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery ))
                SCREEN.blit(GAME_SPRITES['message'],(messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY ))
                pygame.display.update()  # screen won't change if this function won't execute
                FPSCLOCK.tick(FPS)  # to control my game frames per second
                

def maingame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENWIDTH/2)
    basex=0

    # create 2 pipes for blitting on the screen 
    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()

    # my list of upper pipes & bird will stay as it is rather pipes will move and it'll apear as bird is moving
    # starting a pipe after scree i.e. 200 aaage uske baad next one usse thoda aage isliye screenwidth/2
    upperpipes =[
        {'x': SCREENWIDTH+200 , 'y' : newpipe1[0]['y']},
        {'x': SCREENWIDTH +200+ (SCREENWIDTH/2) , 'y' : newpipe2[0]['y']}
        ]
    # my list of lower pipes
    lowerpipes = [{'x': SCREENWIDTH+200 , 'y' : newpipe1[0]['y']}
    ,{'x': SCREENWIDTH +200+ (SCREENWIDTH/2) , 'y' : newpipe2[1]['y']}]
        

    # giving velocity to pipe at which pipes will move(oppositely move)
    pipeVelX = -4
    """
    player will go down with a speed of -9 with a certain accelearation of 1 
    and max speed and min speed are defined below
    """
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while Flapping
    playerFlapped = False # it is true only when the bird is flapping


    """
    now we will make a loop whenever it will run the images are going to be iterated and the game will run according to it loop
    & the keyswe are using we can learn it from pygame library (google it) no need to remember them
    """

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == K_DOWN and event.key == K_ESCAPE ):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True 
                    # we'll play some sounds also
                    GAME_SOUNDS['wings'].play()


        crashTest = isCollide(playerx,playery , upperpipes ,lowerpipes)  # this function will return true if you're crashed 
        if crashTest:
            return

        # we have also implemented the scores so to check score
        playerMidpos = playerx + GAME_SPRITES['player'].get_width()/2   # we are getting the middle position of the player here
        for pipe in upperpipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <=playerMidpos < pipeMidPos+4:
                """
                if player is in somewhere middle between the pipes scor bada do
                """
                score+=1
                print(f"your score is {score}")
                GAME_SOUNDS['points'].play()

        # to increase the player velocity after passing every pipe
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY 

        # if player is flapping we'll make it false because if he is pressing upper key again and again the only make the bird flying else ek baari press krke he leaves then make the player fall down
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playerY = playerY + min(playerVelY , GROUNDY - playerY - playerHeight) # playerY ko badao lekin tab jab vo ground pe aa ajae and min of isliye use kiya ki kahin vo 0 ke neeche yani ground ke neeche hi na ghus jae  jo min mein second term hai that is nothing but zero always 


        # now we'll move pipes to the left because we have already kept the pipes after the screen to create illusion and we'll make them keep moving
        for upperPipe , lowerPipe in zip(upperpipes , lowerpipes):
            upperPipe['x']+= pipeVelX
            lowerPipe['x']+= pipeVelX
            # we have taken velocity as -4 i.e; negative so above we use + to slow down them ultimately
            
            #add a new pipe when the first pipe is about to cross the leftmost part of the screen
            if 0 < upperpipes[0]['x']< 5:
                newpipe = getRandomPipes()
                upperpipes.append(newpipe[0])
                lowerpipes.append(newpipe[1])



            # if the pipe is out of the screen , remove it
            if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
                """
                if pipe screen ke left mein nikal gaya i.e. x co-ordinates negative mein hai
                """
                upperpipes.pop(0)
                lowerpipes.pop(0)

            # let's blit our sprites i.e. we will just simply draw them on screen
            SCREEN.blit(GAME_SPRITES['background'], (0,0))
            for upperPipe , lowerPipe in zip(upperpipes , lowerpipes):
                SCREEN.blit(GAME_SPRITES['base'][0], (upperPipe['x'],lowerPipe['y']))
                SCREEN.blit(GAME_SPRITES['base'][1], (lowerPipe['x'],lowerPipe['y']))
            SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
            SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))

            # now we will show our score by using a simple list comprehension
            myDigits = [intx for x in list(str(score))]
            width = 0 # total width which is going to captured for blitting of scores to our screen
            for digit in myDigits:
                width += GAME_SPRITES['numbers'][digit].get_width()
            Xoffset = (SCREENWIDTH - width)/2  # div by 2 because blitting should be in middle we should know that where we want to blit 


            for digit in myDigits:
                SCREEN.blit(GAME_SPRITES['numbers'][digit] , (Xoffset , SCREENHEIGHT * 0.12)) # ofcourse we can choose at what height we want to display
                # now we 'll increase our Xoffset value to print the next number
                Xoffset += GAME_SPRITES['numbers'][digit].get_width()
            pygame.display.update()
            FPSCLOCK.tick(FPS)  # to control the frame rate per second

def isCollide(playerx,playery , upperpipes ,lowerpipes):
    """
    this function will only return true if you are crashed.
    """
    if playery > GROUNDY-25 or playery <0:  # if player screen se bahar chala jae or ground pe touch ho gaye then it'll return true
        GAME_SOUNDS['hit'].play()
        
        return True
    return False

    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and (abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width())):
            GAME_SOUNDS['hit'].play()
        
            return True

    for pipe in lowerpipes:
        if (playery + GAME_SPRITES['player'].get_height()> pipe['y']) and (abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
        
            return True

             






def getRandomPipes():
    """
    generate position of two pipes for blitting on the screen (one straighted and one rotated)
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()

    y2 = offset + random.randrange(0,int(SCREENHEIGHT -  GAME_SPRITES['base'].get_height()- 1.2*offset))
    pipex = SCREENWIDTH + 10 # added 10 because pipe will come from forward so that's why added 10 i.e; after the screen
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipex , 'y': -y1}, # upper pipe co-ordinates
        {'x':pipex, 'y': y2 }
    ]
    return pipe




if __name__ == "__main__":
    # this will be the mainpoint from our gamew will start
    pygame.init()  #Initializes all pygame modules
    FPSCLOCK = pygame.time.Clock()  # it's use to control framerate of the game
    pygame.display.set_caption("Flappy Bird by Sanskar Gubreley")
    # created a tuple of numbers
    #and convert_alpha is used to optimize the image to game basically it will rendor the images fastly
    
    GAME_SPRITES['numbers'] = (
            pygame.image.load('gallery\sprites\zero.png.png').convert_alpha(),
            pygame.image.load('gallery\sprites\one.png.png').convert_alpha(),
            pygame.image.load('gallery\sprites\wo.png.png').convert_alpha(),
            pygame.image.load('gallery\sprites\hree.png.png').convert_alpha(),
            pygame.image.load('gallery\sprites\our.png').convert_alpha(),
            pygame.image.load('gallery\sprites\ive.png').convert_alpha(),
            pygame.image.load('gallery\sprites\six.png').convert_alpha(),
            pygame.image.load('gallery\sprites\seven.png').convert_alpha(),
            pygame.image.load('gallery\sprites\eight.png').convert_alpha(),
            pygame.image.load('gallery\sprites\ine.png').convert_alpha(),)

    
    GAME_SPRITES['message'] = pygame.image.load('gallery\sprites\message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180 ),
                            pygame.image.load(PIPE).convert_alpha())
                            

    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wings'] = pygame.mixer.Sound('gallery/audio/wings.wav')
    GAME_SOUNDS['points'] = pygame.mixer.Sound('gallery/audio/points.wav')
    
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()


    while True:
        welcomeScreen()  # shows welcoe screen until he presses a button
        mainGame()  # This is the main game function
        
