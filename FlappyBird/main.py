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
pygame.mixer.init()

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

#Music setup
pointSFX = pygame.mixer.Sound("FlappyBird/Assets/audio/point.wav")
flapSFX = pygame.mixer.Sound("FlappyBird/Assets/audio/wing.wav")
fallSFX = pygame.mixer.Sound("FlappyBird/Assets/audio/swoosh.wav")
hitSFX = pygame.mixer.Sound("FlappyBird/Assets/audio/hit.wav")

pointSFX.set_volume(.5)
flapSFX.set_volume(.5)
fallSFX.set_volume(.25)
hitSFX.set_volume(.5)

running = True
#managers setup
entityManager = EntityManager()
scoreManager = ScoreManager()

#Pipe manger setup
birdX = 400
pipeManager = PipeManager(entityManager, scoreManager, pointSFX,birdX) 

#Creates and adds the bird to the entity manager
bird = Bird(x=birdX, y=320,width=50, height=50, colPercentage=.97,name="Bird", color="yellow",aniSpeed=10, maxFlapTime=.25,gravity=50, maxFallSpeed=400, flapStrength=500)
bird.SetFramesImages(["FlappyBird/Assets/sprites/yellowbird-downflap.png","FlappyBird/Assets/sprites/yellowbird-midflap.png","FlappyBird/Assets/sprites/yellowbird-upflap.png","FlappyBird/Assets/sprites/yellowbird-midflap.png"])

entityManager.AddEntity(bird)

#Creates and adds the ground to the entity manager
ground = ObjectEntety(name="Ground", color="green", x=screenWidth/2, y=screenHeight - 50, width=screenWidth, height=100)
ground.SetFramesImages(["FlappyBird/Assets/sprites/base.png"])
entityManager.AddEntity(ground)

#For Score text
font = pygame.font.Font('freesansbold.ttf', 32)


backgroundImage = pygame.image.load("FlappyBird/Assets/sprites/background-day.png").convert_alpha()
backgroundImage = pygame.transform.scale(backgroundImage, (screenWidth, screenHeight))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.blit(backgroundImage,(0,0))
   
    #Updates the positions and draws all entities on screen
    entityManager.Update(screen)


    keys = pygame.key.get_just_pressed()
    
    if keys[pygame.K_SPACE]:
        bird.Flap()
        flapSFX.play()
    else:
        bird.FlapBurnOff()
        
    #Checks if the bird collided with the ground of the pipes
    if entityManager.DoesEntityCollide(bird):
        print("Bird Collided")
        hitSFX.play()
        if bird.y < screenHeight - 200:
            fallSFX.play()
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

