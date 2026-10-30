import pygame
from entity import ObjectEntety

WHITE = (255,255,255)
class Button(ObjectEntety):
   
   
    def __init__(self,callback, name="", color="", x=0, y=0, imgLink="", width=1, height=1, xVel=0, yVel=0, colPercentage=1,frames=[],aniSpeed=10, text="Button", normalColor=(0,0,0), hoverColor=(0,0,0), clickColor=(0,0,0)):
        super().__init__(name, color, x, y, imgLink, width, height, xVel, yVel, colPercentage,frames,aniSpeed)
        self.text = text
        self.callback = callback
        self.normalColor = normalColor
        self.hoverColor = hoverColor
        self.clickColor = clickColor
        self.font = pygame.font.Font('freesansbold.ttf', 32)

        self.is_pressed = False
        self.canInteract = False

    def Draw(self, screen):
        if self.hidden:
            return
        # 1. Get mouse position and click status
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # 2. Determine button color based on interaction
        color = self.hoverColor

        if self.InRnageOfPoint(mouse_pos):
            if mouse_click[0]:  # Left click held down
                color = self.clickColor
                self.is_pressed = True
            else:
                color = self.hoverColor
                # Trigger action only when the user releases the click inside the button
                if self.is_pressed:
                    self.callback()
                    self.is_pressed = False
        else:
            self.is_pressed = False

        # 3. Draw the button body
        pygame.draw.rect(screen, color, self.GetRect(), border_radius=8)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.x,self.y))
        screen.blit(text_surface, text_rect)

        