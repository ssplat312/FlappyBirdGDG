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
from functools import partial
from Network import Network
from packets import Packet
from pathlib import Path

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
    global isReady
    
    isReady = False
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
    global username
    testUsername = usernameInput.text
    password = passwordInput.text
    if databaseHandler.UserNameIsTaken(testUsername):
        GetAccountInfo(testUsername, password)
    else:
        CreateAccount(testUsername, password)
    
    if account is not None:
        username = testUsername
    SetLoginUIViz()

    
def ToggleRememberMe():
    global rememberMe
    rememberMe = rememberMe == False
    
def SetBirdColor(curColor:int):
    global bird
    global birdColor
    birdColor = curColor
    frames = []
    
    if birdColor == 0:
        frames = ["Assets/sprites/yellowbird-downflap.png", "Assets/sprites/yellowbird-midflap.png", "Assets/sprites/yellowbird-upflap.png", "Assets/sprites/yellowbird-midflap.png"]
    elif birdColor == 1:
        frames = ["Assets/sprites/bluebird-downflap.png", "Assets/sprites/bluebird-midflap.png", "Assets/sprites/bluebird-upflap.png", "Assets/sprites/bluebird-midflap.png"]
    else:
        frames = ["Assets/sprites/redbird-downflap.png", "Assets/sprites/redbird-midflap.png", "Assets/sprites/redbird-upflap.png", "Assets/sprites/redbird-midflap.png"]

    bird.SetFramesImages(frames)


def GetBirdFrames(birdColor:int):
    frames = []
        
    if birdColor == 0:
        frames = ["Assets/sprites/yellowbird-downflap.png", "Assets/sprites/yellowbird-midflap.png", "Assets/sprites/yellowbird-upflap.png", "Assets/sprites/yellowbird-midflap.png"]
    elif birdColor == 1:
        frames = ["Assets/sprites/bluebird-downflap.png", "Assets/sprites/bluebird-midflap.png", "Assets/sprites/bluebird-upflap.png", "Assets/sprites/bluebird-midflap.png"]
    else:
        frames = ["Assets/sprites/redbird-downflap.png", "Assets/sprites/redbird-midflap.png", "Assets/sprites/redbird-upflap.png", "Assets/sprites/redbird-midflap.png"]

    return frames

def DrawOtherBird(x:int, y:int,birdColor:int, frameNumber:int, otherUsername:str,otherRank:int):
    global screen
    global bird
    global font
    frameLink = GetBirdFrames(birdColor)[frameNumber]
        
    filePath = Path(frameLink)
    
    if(filePath.is_file() == False):
        return
    
    frame = pygame.image.load(frameLink).convert_alpha()
    frame.set_alpha(127)
    frame = pygame.transform.scale(frame, (bird.width, bird.height))
    screen.blit(frame, (x,y))

    usernameTextInput = otherUsername
    
    if inMultiplayer:
        usernameTextInput = f"{otherUsername} - {otherRank}"
    
    userNameText = font.render(usernameTextInput, True, (255,255,255))
    userNameText.set_alpha(127)
    namePos = (x,y)
    namePos = (int(namePos[0] ), int(namePos[1]) + 50)
    screen.blit(userNameText, namePos)

def DrawPipe(x,y,width,height,isTop):
    global screen
    link = "Assets/sprites/pipe-green.png"
        
    filePath = Path(link)
    
    if(filePath.is_file() == False):
        return
    
    frame = pygame.image.load(link).convert_alpha()
    
    frame = pygame.transform.scale(frame, (width, height))
    frame = pygame.transform.flip(frame, False, isTop)
    screen.blit(frame, (x,y))

def GetRankFromPackets(packetList:list[Packet]):
    global scoreManager
    global packet
    curRanking = packet.playerCount
    
    for otherPacket in packetList:
        if otherPacket is None:
            continue
        
        if otherPacket.birdScore < scoreManager.score:
            curRanking -= 1
        elif otherPacket.birdScore == scoreManager.score and otherPacket.isDead:
            curRanking -= 1
            
    return curRanking

def GetOtherRankFromPackets(mainPacket:Packet,packetList:list[Packet]):
    global scoreManager
    global packet
    global bird
    curRanking = packet.playerCount
    
    if scoreManager.score < mainPacket.birdScore:
        curRank -= 1
    elif scoreManager.score == mainPacket.birdScore and bird.isDead:
        curRanking -= 1
                
    
    for otherPacket in packetList:
        if otherPacket is None:
            continue
        if otherPacket.username == mainPacket.username:
            continue
        
        if otherPacket.birdScore < mainPacket.birdScore:
            curRanking -= 1
        elif otherPacket.birdScore == mainPacket.birdScore and otherPacket.isDead:
            curRanking -= 1
            
    return curRanking

#Checks if atleast 2 people are alive
def CanResetMultiplayerGame(packetList:list[Packet]):    
    global bird
    aliveCount = 0
    if bird.isDead == False:
        aliveCount += 1
        
    if isReady == False:
        return True
    
    
    for otherPacket in packetList:
        if otherPacket is None:
            continue
        
        if otherPacket.isDead == False:
            aliveCount += 1
            
        if otherPacket.isReady == False:
            return True
        
    if aliveCount < 2:
        return True
    
    return False
    
    

