import pygame

class Snake:
    def __init__(self , screen , x , y , color , up , down , right , left , unit , width , height):
        
        self.UNIT = unit
        
        self.screen = screen
        self.color = color
        self.parts=[[x , y] ,
                    [x + self.UNIT , y] ,
                    [x + (self.UNIT * 2), y] , 
                    [x + (self.UNIT * 3), y]]
        
        self.up = up
        self.down = down
        self.right = right
        self.left = left
        
        self.goingright = True
        self.goingup = False
        self.goingdown = False
        self.goingleft = False
        
        self.touch = False
                
        self.WIDTH = width
        self.HEIGHT = height
        
    def move(self ):
        x , y = self.parts[-1]
        if not self.touch:
            self.parts.remove(self.parts[0])
        self.touch = False
        if self.goingright:
            if x + self.UNIT >= self.WIDTH:
                x = 0
            else:
                x += self.UNIT
        elif self.goingleft:
            if x - self.UNIT < 0:
                x = self.WIDTH
            else:
                x -= self.UNIT
        elif self.goingup:
            if y - self.UNIT < 0:
                y = self.HEIGHT
            else:
                y -= self.UNIT
        elif self.goingdown:
            if y + self.UNIT >= self.HEIGHT:
                y = 0
            else:
                y += self.UNIT
        self.parts.append([x , y])

    def draw(self):
        for part in self.parts:
            sur = pygame.Surface( (self.UNIT , self.UNIT) )
            if part == self.parts[-1]:
                sur.fill("black")
            else:
                sur.fill(self.color)
            sur_rect = sur.get_rect(topleft = (part[0] , part[1]))

            self.screen.blit(sur , sur_rect)

            pygame.draw.rect(self.screen ,"black", sur_rect , 1 , 0)
