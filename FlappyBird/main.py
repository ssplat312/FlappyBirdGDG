# Example file showing a basic pygame "game loop"
from entity import ObjectEntety
import pygame
from entity_manager import EntityManager
from GlobalInfo import GlobalInfo
from pipe_creation import PipeManager
from ScoreManager import ScoreManager
from BirdObject  import Bird
from Button import Button
from TextInputBox import TextInputBox
from DatabaseHandler import DatabaseHandler
import json

def SetLoginUIViz():
    global loginUI
    global logined
    
    if logined:
        for ui in loginUI:
            ui.Hide()
    else:
        for ui in loginUI:
            ui.Show()

def SetStartScreen():
    global bird
    global GameState
    global startUI
    global deathUI
    global loginUI
    global pipeManager
    global scoreManager
    bird.isStatic = True
    bird.isDead = False
    bird.y = bird.staticY
    pipeManager.FullPipeResetWithoutCreation()
    scoreManager.ResetScore()
    for ui in deathUI:
        ui.Hide()
                
    for ui in startUI:
        ui.Show()
    
    SetLoginUIViz()
        
    GameState = 0
     

def StartGame():
    global bird
    global GameState
    global startUI
    global loginUI
    global deathUI
    global pipeManager
    
    for ui in deathUI:
        ui.Hide()
            
    for ui in startUI:
        ui.Hide()
        
    for ui in loginUI:
        ui.Hide()
        
    bird.isStatic = False
    bird.isDead = False
    pipeManager.FullPipesReset()
    
    GameState = 1

    
def SetDeathScreen():
    global bird
    global GameState
    global startUI
    global deathUI
    global loginUI
    global pipeManager
    
    GameState = 2
    bird.isDead = True
    bird.isStatic = False
    hitSFX.play()
    if bird.y < screenHeight - 200:
        fallSFX.play()
    # Resets the game(pipes, score, etc) to start the game again
    pipeManager.StopPipes()

    for ui in deathUI:
        ui.Show()
        
    for ui in startUI:
        ui.Hide()
        
    for ui in loginUI:
        ui.Hide()
        
        

def GetAccountInfo(username:str, password:str):
    global account
    global scoreManager
    global databaseHandler
    global logined
    account = databaseHandler.GetAccount(username, password)
    if account is not None:
        scoreManager.bestScore = account["Bestscore"]
        logined = True
    
    SetLoginUIViz()


def CreateAccount(username:str, password:str):
    global account
    global scoreManager
    global databaseHandler
    global logined
    account = databaseHandler.AddAccount(username, password)
    if account is not None:
        account["Bestscore"] = scoreManager.bestScore
        logined = True
        
def FormHandle():
    global usernameInput
    global passwordInput
    global databaseHandler
    username = usernameInput.text
    password = passwordInput.text
    if databaseHandler.UserNameIsTaken(username):
        GetAccountInfo(username, password)
    else:
        CreateAccount(username, password)
    
    SetLoginUIViz()

    
def ToggleRememberMe():
    global rememberMe
    rememberMe = rememberMe == False

# pygame setup
screenWidth = GlobalInfo.screenWidth
screenHeight = GlobalInfo.screenHeight
GameState = 1  # 0 is start, 1 is game playing, 2 is death, for the ui
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# Music setup
pointSFX = pygame.mixer.Sound("Assets/audio/point.wav")
flapSFX = pygame.mixer.Sound("Assets/audio/wing.wav")
fallSFX = pygame.mixer.Sound("Assets/audio/swoosh.wav")
hitSFX = pygame.mixer.Sound("Assets/audio/hit.wav")

pointSFX.set_volume(.5)
flapSFX.set_volume(.5)
fallSFX.set_volume(.25)
hitSFX.set_volume(.5)

running = True
deathScreenShown = False
startScreenShown = False
mouseClick = False
# managers setup
entityManager = EntityManager()
scoreManager = ScoreManager()

# Pipe manger setup
birdX = 400
pipeManager = PipeManager(entityManager, scoreManager, pointSFX, birdX) 

# Creates and adds the bird to the entity manager
bird = Bird(x=birdX, y=320, width=50, height=50, colPercentage=.97, name="Bird", color="yellow", aniSpeed=10, maxFlapTime=.25, gravity=50, maxFallSpeed=400, flapStrength=500)
bird.SetFramesImages(["Assets/sprites/yellowbird-downflap.png", "Assets/sprites/yellowbird-midflap.png", "Assets/sprites/yellowbird-upflap.png", "Assets/sprites/yellowbird-midflap.png"])
entityManager.AddEntity(bird)

# Creates and adds the ground to the entity manager
ground = ObjectEntety(name="Ground", color="green", x=screenWidth / 2, y=screenHeight - 50, width=screenWidth, height=100)
ground.SetFramesImages(["Assets/sprites/base.png"])
entityManager.AddEntity(ground, 1)

# For Score text
font = pygame.font.Font('freesansbold.ttf', 32)
BUTTONCOLOR = (120, 120, 120)
BUTTONHOVERCOLOR = (100, 100, 100)

backgroundImage = pygame.image.load("Assets/sprites/background-day.png").convert_alpha()
backgroundImage = pygame.transform.scale(backgroundImage, (screenWidth, screenHeight))

saveFile = None
with open('SaveFile.json', "r", encoding='utf-8') as file:
    saveFile = json.load(file)

