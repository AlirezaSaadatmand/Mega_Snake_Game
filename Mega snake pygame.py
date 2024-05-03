import pygame
from sys import exit
import random
import pyautogui

size = pyautogui.size()
WIDTH , HEIGHT = size
WIDTH , HEIGHT = (WIDTH*8//10) , (HEIGHT*8//10)

UNIT = 12

WIDTH -= WIDTH % UNIT
HEIGHT -= HEIGHT % UNIT

snakes = []

foods = []

gameOver = False

food_count = 10

colors = {
    1 : "red",
    2 : "green",
    3 : "blue",
    4 : "yellow"
}

moves = {
    1 : [119 , 115 , 100 , 97],
    2 : [1073741906 , 1073741905 , 1073741903 , 1073741904],
    3 : [116 , 103 , 104 , 102],
    4 : [111 , 108 , 59 , 107]
}

class Snake:
    def __init__(self , screen , x , y , color , up , down , right , left):
        self.screen = screen
        self.color = color
        self.parts=[[x , y] ,
                    [x + UNIT , y] ,
                    [x + (UNIT * 2), y] , 
                    [x + (UNIT * 3), y]]
        
        self.up = up
        self.down = down
        self.right = right
        self.left = left
        
        self.goingright = True
        self.goingup = False
        self.goingdown = False
        self.goingleft = False
        
        self.touch = False
        
    def move(self ):
        x , y = self.parts[-1]
        if not self.touch:
            self.parts.remove(self.parts[0])
        self.touch = False
        if self.goingright:
            if x + UNIT >= WIDTH:
                x = 0
            else:
                x += UNIT
        elif self.goingleft:
            if x - UNIT < 0:
                x = WIDTH
            else:
                x -= UNIT
        elif self.goingup:
            if y - UNIT < 0:
                y = HEIGHT
            else:
                y -= UNIT
        elif self.goingdown:
            if y + UNIT >= HEIGHT:
                y = 0
            else:
                y += UNIT
        self.parts.append([x , y])

    def draw(self):
        for part in self.parts:
            sur = pygame.Surface( (UNIT , UNIT) )
            if part == self.parts[-1]:
                sur.fill("black")
            else:
                sur.fill(self.color)
            sur_rect = sur.get_rect(topleft = (part[0] , part[1]))

            self.screen.blit(sur , sur_rect)

            pygame.draw.rect(self.screen ,"black", sur_rect , 1 , 0)

class Food:
    def __init__(self , screen , x , y):
        self.screen = screen
        self.x = x
        self.y = y
    def draw(self):
        sur = pygame.Surface( (UNIT , UNIT) )
        sur.fill("red")
        sur_rect = sur.get_rect(topleft = (self.x , self.y))
        self.screen.blit(sur , sur_rect)
                
def create_sanke(screen , count):
    xrange = WIDTH // UNIT
    yrange = HEIGHT // UNIT
    for i in range(1 , count+1):
        snakes.append(Snake(screen , random.randint(1, xrange-3) * UNIT , random.randint(1 , yrange-3) * UNIT , colors[i] , *moves[i]))

def create_food(screen):
    x = random.randint(0 , WIDTH // UNIT) * UNIT
    y = random.randint(0 , HEIGHT // UNIT) * UNIT
    while True:
        for snake in snakes:
            if [x , y] in snake.parts:
                x = random.randint(0 , WIDTH // UNIT) * UNIT
                y = random.randint(0 , HEIGHT // UNIT) * UNIT
                break
        else:
            break
    foods.append(Food(screen , x , y))

def draw():
    for food in foods:
        food.draw()
    for snake in snakes:
        snake.move()
        snake.draw()
    time_text = pygame.font.Font(None , 40)
    time_text = time_text.render(f"{counter // 120}" , "white" , True)
    screen.blit(time_text , (WIDTH - 50 , 30))
    
def all_false(snake):
    snake.goingup = False
    snake.goingdown = False
    snake.goingright = False
    snake.goingleft = False    

def touch():
    global foods
    global snakes
    for food in foods:
        for snake in snakes:
            if [food.x , food.y] == snake.parts[-1]:
                foods.remove(food)
                snake.touch = True
                break

pygame.init()
screen = pygame.display.set_mode( (WIDTH , HEIGHT) )
screen.fill("orange")
pygame.display.set_caption("Mega Snake")
clock = pygame.time.Clock()

create_sanke(screen , 3)

counter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if event.type == pygame.KEYDOWN:
            for snake in snakes:
                lst = [snake.goingup , snake.goingdown , snake.goingright , snake.goingleft]
                f = [snake.up , snake.down , snake.right , snake.left]
                if event.key in f:
                    index = f.index(event.key)

                    if index == 0 and snake.goingdown == False:
                        all_false(snake)                  
                        snake.goingup = True
                    elif index == 1 and snake.goingup == False:
                        all_false(snake)                  
                        snake.goingdown = True
                    elif index == 2 and not snake.goingleft:
                        all_false(snake)                  
                        snake.goingright = True
                    elif index == 3 and not snake.goingright:
                        all_false(snake)                  
                        snake.goingleft = True
            
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
    
    if not gameOver:
        
        if counter % 12 == 0:
            screen.fill("green")
            
            while len(foods) < food_count:
                create_food(screen)
            touch()
            draw()
            if counter == 12000:
                gameOver = True
    else:
        ...
    counter += 1 
    pygame.display.update()
    clock.tick(120)