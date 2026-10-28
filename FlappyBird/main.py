# Example file showing a basic pygame "game loop"
from bird import Bird
from entity import ObjectEntety
import pygame
from entity_manager import EntityManager
from GlobalInfo import GlobalInfo
from pipe_creation import PipeManager
from ScoreManager import ScoreManager

# pygame setup
screenWidth = GlobalInfo.screenWidth
screenHeight = GlobalInfo.screenHeight
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
running = True

#managers setup
entityManager = EntityManager()
scoreManager = ScoreManager()

#Pipe manger setup
birdX = 400
pipeManager = PipeManager(entityManager, scoreManager, birdX) 

#Creates and adds the bird to the entity manager
bird = Bird(x=birdX, y=320,width=50, height=50, colPercentage=.97,name="Bird", color="yellow", maxFlapTime=.25,gravity=50, maxFallSpeed=400, flapStrength=500)
entityManager.AddEntity(bird)

#Creates and adds the ground to the entity manager
ground = ObjectEntety(name="Ground", color="green", x=screenWidth/2, y=screenHeight - 50, width=screenWidth, height=100)
entityManager.AddEntity(ground)

#For Score text
font = pygame.font.Font('freesansbold.ttf', 32)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("aqua")
   
    #Updates the positions and draws all entities on screen
    entityManager.Update(screen)


    keys = pygame.key.get_just_pressed()
    
    if keys[pygame.K_SPACE]:
        bird.Flap()
    else:
        bird.FlapBurnOff()
        
    #Checks if the bird collided with the ground of the pipes
    if entityManager.DoesEntityCollide(bird):
        print("Bird Collided")
        #Resets the game(pipes, score, etc) to start the game again
        pipeManager.FullPipesReset()
        scoreManager.ResetScore()
        bird.y = 320
        bird.ForceBurnOff()


    pipeManager.Update()
 
    scoreText = font.render(f"Score: {scoreManager.score}\nBest Score: {scoreManager.bestScore}", True, "white")
    screen.blit(scoreText, (screenWidth//2 - 50,10))
    # flip() the display to put your work on screen
    pygame.display.flip()
    #Updates the delta time for entity manager(for velocity)
    dt = clock.tick(60)/1000  # limits FPS to 60
    entityManager.UpdateDeltaTime(dt)


pygame.quit()

