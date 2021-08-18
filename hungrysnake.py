import pygame
from pygame.locals import *
from pygame import mixer
import random
import time

# initialize
pygame.init()

bottom_panel = 100
screen_width = 600
screen_height = 600 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hungry Snake')

# set backsong
mixer.init()
mixer.music.load("backsound\The-Ant-Hill-Gang-Goes-West.mp3")
mixer.music.play(loops = -1)

#define font
font = pygame.font.SysFont('04B_19.ttf', 50)
font2 = pygame.font.SysFont('04B_19.ttf', 30)
#setup a rectangle for "Play Again" Option
again_rect = Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)

# timer
clock = pygame.time.Clock()
counter, text = 60, '60'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)

#define snake variables
snake_pos = [[int(screen_width / 2), int(((screen_height - bottom_panel) / 2))]]
snake_pos.append([300,310])
snake_pos.append([300,320])
snake_pos.append([300,330])
snake_pos.append([300,340])
direction = 1 #1 is up, 2 is right, 3 is down, 4 is left

#load images
cover_img = pygame.image.load((r'img\cover.png')).convert_alpha()
start_img = pygame.image.load((r'img\startbutton.png')).convert_alpha()
background_img = pygame.image.load((r'img\bg.png')).convert_alpha()
apple_img = pygame.image.load((r'img\apple.png')).convert_alpha()
mushroom_img = pygame.image.load((r'img\mushroom.png')).convert_alpha()
stone_img = pygame.image.load((r'img\stone.png')).convert_alpha()
potion_img = pygame.image.load((r'img\potion.png')).convert_alpha()
head = pygame.image.load((r'img\head.png')).convert_alpha()
body = pygame.image.load((r'img\snake.png')).convert_alpha()
panel = pygame.image.load((r'img\panel.png')).convert_alpha()
panel2 = pygame.image.load((r'img\panel2.png')).convert_alpha()

#define game variables
cell_size = 60
update_snake = 0
food_apple = [0,0]
food_mushroom = [0,0]
food_stone = [0,0]
food_potion = [0,0]
new_food = True
game_over = False
clicked = False
start_game = False
start_song = False
score = 0
high_score = 0
fps = 1000

#define colors
bg = (255, 200, 150)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
brown = (100,40,0)
yellow = (255, 255, 0)
gray = (127, 127, 127)
purple = (240, 0, 255)

# Function
def draw_screen():
    screen.blit(background_img, (0,0))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def draw_panel():
    # draw panel rectangles
    screen.blit(panel, (0, (screen_height - bottom_panel)))
    # show score
    draw_text(f'Score : {str(score)}', font, red, 40, (screen_height - bottom_panel) + 20)
    draw_text(f'Timer : {counter}', font, red, 400, (screen_height - bottom_panel) + 20 )
    draw_text(f'High Score : {high_score}', font2, black, 230, (screen_height - bottom_panel) + 60 )

def check_game_over(game_over):
    # timer
    if counter == 0:
        game_over = True

    #second check is to see if the snake has gone out of bounds
    if snake_pos[0][0] < 0 or snake_pos[0][0] > screen_width or snake_pos[0][1] < 0 or snake_pos[0][1] > 540:
        game_over = True 

    return game_over

