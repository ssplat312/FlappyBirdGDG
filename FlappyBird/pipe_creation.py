from entity import ObjectEntety
from entity_manager import EntityManager
from GlobalInfo import GlobalInfo
from time import time
from random import randint
from ScoreManager import ScoreManager

#Handles creating pipes, adding score when passing pipes, and moving/adding new pipes to the right of the screen
class PipeManager():
    def __init__(self, newManager:EntityManager, scoreManager:ScoreManager, pointSFX,playerX=400):
        self.entityManager = newManager
        self.scoreManager = scoreManager
        self.pointSFX = pointSFX
        self.playerX = playerX
        self.pipeVelocity = 300
        self.pipeWidth = 150
        self.pipeHeight = GlobalInfo.screenHeight + 200
        self.distanceBetweenPipeSets = 300
        self.distanceBetweenPipeSets += self.pipeWidth
        self.spawnDelay = self.distanceBetweenPipeSets/self.pipeVelocity
        self.distanceBetweenPipesTops = 150 
        self.pipesStartX = GlobalInfo.screenWidth + 300
        self.pipesEndX = -100
        self.pipesInfo: list[tuple[ObjectEntety, ObjectEntety,bool]] = []  # [(topPipe, bottomPipe, midpoint, didPass)]
        self.pipeTime = time()
        
        #Prevents an extra pipe set from being made at the start
        self.CreatePipe()
        
    #Calls the midpoint checker and adds a pipe if needed
    def Update(self):
        self.CheckMidpoints()
        if self.NeedPipe():
            self.AddPipeAtEnd()
       
    #Checks if the pipe is to the left of the bird, and adds a point if it is
    def CheckMidpoints(self):   
        for pipeInfo in self.pipesInfo:
            if pipeInfo[0].x <= self.playerX and  pipeInfo[2] == False:
                pipeInfo[2] = True
                self.scoreManager.IncreaseScore()
                self.pointSFX.play()
        
    
    #Gets a random start y position for the pipes gap point
    def GetRandomPipeY(self):
        screenHeight = GlobalInfo.screenHeight
        
        return randint(self.distanceBetweenPipesTops, screenHeight - 200 - self.distanceBetweenPipesTops)
        
    #Gets the futhest pipe(pipe with lowest x)
    def GetFarthestPipeIndex(self):
        if len(self.pipesInfo) == 0:
            return -1
        x = 10000
        i = 0
        bestI = 0
        for pipeInfo in self.pipesInfo:
            if pipeInfo[0].x < x:
                x = pipeInfo[0].x
                bestI = i
            i += 1
            
        return bestI
    
    #Adds a pipe to the right of the screen if avaliable, otherwise creates a new one to add
    def AddPipeAtEnd(self):
        futherstIndex = self.GetFarthestPipeIndex()
        if futherstIndex < 0:
            self.CreatePipe()
            return
        futhestPipe = self.pipesInfo[futherstIndex]
        self.pipeTime = time()
        if futhestPipe is None or futhestPipe[0].x > self.pipesEndX:
            self.CreatePipe()
            return
        
        self.ResetPipeInfo(futherstIndex)
        
    
    #Creates a new pipe and puts it to the right of the screen.
    def CreatePipe(self):        
        topPipe = ObjectEntety(name="Top Pipe", color="green", x=self.pipesStartX, width=self.pipeWidth, height=self.pipeHeight,xVel=-self.pipeVelocity)
        bottomPipe = ObjectEntety(name="Bottom Pipe", color="green", x=self.pipesStartX, width=self.pipeWidth, height=self.pipeHeight,xVel=-self.pipeVelocity)
        
        bottomPipe.SetFramesImages(["FlappyBird/Assets/sprites/pipe-green.png"])
        topPipe.SetFramesImages(["FlappyBird/Assets/sprites/pipe-green.png"], flipVertical=True)
        
        newInfo: tuple[ObjectEntety, ObjectEntety,bool] = [topPipe, bottomPipe, False]
        self.entityManager.AddEntity(topPipe)
        self.entityManager.AddEntity(bottomPipe)
        self.pipesInfo.append(newInfo)
        self.ResetPipeInfo(len(self.pipesInfo) - 1)
        
        
    
    #Resets the pipe x and y positions, and resets its midpoint checker
    def ResetPipeInfo(self, index):
        usedInfo: tuple[ObjectEntety, ObjectEntety,bool] = self.pipesInfo[index]
        usedInfo[0].x = self.pipesStartX
        usedInfo[1].x = self.pipesStartX
        midY = self.GetRandomPipeY()
        
        usedInfo[0].y = midY - self.distanceBetweenPipesTops - self.pipeHeight/2
        usedInfo[1].y = midY + self.distanceBetweenPipesTops + self.pipeHeight/2
        
        usedInfo[2] = False
    
    #Removes every pipe from the entity manager, and adds a new one for the start of the game
    def FullPipesReset(self):#Reset for a new game
        self.pipeTime = time()
        for pipeInfo in self.pipesInfo:
            self.entityManager.RemoveEntity(pipeInfo[0])
            self.entityManager.RemoveEntity(pipeInfo[1])
            
        self.pipesInfo = []
        self.CreatePipe()
        self.pipeTime = time()
        
    #Checks if you need a new pipe
    def NeedPipe(self):
        return (time() - self.pipeTime) > self.spawnDelay
    