def DrawPacket(curPacket:Packet, rank):
    curPacket.PrintInfo()
    DrawOtherBird(curPacket.birdPos[0], curPacket.birdPos[1], curPacket.birdColor, curPacket.birdFrame, curPacket.username, rank)

def DrawPacketFullInfo(curPacket:Packet):
    pass

def MutiplayerToggle():
    global network
    global inMultiplayer
    if inMultiplayer:
        inMultiplayer = False
        network.DisconnectNetwork()
    else:
        inMultiplayer = True
        network.SetUpNetwork()

def HandleMultiplayer():
    global network
    global birdColor
    global bird
    global scoreManager
    global username
    global packet
    global pipeManager
    global pipeFrame 
    global isReady
    global GameState
    global curRank
    
    pipeFrame += 1
    pipeInfos = []
    if pipeFrame >= 5:
        pipeInfos = pipeManager.GetPipesPacketInfo()
        pipeFrame = 0
    packet.SetInfo(birdColor,bird.curFrame,bird.GetTopLeftConner(),bird.isDead,pipeInfos,scoreManager.score, username,packet.playerCount, packet.readyCount,isReady)
    otherPackets = network.send(packet)
    if otherPackets is None:
        return

    #When showing the pipe info make it empty and then update it every couple of frames
    for otherPacket in otherPackets:
        rank = GetOtherRankFromPackets(otherPacket, otherPackets)
        DrawPacket(otherPacket, rank)
    
    canReset = CanResetMultiplayerGame(otherPackets)
            
    if GameState != 0:
        curRank = GetRankFromPackets(otherPackets)
        if canReset:
            SetStartScreen()
        return
    

        
        
    everyoneReady = isReady
    
    if everyoneReady:
        for packet in otherPackets:
            if packet.isReady == False:
                everyoneReady = False
                break
    if everyoneReady:
        StartGame()         
    
    

# pygame setup
screenWidth = GlobalInfo.screenWidth
screenHeight = GlobalInfo.screenHeight
GameState = 1  # 0 is start, 1 is game playing, 2 is death, for the ui
curRank = 0
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
inMultiplayer = False
isReady = False

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
birdColor = 0


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
yellowBirdButton = Button(partial(SetBirdColor, 0),text="",normalColor=(255,255,0), clickColor=(255,255,0),hoverColor=(255,255,0),name="YellowBird", x=100, y=screenHeight*.4,width=100, height=100)
blueBirdButton = Button(partial(SetBirdColor, 1), text="",color=(0,0,255),clickColor=(0,0,255),hoverColor=(0,0,255), name="BlueBird", x=100, y=screenHeight*.5,width=100, height=100)
redBirdButton = Button(partial(SetBirdColor, 2), text="",color=(255,0,0),clickColor=(255,0,0),hoverColor=(255,0,0), name="RedBird", x=100, y=screenHeight*.6,width=100, height=100)
multiplayerButton = Button(MutiplayerToggle,text="Multiplayer Toggle",color=(0,0,0),clickColor=(0,0,0),hoverColor=(0,0,0),normalColor=(0,0,0),x=150,y=screenHeight*.7, width=300, height=50)
startUI.append(yellowBirdButton)
startUI.append(blueBirdButton)
startUI.append(redBirdButton)
startUI.append(multiplayerButton)

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
    birdColor = saveFile["BirdColor"]

SetBirdColor(birdColor)
account = None

if rememberMe:
    account = databaseHandler.GetAccount(username, password)
    if account:
        scoreManager.bestScore = account["Bestscore"]
        logined = True


globalInfo = GlobalInfo()

packet = Packet()
#packet.SetInfo(birdColor,0,bird.GetPosition(),False,[],scoreManager.score, username,1,0,False)
network = Network()
#network.send(packet)

prevPipeInfo = []
pipeFrame = 0

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
   
    if inMultiplayer:
        HandleMultiplayer()
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
            if inMultiplayer == False:
                StartGame()
            else:
                isReady = True
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
    
    usernameTextInput = username
    
    if inMultiplayer:
        usernameTextInput = f"{username} - {curRank}"
        
    userNameText = font.render(usernameTextInput, True, "white")
    namePos = bird.GetPosition()
    namePos = (int(namePos[0] - bird.width//2), int(namePos[1]) + 40)
    screen.blit(userNameText, namePos)
    if startScreenShown:
        startText = font.render("Flappy Bird", True, "white")
        rememberText = font.render("Yes" if rememberMe else "No", True, "white")
        multiplayerText = font.render("Yes" if inMultiplayer else "No", True, "black")
        screen.blit(startText, (screenWidth // 2, screenHeight * .35))
        screen.blit(rememberText, (screenWidth *.6, screenHeight * .55))
        screen.blit(multiplayerText, (200, screenHeight * .75))
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
    "RememberAccount": rememberMe,
    "BirdColor":birdColor
    }
    
    with open('SaveFile.json', "w", encoding='utf-8') as file:
        print(accountInfo)
        json.dump(accountInfo, file, indent=4)
    
    

pygame.quit()