def draw_game_over():

    # function of game over comment
    def game_over_comment(comment, valueX, valueY):
        over_text = comment
        over_img = font2.render(over_text, True, brown)
        screen.blit(panel2, (35, 170))
        screen.blit(over_img, ((screen_width // 2) - valueX, (screen_height // 2) - valueY))
    
    # comment condition
    if score >= 25:   
        game_over_comment("Yummy! I am full and healty!", 140, 90)

    elif score >= 15 and score < 25:
        game_over_comment("Nice! But you eat some poisonous mushroom!", 210, 90) 

    elif score > 8 and score < 15:
        game_over_comment("Good! Still a little bit hungry", 130, 90)

    else:
        game_over_comment("Blehh!You will get ill because of starving!", 200, 90)

    again_text = 'Play Again?'
    again_img = font.render(again_text, True, blue)
    pygame.draw.rect(screen, red, again_rect)
    screen.blit(again_img, (screen_width // 2 - 100, screen_height // 2 + 5))

run = True
while run:

    clock.tick(fps)

    if start_game == False:
        #draw menu
        screen.blit(cover_img, (0,0))
        # add buttons
        screen.blit(start_img, (screen_width // 2 - 100, screen_height // 2 - 100))
        for event2 in pygame.event.get():
            if event2.type == pygame.QUIT:
                run = False
            if event2.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event2.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                start_game = True
                start_song = True

    else:
        draw_screen()
        draw_panel()
   
        # High score
        if high_score < score:
            high_score = score

        #create food
        if new_food == True:
            new_food = False
            food_apple[0] = cell_size * random.randint(0, ((screen_height - bottom_panel) / cell_size) - 1)
            food_apple[1] = cell_size * random.randint(0, ((screen_height - bottom_panel) / cell_size) - 1)
            food_mushroom[0] = cell_size * random.randint(0, ((screen_height - bottom_panel) / cell_size) - 1)
            food_mushroom[1] = cell_size * random.randint(0, ((screen_height - bottom_panel) / cell_size) - 1)
            food_stone[0] = cell_size * random.randint(0, ((screen_height - bottom_panel) / cell_size) - 1)
            food_stone[1] = cell_size * random.randint(0, ((screen_height - bottom_panel) / cell_size) - 1)
            food_potion[0] = cell_size * random.randint(0, ((screen_height - bottom_panel)/ cell_size) - 1)
            food_potion[1] = cell_size * random.randint(0, ((screen_height - bottom_panel)/ cell_size) - 1)

        #draw food 
        screen.blit(apple_img, (food_apple[0],food_apple[1]))
        screen.blit(mushroom_img, (food_mushroom[0],food_mushroom[1]))
        screen.blit(stone_img, (food_stone[0],food_stone[1]))
        screen.blit(potion_img, (food_potion[0],food_potion[1]))


        #check if food has been eaten
        if snake_pos[0] == food_apple:
            fps = 1000
            new_food = True
            score += 3

        if snake_pos[0] == food_mushroom:
            fps = 1000
            new_food = True
            score -= 2

        if snake_pos[0] == food_stone:
            fps = 60
            new_food = True
            score += 0
            counter -= 5

        if snake_pos[0] == food_potion:
            fps = 5000
            new_food = True
            score += 1
            counter += 5

        if game_over == False:
            #update snake
            if update_snake > 99:
                update_snake = 0
                #first shift the positions of each snake piece back.
                snake_pos = snake_pos[-1:] + snake_pos[:-1]
                #now update the position of the head based on direction
                #heading up
                if direction == 1:
                    snake_pos[0][0] = snake_pos[1][0]
                    snake_pos[0][1] = snake_pos[1][1] - cell_size
                #heading down
                if direction == 3:
                    snake_pos[0][0] = snake_pos[1][0]
                    snake_pos[0][1] = snake_pos[1][1] + cell_size
                #heading right
                if direction == 2:
                    snake_pos[0][1] = snake_pos[1][1]
                    snake_pos[0][0] = snake_pos[1][0] + cell_size
                #heading left
                if direction == 4:
                    snake_pos[0][1] = snake_pos[1][1]
                    snake_pos[0][0] = snake_pos[1][0] - cell_size
                game_over = check_game_over(game_over)
            

        if game_over == True:
            draw_game_over()
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                 #reset variables
                game_over = False
                update_snake = 0
                food = [0, 0]
                new_food = True
                #define snake variables
                snake_pos = [[int(screen_width / 2), int((screen_height - bottom_panel)/ 2)]]
                snake_pos.append([300,310])
                snake_pos.append([300,320])
                snake_pos.append([300,330])
                snake_pos.append([300,340])
                direction = 1 #1 is up, 2 is right, 3 is down, 4 is left
                score = 0
                counter = 60
                fps = 1000

        head_snake = 1
        for i in range(5):
            if head_snake == 0:
                screen.blit(body, (snake_pos[i][0], snake_pos[i][1]))
                screen.blit(head, (snake_pos[0][0], snake_pos[0][1]))			
            if head_snake == 1:
                screen.blit(body, (snake_pos[i][0], snake_pos[i][1]))
                screen.blit(head, (snake_pos[0][0], snake_pos[0][1]))  


    for event in pygame.event.get():   
        if event.type == pygame.USEREVENT:
            if start_game == True:
                counter -= 1
                text = str(counter).rjust(3)
                if game_over == True:
                    counter = 0
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3:
                direction = 1
            if event.key == pygame.K_RIGHT and direction != 4:
                direction = 2
            if event.key == pygame.K_DOWN and direction != 1:
                direction = 3
            if event.key == pygame.K_LEFT and direction != 2:
                direction  = 4

    pygame.display.update()

    update_snake += 1
    pygame.display.flip()
    
pygame.quit()