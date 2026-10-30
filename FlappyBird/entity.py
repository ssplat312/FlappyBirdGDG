from GlobalInfo import GlobalInfo
from math import sqrt, pow
from time import time
import pygame
from pathlib import Path
#An entity holder for pygames object that contains it's name, color, position(center), dimensions, etc.
#For future note if you wanted to reduce the collider size you would need to lerp between the objects x and y position and it's conner position
class ObjectEntety():
    globalID = 0
    dt = 0

    def __init__(self, name="", color="red", x=0, y=0, imgLink="", width=1, height=1, xVel=0, yVel=0, colliderPercentage=1, frameLinks =[],animationSpeed=10):
        self.id = ObjectEntety.globalID
        ObjectEntety.globalID = ObjectEntety.globalID + 1
        self.name = name
        self.color = color
        self.x = x  # X and Y are the top left positions
        self.y = y
        self.imgLink = imgLink
        self.animationFrames = []
        self.SetFramesImages(frameLinks)
        self.animationSpeed = animationSpeed#By frame count
        self.curFrame = 0
        self.frameCount = 0
        self.width = width
        self.height = height
        self.isFlipped = False
        self.velocity = (xVel, yVel)
        self.colliderPercentage = colliderPercentage
        self.hidden = False
        
    def Draw(self, screen):
        if self.hidden:
            return
        pygame.draw.rect(screen, self.color, self.GetRect())

    def DrarFrames(self, screen):
        if self.hidden:
            return 
        screen.blit(self.GetFrame(), self.GetTopLeftConner())

        
    def SetFramesImages(self, frameLinks, flipHorizontal=False, flipVertical=False):
        self.animationFrames = []
        for link in frameLinks:
            filePath = Path(link)
            
            if(filePath.is_file() == False):
                continue
            
            frame = pygame.image.load(link).convert_alpha()
            
            frame = pygame.transform.scale(frame, (self.width, self.height))
            if flipHorizontal or flipVertical:
                frame = pygame.transform.flip(frame, flipHorizontal, flipVertical)
            self.animationFrames.append(frame)
            
        
    #Determines if the entity is out of screen bounds
    def InScreenBoundries(self):
        minX = 0
        maxX = GlobalInfo.screenWidth
        minY =  0
        maxY = GlobalInfo.screenHeight
        
        return minX < self.x and maxX > self.x and minY < self.y and maxY > self.y
    
    #Gets the name of the object
    def GetObjectName(self):
        return self.name
    
    #Gets the position of the object in tuple form
    def GetPosition(self):
        return (self.x, self.y)
    
    #Gets the top left conner of the object(mainly for when drawing on screen)
    def GetTopLeftConner(self):
        return (self.x - self.width/2, self.y - self.height/2)
    
    #Gets the conners of the object(for collision detection)
    def GetConnerPositions(self):
        return [ (self.x - self.width/2, self.y - self.height/2), (self.x + self.width/2, self.y - self.height/2), (self.x + self.width/2, self.y + self.height/2), (self.x - self.width/2, self.y + self.height/2)]

    def GetColliderConners(self):
        position = self.GetPosition()
        conners = self.GetConnerPositions()
        return [LerpVec2(position,conners[0], self.colliderPercentage), LerpVec2(position,conners[1], self.colliderPercentage),LerpVec2(position,conners[2], self.colliderPercentage),LerpVec2(position,conners[3], self.colliderPercentage)]
    
    #Gets the rect of the object (x, y, width, height)
    def GetRect(self):
        leftConner = self.GetTopLeftConner()
        return (leftConner[0], leftConner[1], self.width, self.height)
    
    #Gets the velocity of the object (tuple[x, y])
    def GetVelocity(self):
        return self.velocity
    
    #Updates the position of the object(adds to x and takes away from y becasue going down increases y)
    def Update(self):
        self.x += (self.GetXVelocity() * self.dt)
        self.y -= (self.GetYVelocity() * self.dt)
        if len(self.animationFrames) > 0:
            self.UpdateFrame()
        
        
    def UpdateFrame(self):
        self.frameCount += 1
        
        if self.frameCount < self.animationSpeed:
            return
        
        self.frameCount = 0
        self.curFrame += 1
        
        if self.curFrame >= len(self.animationFrames):
            self.curFrame = 0
    
    
    def GetFrame(self):
        return self.animationFrames[self.curFrame]
        
    
    #Updates the x velocity
    def UpdateXVelocity(self, newX):
        self.velocity = (newX, self.GetYVelocity())
        
    #Updates the y velocity
    def UpdateYVelocity(self, newY):
        self.velocity = (self.GetXVelocity(), newY)
        
    #Gets the x velocity
    def GetXVelocity(self):
        return self.velocity[0]
    
    #Gets the y velocity
    def GetYVelocity(self):
        return self.velocity[1]
    
    def GetXDistance(self, other):
        return abs(other.x - self.x)
    
    def GetYDistance(self, other):
        return abs(other.y - self.y)

    def ShouldCheckCollision(self, other:ObjectEntety) -> bool:
        xDist = self.GetXDistance(other)
        yDist = self.GetYDistance(other)
        
        highWidth = max(self.width, other.width)//2 + 25
        highHeight = max(self.height, other.height)//2 + 25
        highColider = max(self.colliderPercentage, other.colliderPercentage)
        if highColider <= 0:
            highColider = 1
        return highWidth * highColider > xDist and highHeight * highColider > yDist
        
    #Gets the distance between 2 objects
    def GetDistance(self, other):
        return sqrt(pow(other.x - self.x, 2) + pow(other.y - self.y))
    
    def InRnageOfPoint(self, point):
        return abs(point[0] - self.x) <= self.width//2 and abs(point[1] - self.y) <= self.height//2
     
    # Detects if it's touching another object(box collider)
    def IsColliding(self, other) -> bool:
        return self._CheckCollision(other) or other._CheckCollision(self)
        
    #Checks if the object overlaps the other object
    def _CheckCollision(self, other) -> bool:
        minX = self.x - self.width / 2
        maxX = self.x + self.width / 2
        minY = self.y - self.height / 2
        maxY = self.y + self.height / 2
        
        otherConners = other.GetColliderConners()
        for conner in otherConners:
            if conner[0] > minX and conner[0] < maxX and conner[1] > minY and conner[1] < maxY:
                return  True
        return False
    
    def Hide(self):
        self.hidden = True
    
    def Show(self):
        self.hidden = False


def LerpVec2(a, b, t:float):
    xPos = (b[0] - a[0]) * t + a[0]
    yPos = (b[1] - a[1]) * t + a[1]
    return (xPos, yPos)

