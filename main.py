import random # For generating random numbers which is used for random pillars
import sys # We will use sys.exit to exit the program whenever the user uses the cross button to close the game
import pygame   # Basic pygame imports
from pygame.locals import * # Basic pygame imports

# Global Variables for the game
FPS = 32    # FPS stands for frames per second
SCREENWIDTH = 289   # width of the screen 
SCREENHEIGHT = 511  # height of the screen
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))   # this will initilize a window or screen for display the game
GROUNDY = SCREENHEIGHT * 0.8    # 80% of the screen will be ground
GAME_SPRITES = {}   # this will display the images
GAME_SOUNDS = {}    # this will play the sounds
PLAYER = 'gallery/sprites/bird.png' # path of player(here the bird)
BACKGROUND = 'gallery/sprites/background.png'   # path of background
PIPE = 'gallery/sprites/pipe.png'   # path of pipe

def welcomeScreen():
    """
    Shows welcome images on the screen
    """
    # co-ordinate of player on the screen
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2) # player height which is in game sprites is subtracted from screen height in order to display the bird in center
    # co-ordinate of message on the screen
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)   # message width which is in game sprites is subtracted from screen width in order to display the message in center
    messagey = int(SCREENHEIGHT*0.13)
    # co-ordinate of base on the screen
    basex = 0   # the x co-ordinate will be 0
    while True:
        for event in pygame.event.get():    # tells about all the action that the user performs such as where the user clicks, which button is clicked
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return     # this will start the game and will stop showing the welcome screen
            else:
                # bliting all the images and message on the welcome screen on the their respective co-ordinate.
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update() # this is used to change/update the screen
                FPSCLOCK.tick(FPS)  # this controlls the game FPS

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)    # this will display playerx at the respective distance
    playery = int(SCREENWIDTH/2)    # this will display playery at the center of screen
    basex = 0   # this will blit the base of the game

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4       # assigning velocity to our pipe
    playerVelY = -9     # player will fall downward with this velocity
    playerMaxVelY = 10  # maximum velocity of player
    playerMinVelY = -8  # minimum velocity of player
    playerAccY = 1      # player acceleration speed

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:     # this is game loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): # when the user want to quit the game
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):   # when user is playing the game
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2   # mid position of player
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2  # middle positon of pipe
            if pipeMidPos<= playerMidPos < pipeMidPos +4:   # condition for player to cross pipe successfully
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY        # increasing the velocity of player when player is not flapping

        if playerFlapped:
            playerFlapped = False            # player is not flapping
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:      # condition for add the the pipe
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])   # append function is used to add new pipe
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():   # condition for removing the pipe
            upperPipes.pop(0)           # pop function is used to remove the pipe 
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y'])) 

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:     # condition when player gets collided with base and celling
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:     # conditon when player gets collided with upper pipe
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:     # condtion when player gets collided with lower pipe
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe


if __name__ == "__main__":      # This will be the main point from where our game will start
    pygame.init()   # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()  # This is used to control the FPS of the game
    pygame.display.set_caption('Flappy Bird by Ayush Ranjan')  # this is used to set caption
    GAME_SPRITES['numbers'] = (                                         # Creating a dictionary of all the number images
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),     # convert_alpha() is used to render image on screen faster
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()   # creating the message 
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()         # creating the base
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180),  # rotate is used to rotate the image by specified degree(here 180)
    pygame.image.load(PIPE).convert_alpha()   # creating the pipes, here there will be two pipes, one will be turned up side down and other will be straight
    )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()    # creating background sprites,   convert only changes the image
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()  # creating player sprites,   conver aplha changes both image and pixel

    while True:     # this is an infinite loop
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 