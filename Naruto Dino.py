#Importing libraries
import pygame
import random
import time
import math
import button

pygame.init()
clock = pygame.time.Clock()
FPS = 60

# screen variables
SCREENWIDTH = 1000
SCREENHEIGHT = 500

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Naruto Run')
pygame.display.set_icon(pygame.image.load('images/naruto_icon.png'))

#rankings and score
speed_list = ['not a num',4,3,2,2,1,1,1]
score = 0
score_show = 0
score_x = 400
score_size = 30
def rank_game(f_score):
    ranks = ('Genin', 'Chunin', 'Jonin', 'Elite Jonin', 'Kage','God Of Shinobi')
    # Genin 0 - 499, Chunin, 500 - 999, Jonin 1000 - 1499, Elite Jonin 1500 - 1999, Kage 2000-2499, G.O.S 2500+.
    ranks_score = f_score//500
    if ranks_score > 5: ranks_score = 5
    return ranks[ranks_score]

#text and music
def draw_text(use_font, text, color, px, py):
    writing = use_font.render(text,True,color)
    screen.blit(writing,(px,py))
x_font = 250
def size_font(size):
    font = pygame.font.Font('njnaruto.ttf', size)
    return font

#soundtracks
pygame.mixer.init()
end_song = pygame.mixer.Sound('music/wind.ogg')
naruto_sfx = pygame.mixer.Sound('music/play_song.ogg')
play_song = pygame.mixer.Sound('music/song1.ogg')
start_button_sfx = pygame.mixer.Sound('music/game_start.ogg')
totally_normal_sfx = pygame.mixer.Sound('music/totally_normal_sfx.ogg')

# function for button SFX
def button_sound(sfx):
    sfx.set_volume(0.3)
    vol = 0.1
    start_button_sfx.set_volume(vol)
    start_button_sfx.play()

    while vol < 1.0:
        start_button_sfx.set_volume(vol)
        vol += 0.1
    time.sleep(2)
    sfx.set_volume(1.0)

#tutorial
tutorial_space = False
tutorial_lshift = False
tutorial_Pause = False

