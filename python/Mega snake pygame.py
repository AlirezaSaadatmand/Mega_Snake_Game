import pygame
from sys import exit
import random
import pyautogui

from classes.Snake import Snake
from classes.Food import Food

size = pyautogui.size()
WIDTH , HEIGHT = size
WIDTH , HEIGHT = (WIDTH*8//10) , (HEIGHT*8//10)

UNIT = 12

WIDTH -= WIDTH % UNIT
HEIGHT -= HEIGHT % UNIT

intro = True

GAME_DURATION = 100

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
             
def create_sanke(screen , count):
    xrange = WIDTH // UNIT
    yrange = HEIGHT // UNIT
    for i in range(1 , count+1):
        snakes.append(Snake(screen , random.randint(1, xrange-3) * UNIT , random.randint(1 , yrange-3) * UNIT , colors[i] , *moves[i] , UNIT , WIDTH , HEIGHT))

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
    foods.append(Food(screen , x , y , UNIT))

def win():
    s = ""
    count = 0
    for snake in snakes:
        if len(snake.parts) > count:
            count = len(snake.parts)
            s = snake.color
        elif len(snake.parts) == count:
            s += f" , {snake.color}"
    return s

def draw():
    if not gameOver:
        for food in foods:
            food.draw()
        for snake in snakes:
            snake.move()
            snake.draw()
        time_text = pygame.font.Font(None , 40)
        time_text = time_text.render(f"{counter // 120}" , "white" , True)
        screen.blit(time_text , (WIDTH - 50 , 30))
    else:
        screen.fill("#eee4da")
        screen.blit(end_game_surface , end_game_rect)
        pos = 1
        width = WIDTH // 1.5
        unit = width // (int(text) + 1)
        for snake in snakes:
            score_text = pygame.font.Font(None , 30)
            score_text = score_text.render(f"{snake.color} : {len(snake.parts)}" , "white" , True)
            score_text_rect = score_text.get_rect(center = ((WIDTH-width)/2 + pos*unit  , HEIGHT /2))
            screen.blit(score_text , score_text_rect)
            pos += 1
        win_text = pygame.font.Font(None , 60)
        win_text = win_text.render(f"{win()} player won!" , "white" , True)
        win_text_rect = win_text.get_rect(center = (WIDTH / 2 , HEIGHT / 8))
        screen.blit(win_text , win_text_rect)
        
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
screen.fill("#ede0c8")
clock = pygame.time.Clock()

begin_text = pygame.font.Font(None , 40)
begin_text = begin_text.render("How many snake ? (2 , 4)" , "black" , False)
begin_text_rect = begin_text.get_rect(center = (WIDTH / 2 , HEIGHT / 2 - 50))

sur = pygame.Surface( (100 , 30) )
sur.fill("#f59563")
sur_rect = sur.get_rect(center = (WIDTH / 2 , HEIGHT / 2))

end_game_surface = pygame.Surface( (WIDTH // 1.5 , HEIGHT // 4) )
end_game_surface.fill("#c1b3a4")
end_game_rect = end_game_surface.get_rect(center = (WIDTH // 2 , HEIGHT // 2))


counter = 0

text = ""

while True:
    pygame.display.set_caption(f"FPS : {round(clock.get_fps())} Mega Snake")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if event.type == pygame.KEYDOWN:
            if not intro:
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
            else:
                if event.unicode.isdigit():
                    text += str(event.unicode)
                if event.key == pygame.K_BACKSPACE and len(text) > 0:
                    text = text[:-1]
                if event.key == pygame.K_SPACE and 2 <= int(text) <= 4:
                    create_sanke(screen , int(text))
                    intro = False

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
    if intro:
        screen.blit(begin_text , begin_text_rect)
        screen.blit(sur , sur_rect)
        
        number_text = pygame.font.Font(None , 30)
        number_text = number_text.render(text , "black" , True)
        number_text_rect = number_text.get_rect(center = (WIDTH / 2 , HEIGHT / 2))
        screen.blit(number_text , number_text_rect)
    else:
        if not gameOver:
            
            if counter % 12 == 0:
                screen.fill("#ede0c8")
                
                while len(foods) < food_count:
                    create_food(screen)
                touch()
                draw()
                if counter == GAME_DURATION * 120:
                    gameOver = True
            counter += 1 
        else:
            draw()
    pygame.display.update()
    clock.tick(120)