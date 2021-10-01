# Joshua Nelson | Pong | Version 2.1 | 9/30/21 |
# Music: XO by Peter Lam | https://hellothematic.com/


import pygame, sys, random


def ball_animation():
    pygame.mixer.Sound.play(pong_sound)
    global ball_speed_x
    global ball_speed_y
    global player_score
    global ai_opponent_score
    global score_time


    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0:
        ai_opponent_score += 1
        score_time = pygame.time.get_ticks()
    if ball.right >= screen_width:
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(ai_opponent) and ball_speed_x < 0:
        if abs(ball.left - ai_opponent.right) > 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - ai_opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - ai_opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def ai_animation():
    if ai_opponent.top < ball.y:
        ai_opponent.top += ai_opponent_speed
    if ai_opponent.bottom > ball.y:
        ai_opponent.bottom -= ai_opponent_speed
    if ai_opponent.top <= 0:
        ai_opponent.top = 0
    if ai_opponent.bottom >= screen_height:
        ai_opponent.bottom = ai_opponent_speed


def ball_restart():
    global ball_speed_x
    global ball_speed_y
    global score_time

    current_time = pygame.time.get_ticks()

    ball.center = (screen_width / 2, screen_height / 2)

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))
        score_time = None


# GENERAL SETUP
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# TEXT VARIABLES
player_score = 0
ai_opponent_score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# SOUND
pong_sound = pygame.mixer.Sound('C:\\music\\XO.mp3')

# COLORS
light_grey = (200, 200, 200)
bg_color = pygame.Color('grey12')

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
ai_opponent_speed = 7

# GAME RECTANGLES
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
ai_opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)


# SCORE TIMER
score_time = None



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7

            if event.key == pygame.K_w:
                ai_opponent_speed += 7
            if event.key == pygame.K_s:
                ai_opponent_speed -= 7

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

            if event.key == pygame.K_s:
                ai_opponent_speed -= 7
            if event.key == pygame.K_w:
                player_speed += 7

    ball_animation()
    player_animation()
    ai_animation()

    # VISUALS
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, ai_opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    player_text = font.render(f'{player_score}', False, light_grey)
    screen.blit(player_text, (660, 360))

    ai_opponent_text = font.render(f'{ai_opponent_score}', False, light_grey)
    screen.blit(ai_opponent_text, (600, 360))

    if score_time:
        ball_restart()

    pygame.display.flip()
    clock.tick(60)