# load and scale background
bg = pygame.image.load('images/background.png').convert_alpha()
bg = pygame.transform.scale(bg, (SCREENWIDTH // 2, SCREENHEIGHT))
bg_width = bg.get_width()
bg_lose =pygame.image.load('images/background1.png').convert_alpha()
bg_lose = pygame.transform.scale(bg_lose, (SCREENWIDTH, SCREENHEIGHT))
bg_start = pygame.image.load('images/background_start.png').convert_alpha()
bg_start = pygame.transform.scale(bg_start, (SCREENWIDTH, SCREENHEIGHT))


# define scroll variables
scroll = 0
tiles = math.ceil(SCREENWIDTH / bg_width) + 1

# jumping variables
jump_vel = 0
is_jumping = False
ground_y = 340
x = -0.5 # gravity acceleration

# obstacles
obstacle_speed = 10
choose_obs = 0
min_speed = 10
max_speed = 15
speed_increase = 0


#Sasuke obs
Sasuke_obs = pygame.image.load('images/sasuke.png').convert_alpha()
Sasuke_obs = pygame.transform.scale(Sasuke_obs, (125, 100))
Sasuke_rect = Sasuke_obs.get_rect()

#reducing his hitbox size
Sasuke_rect.width = int(Sasuke_obs.get_width()*.75)
Sasuke_rect.height = int(Sasuke_obs.get_height()*.75)

Sasuke_rect.topleft = (1000, ground_y - 10)

#kunai_obstacle
kunai_obs = pygame.image.load('images/kunai.png').convert_alpha()
kunai_obs = pygame.transform.scale(kunai_obs, (85, 85))
kunai_list = []
kunai_y_positions = [ground_y - 25, ground_y - 65, ground_y - 105, ground_y- 145, ground_y - 185, ground_y - 225]

# load and scale player
player = pygame.transform.scale((pygame.image.load('images/naruto.png').convert_alpha()), (100, 75))
player_rect = player.get_rect()
player_rect.width = int(player.get_width()*.8)
player_rect.height = int(player.get_height()*.8)
player_rect.topleft = (100, ground_y)
crawling = False

#crawling and running pos
crawling_player = pygame.transform.scale(pygame.image.load('images/naruto_crawl.png').convert_alpha(),(100,50))# בונאה איזו שורה ארוכה :(
standing_player = pygame.transform.scale(pygame.image.load('images/naruto.png').convert_alpha(),(100,75)) #בונאה איזו שורה ארוכה 2 :(

# buttons
Start_img = pygame.image.load('images/Start.png').convert_alpha()
button_start = button.Button(200, 200, Start_img, 1)
Finish_img = pygame.image.load('images/finish.png').convert_alpha()
button_finish = button.Button(600, 200, Finish_img, 1)
play_img = pygame.transform.scale(pygame.image.load('images/play_button.png').convert_alpha(), (200, 50))
Play_button = button.Button(int(SCREENWIDTH/2-120), 150, play_img, 1)

#popping title
title_y = 15075

# game loop
End_game = False
game = False
start_screen = True
Pause = False
nothing_special = False

#Start loop
play_song.play(loops = -1)
while start_screen:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: start_screen = False
        else: pass


    screen.blit(bg_start, (0,0))
    draw_text(size_font(50), 'Naruto Run', 'orange', 335, title_y)

    #rising title
    if title_y > 75: title_y -= 100
    else: title_y = 75

    if Play_button.draw(screen):
        button_sound(play_song)
        start_screen = False
        game = True
    pygame.display.update()

play_song.stop()
naruto_sfx.play(loops=-1)

#main loop
while game:
    clock.tick(FPS)

    # key inputs
    key = pygame.key.get_pressed()
    if (key[pygame.K_SPACE] or key[pygame.K_UP]) and not is_jumping:
        if not tutorial_space:
            tutorial_space = True
        is_jumping = True
        jump_vel = -20

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    #pause the game
    if key[pygame.K_ESCAPE] and not Pause:
        if not tutorial_Pause:
            tutorial_Pause = True
        Pause = True
        last_press = pygame.time.get_ticks()
        naruto_sfx.stop()
        end_song.play()

    #nothing to see here
    if key[pygame.K_F3] and key[pygame.K_F4]:
        nothing_special = True

    while nothing_special:
        naruto_sfx.stop()
        score = 5000
        totally_normal_text = ('How did you know ?', "you cheated didn't you ?", 'Well, Guess you won...')

        for i in totally_normal_text:
            screen.fill((100,125,150))
            if i == 'Well, Guess you won...':
                x_font = 220
                totally_normal_sfx.play()
            draw_text(size_font(50), i, 'black', x_font, 200)
            x_font = 200
            pygame.display.update()
            time.sleep(2.25)
        End_game = True
        nothing_special = False

    #crawling
    if key[pygame.K_LSHIFT] or key[pygame.K_DOWN]:
        crawling = True
        if not tutorial_lshift:
            tutorial_lshift = True

    if crawling:
        player = crawling_player
        player_rect.y = ground_y+25
        is_jumping = False
        crawling = False
        x = -0.5

    #return to running pos
    else:
        player = standing_player
        if player_rect.y > ground_y:
            player_rect.y = ground_y

    if is_jumping:
        player_rect.y += jump_vel
        jump_vel += x
        x += 0.2  # increase gravity over time

         # landing
        if player_rect.y >= ground_y:
            player_rect.y = ground_y
            is_jumping = False
            x = -0.5

    # draw background
    scroll += 5
    scroll = scroll % bg_width
    for i in range(tiles):
        screen.blit(bg, (i * bg_width - scroll, 0))

    #score system
    draw_text(size_font(30), f'Score:  {score_show}', 'black', SCREENWIDTH - 300, 60)
    score += 1
    score_show = score//2

    #tutorials
    if not tutorial_space and not tutorial_lshift:
        draw_text(size_font(30), 'press  SPACE  to  jump', 'black', 100, 100)
    elif tutorial_space and not tutorial_lshift:
        draw_text(size_font(30), 'press  Lshift  to  crawl', 'black', 100, 100)
    elif tutorial_lshift and tutorial_space and not tutorial_Pause:
        draw_text(size_font(30), 'press  ESC  to  pause  anytime', 'black', 100, 100)
    if not tutorial_Pause and (score_show > 500):
        tutorial_Pause = True

    # draw player
    screen.blit(player, player_rect)

    #obs movement
    screen.blit(Sasuke_obs, Sasuke_rect)
    Sasuke_rect.x -= obstacle_speed

    for rect in kunai_list:
        screen.blit(kunai_obs, rect)
        rect.x -= obstacle_speed

    #picking which obs is next
    if Sasuke_rect.x < -70 and all(k.x < -70 for k in kunai_list):
        choose_obs = random.randint(0, 3)
        obstacle_speed = random.randint(min_speed, max_speed)

        if choose_obs == 1:
            Sasuke_rect.x = -100
            kunai_list.clear()
            for y in kunai_y_positions:
                rect = kunai_obs.get_rect()
                rect.topleft = (1200, y)
                rect.height = int(rect.height * 0.5)
                rect.width = int(rect.width * 0.5)
                kunai_list.append(rect)
        else:
            kunai_list.clear()
            Sasuke_rect.x = 1200

    #difficulty increase
    if score%1000 == 0:
        if score//1000 > 6: speed_increase = 2
        else:   speed_increase = speed_list[score//1000]
        min_speed += speed_increase
        max_speed += speed_increase
        print(f'speed increased by: {speed_increase} m/s and is now: {min_speed}-{max_speed} m/s')

    #FPS show
    draw_text(size_font(20),f"FPS:  {int(clock.get_fps())}", 'black', 30, 30)

    #pause screen
    while Pause:
        clock.tick(FPS/3)

        screen.blit(bg_start, (0,0))
        draw_text(size_font(50), 'PAUSED', 'black', 400, 75)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Pause = False
                game = False

        if button_start.draw(screen):
            button_sound(end_song)
            naruto_sfx.play()
            end_song.stop()
            Pause = False

        elif button_finish.draw(screen):
            Pause = False
            game = False

        pygame.display.update()

    # collision
    if Sasuke_rect.colliderect(player_rect) or any(rect.colliderect(player_rect) for rect in kunai_list) or End_game:
        End_game = True
        naruto_sfx.stop()
        end_song.play(loops= -1)

    #End Game
    while End_game:
        clock.tick(FPS/2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                End_game  = False
                game = False

        #screen change
        screen.blit(bg_lose, (0,0))

        #score size and x
        if rank_game(score_show) == 'God Of Shinobi':
            score_x = 330
            score_size = 25
        else:
            score_x = 400
            score_size = 30

        draw_text(size_font(30), f'Final Score: {score_show}', 'black', 500, ground_y)
        draw_text(size_font(score_size), f'Your  Rank  is:  {rank_game(score_show)}', 'black', score_x, ground_y + 100)

        #button pressed end game
        if button_finish.draw(screen):
            End_game = False
            game = False

        elif button_start.draw(screen):
            button_sound(end_song)
            Sasuke_rect.x = 1200
            kunai_list.clear()
            player_rect.y = ground_y
            End_game = False
            x = -0.5
            min_speed = 10
            max_speed = 15
            speed_increase = 0
            score = 0
            obstacle_speed = 10
            end_song.stop()
            naruto_sfx.play()
        pygame.display.update()

    pygame.display.update()
pygame.quit()