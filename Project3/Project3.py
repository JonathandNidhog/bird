import pygame 
from time import sleep
from random import randrange
# Initialize Pygame
pygame.init()

# Set screen width and height
map_w = 284  
map_h = 512  

# Set frame and FPS
frame = 0  # Current frame number
FPS = 60  # Frames per second

# Set pipes
pipes = [[180,4]]
# Set Bird position 
bird = [40,map_h//2-50]
# Set gravity
gravity = 0.2
# Set Velocity
velocity = 0

# Set Status
game_status = "not_started"

# Create game window and load background image
gameScreen = pygame.display.set_mode((map_w, map_h))  
clock = pygame.time.Clock() 
background = pygame.image.load("images/background.png")  
pipe_b = pygame.image.load("images/pipe_body.png")
pipe_e = pygame.image.load("images/pipe_end.png")
# Load bird asset
bird_up = bird_up_copy =  pygame.image.load("images/bird_wing_up.png") 
bird_down = bird_down_copy =  pygame.image.load("images/bird_wing_down.png") 
#Draw pipes
def draw_pipes():
    global pipes
    for n in range(len(pipes)):
        for m in range(pipes[n][1]):
            gameScreen.blit(pipe_b,(pipes[n][0], m*32))
        for m in range (pipes[n][1]+6, 16):
            gameScreen.blit(pipe_b,(pipes[n][0], m*32))
        gameScreen.blit(pipe_e,(pipes[n][0],(pipes[n][1])*32))
        gameScreen.blit(pipe_e,(pipes[n][0],(pipes[n][1]+5)*32))
        pipes[n][0] -= 1
        
# Define the function to draw the bird
def draw_bird(x,y):
    global frame 
    if 0 <= frame<=30:
        gameScreen.blit(bird_up,(x,y))
        frame +=1
    elif 30<frame<=60:
        gameScreen.blit(bird_down,(x,y))
        frame +=1
        if frame == 60 : frame = 0    
# Define the function about did the bird touch the pipes
def safe():
    if bird[1]>map_h - 35:
        print("hit floor")
        return False
    if bird[1]<0:
        print("hit celling")
        return False
    if pipes[0][0]-30 < bird[0] < pipes[0][0] + 79:
        if bird[1]<(pipes[0][1]+1)*32 or bird[1]>(pipes[0][1]+4)*32:
            print("hit pipe")
            return False
    return True 
# Reset Game function 
def reset():
    global frame,map_h,map_w,FPS,pipes,bird,gravity,velocity
    frame = 0
    FPS = 60 
    map_w = 284  
    map_h = 512 
    pipes.clear()
    bird.clear()
    pipes = [[180,4]] 
    bird = [40,map_h//2-50]
    gravity = 0.2
    velocity = 0
# Define the main game loop
def gameLoop():
    # Use the global variable 'background' within this function
    global background,velocity,bird_up,bird_down
    while True:

        # Add random pipes
        if len(pipes)<4:
            x = pipes[-1][0] + 200
            open_pos = randrange(1,9)
            pipes.append([x,open_pos])
        if pipes[0][0]<-100:
            pipes.pop(0)    
        
        # Close the game when the Close button is clicked
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:# Control bird  
                bird[1] -= 40
                velocity = 0
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        # Add gravity to bird
        velocity += gravity
        bird[1] += velocity
        # Turn Bird Head
        bird_down = pygame.transform.rotate(bird_down_copy,-90*(velocity/15))
        bird_up = pygame.transform.rotate(bird_up_copy,-90*(velocity/15))
        # Draw the background image onto the game screen
        gameScreen.blit(background, (0, 0))
        # Draw the bird
        draw_bird(bird[0],bird[1])
        # Draw pipes
        draw_pipes()
        # Update the display
        pygame.display.update()
        # Check player alive or not
        if not safe():
            sleep(3)
            reset()
        # Set the game's FPS
        clock.tick(FPS)

# Call the main game loop function
gameLoop()