deathUI: list[ObjectEntety] = [Button(SetStartScreen, text="Restart", name="DeathButton", x=screenWidth // 2, y=screenHeight * .5, width=200, height=50)]
startUI: list[ObjectEntety] = [Button(StartGame, text="Start", name="StartButton", x=screenWidth // 2, y=screenHeight * .45, width=200, height=50), Button(ToggleRememberMe, text="Remember Me?", name="RemeberButton",x=screenWidth // 2, y=screenHeight * .55, width=200, height=50)]
loginUI: list[ObjectEntety] = []
passwordInput = TextInputBox(name="PasswordInput",x=screenWidth//2, y=screenHeight*.75, width=200, height=50, color=(0,0,0), decorText="Password: ",textColor=(0,0,0), inactiveColor=(255,255,255), activeColor=(240,240,240))
usernameInput = TextInputBox(name="UsernameInput",x=screenWidth//2, y=screenHeight*.65, width=200, height=50, color=(0,0,0), decorText="Username: ", textColor=(0,0,0),inactiveColor=(255,255,255), activeColor=(240,240,240))
loginUI.append(usernameInput)
loginUI.append(passwordInput)
loginUI.append(Button(FormHandle, name="FormButton", text="Login/Create", x =screenWidth//2, y=screenHeight * .85, width=200, height=50))



logined = False
databaseHandler = DatabaseHandler()

rememberMe = False
username = ""
password = ""
if saveFile is not None:
    rememberMe = saveFile["RememberAccount"]
    username = saveFile["AccountName"]
    password = saveFile["AccountPassword"]

account = None

if rememberMe:
    account = databaseHandler.GetAccount(username, password)
    if account:
        scoreManager.bestScore = account["Bestscore"]
        logined = True


globalInfo = GlobalInfo()

for ui in deathUI:
    ui.Hide()
    entityManager.AddEntity(ui)
    
for ui in startUI:
    ui.Hide()
    entityManager.AddEntity(ui)
    
for ui in loginUI:
    ui.Hide()
    entityManager.AddEntity(ui)
    
SetStartScreen()

while running:
    
    mouseClick = False
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseClick = True
            GlobalInfo.mouseClick = True
            
        if event.type == pygame.KEYDOWN:
            GlobalInfo.pressedKey = True
            GlobalInfo.curKey = event.key
            GlobalInfo.curUnicode = event.unicode

    # fill the screen with a color to wipe away anything from last frame
    screen.blit(backgroundImage, (0, 0))
   
    # Updates the positions and draws all entities on screen
    entityManager.Update(screen)

    keys = pygame.key.get_just_pressed()
    
    if (keys[pygame.K_SPACE] or (mouseClick and GameState==1)):
        bird.Flap()
        flapSFX.play()
    elif bird.isDead == False:
        bird.FlapBurnOff()
        
    if keys[pygame.K_SPACE]:
        if GameState == 0:
            StartGame()
        elif GameState == 2:
            SetStartScreen()
            
    # Checks if the bird collided with the ground of the pipes
    if entityManager.DoesEntityCollide(bird) and bird.isDead == False:
        print("Bird Collided")
        bird.isDead = True
        hitSFX.play()
        if bird.y < screenHeight - 200:
            fallSFX.play()
        # Resets the game(pipes, score, etc) to start the game again
        pipeManager.StopPipes()
        GameState = 2
        SetDeathScreen()

    if GameState == 0:
        deathScreenShown = False
        startScreenShown = True
    elif GameState == 1:
        pipeManager.Update()
        scoreText = font.render(f"Score: {scoreManager.score}\nBest Score: {scoreManager.bestScore}", True, "white")
        screen.blit(scoreText, (screenWidth // 2 - 50, 10))
        deathScreenShown = False
        startScreenShown = False
    elif GameState == 2:
        deathScreenShown = True
        startScreenShown = False
        
    if startScreenShown:
        startText = font.render("Flappy Bird", True, "white")
        rememberText = font.render("Yes" if rememberMe else "No", True, "white")
        screen.blit(startText, (screenWidth // 2, screenHeight * .35))
        screen.blit(rememberText, (screenWidth *.6, screenHeight * .55))

    elif deathScreenShown:
        deathText = font.render((f"New Best: {scoreManager.bestScore}!" if scoreManager.beatBestScore else f"Best Score: {scoreManager.bestScore}\nTry Again?"), True, "white")
        screen.blit(deathText, (screenWidth // 2, screenHeight * .4))
        
    # flip() the display to put your work on screen
    pygame.display.flip()
    # Updates the delta time for entity manager(for velocity)
    dt = clock.tick(60) / 1000  # limits FPS to 60
    entityManager.UpdateDeltaTime(dt)
    globalInfo.ResetTempInfo()
    
if account is not None:
    account["Bestscore"] = scoreManager.bestScore
    print(account)
    databaseHandler.UpdateAccount(account)
    
if account is None:
    account = {
        "Username":"",
        "Password":"",
    }

if account is not None:
    if rememberMe == False:
        account["Username"] = ""
        account["Password"] = ""
        
    accountInfo = {
        "AccountName": account["Username"],
    "AccountPassword": account["Password"],
    "RememberAccount": rememberMe
    }
    with open('SaveFile.json', "w", encoding='utf-8') as file:
        print(accountInfo)
        json.dump(accountInfo, file, indent=4)
    
    

pygame.quit()

