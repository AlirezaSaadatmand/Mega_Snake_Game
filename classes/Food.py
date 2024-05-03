import pygame

class Food:
    def __init__(self , screen , x , y , unit):
        self.screen = screen
        self.x = x
        self.y = y
        
        self.UNIT = unit
        
    def draw(self):
        sur = pygame.Surface( (self.UNIT , self.UNIT) )
        sur.fill("brown")
        sur_rect = sur.get_rect(topleft = (self.x , self.y))
        self.screen.blit(sur , sur_rect)
 
 
 