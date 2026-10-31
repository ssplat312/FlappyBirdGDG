from entity import ObjectEntety
import pygame
from GlobalInfo import GlobalInfo

class TextInputBox(ObjectEntety):

    def __init__(self, name="", color="red", x=0, y=0, imgLink="", width=1, height=1, xVel=0, yVel=0, colliderPercentage=1, frameLinks=[], animationSpeed=10, decorText="",textColor=(255,255,255), activeColor=(255, 255, 255), inactiveColor=(255, 255, 255)):
        super().__init__(name, color, x, y, imgLink, width, height, xVel, yVel, colliderPercentage, frameLinks, animationSpeed)
        
        self.isActive = False
        self.inactiveColor = inactiveColor
        self.activeColor = activeColor
        self.color = inactiveColor
        self.text = ""
        self.decorText = decorText
        self.textColor = textColor
        self.font = pygame.font.Font(None, 32) 
        self.txt_surface = self.font.render(decorText+self.text, True, (0,0,0))

    def Update(self):
        self.EventHandle()
        super().Update()
    
    def EventHandle(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = GlobalInfo.mouseClick
        inRange =  self.InRnageOfPoint(mouse_pos)
        
        if mouse_click and inRange:
            self.isActive = self.isActive == False            
            self.color = self.activeColor if self.isActive else self.inactiveColor
        elif inRange:
            self.color = self.activeColor
        elif mouse_click and inRange == False:
            self.isActive = False
            self.color = self.inactiveColor
                        
        if GlobalInfo.pressedKey:
            if self.isActive:
                if GlobalInfo.curKey == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # event.unicode gets the exact character typed
                    self.text += GlobalInfo.curUnicode
                
                # Re-render the text surface
                self.txt_surface = self.font.render( self.decorText + self.text, True, self.textColor)

    def Draw(self, screen):
        if self.hidden:
            return
        
        pygame.draw.rect(screen, self.color, self.GetRect())
        # Blit the text surface onto the screen inside our box
        screen.blit(self.txt_surface, (self.x - self.width//2, self.y + 5))
        # Draw the bounding rectangle outline
