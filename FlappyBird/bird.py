from entity import ObjectEntety
from time import time


#The bird is an extension of the object ententy that has gravity and specilized controls
class Bird(ObjectEntety):

    def __init__(self, name="", color="", x=0, y=0, imgLink="", width=1, height=1, xVel=0, yVel=0, colPercentage=1, maxYVel=10, maxFallSpeed=10, flapStrength=2, maxFlapTime=1, gravity=1):
        super().__init__(name, color, x, y, imgLink, width, height, xVel, yVel, colPercentage)
        self.gravity = gravity
        self.flapStrength = flapStrength
        self.maxYVelocity = maxYVel
        self.lastFlapTime = time()
        self.maxFlapTime = maxFlapTime
        self.maxFallSpeed = maxFallSpeed
        self.burnOffTime = time()
        self.maxBurnOffTime = .1
        self.justFlapped = False
        self.isDead = False
        
    #Updates the y velocity of the bird and determines if it should fall or not
    def Update(self):
        
        if(time() - self.lastFlapTime) > self.maxFlapTime:
            tempYVel = self.GetYVelocity()
            tempYVel -= self.gravity
            if(-tempYVel > self.maxFallSpeed):
                tempYVel = -self.maxFallSpeed
            self.UpdateYVelocity(tempYVel)
        
        super().Update()
        
    #Sets a timer that makes it so it flies until a set time
    def Flap(self):
        self.burnOffTime = time() 
        self.lastFlapTime = time() 
        self.UpdateYVelocity(self.flapStrength)
        self.justFlapped = True
     
    #Ensures that the bird stays at the same y pos for some time   
    def FlapBurnOff(self):
        if self.justFlapped == False:
            return
        
        self.lastFlapTime = time()
        if time() - self.burnOffTime < self.maxBurnOffTime:
            return
        
        self.UpdateYVelocity(0)
        self.justFlapped = False

    #Forces the bird into the burn off state
    def ForceBurnOff(self):
        self.burnOffTime = time() 
        self.lastFlapTime = time()
        self.justFlapped = True
