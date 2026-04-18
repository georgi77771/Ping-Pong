import pygame
from pygame import *
import random

pygame.init()

win_width = 1028
win_height = 480
window = display.set_mode((win_width, win_height))
display.set_caption('Ping Pong')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

FPS = 60
clock = time.Clock()
run = True
game_over = False
loser = ""

font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 120:
            self.rect.y += self.speed
    
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 120:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, speed_x, speed_y, player_speed, player_width, player_height):
        super().__init__(player_image, player_x, player_y, player_speed, player_width, player_height)
        self.speed_x = speed_x
        self.speed_y = speed_y
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.y <= 0 or self.rect.y >= win_height - 20:
            self.speed_y = -self.speed_y

racket_left = Player("left_paddle.png", 30, win_height//2 - 60, 7, 25, 100)
racket_right = Player("right_paddle.png", win_width - 55, win_height//2 - 60, 7, 25, 100)
ball = Ball("ball.png", win_width//2 - 10, win_height//2 - 10, 4, 4, 0, 20, 20)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and game_over:
            if e.key == K_SPACE:
                game_over = False
                loser = ""
                ball.rect.x = win_width//2 - 10
                ball.rect.y = win_height//2 - 10
                ball.speed_x = 4
                ball.speed_y = 4
                racket_left.rect.y = win_height//2 - 60
                racket_right.rect.y = win_height//2 - 60

    if not game_over:
        racket_left.update_l()
        racket_right.update_r()
        ball.update()
        
        if sprite.collide_rect(ball, racket_left):
            ball.speed_x = abs(ball.speed_x)
            ball.rect.x = racket_left.rect.x + 25
        
        if sprite.collide_rect(ball, racket_right):
            ball.speed_x = -abs(ball.speed_x)
            ball.rect.x = racket_right.rect.x - 20
        
        if ball.rect.x < 0:
            game_over = True
            loser = "Player 2"
        
        if ball.rect.x > win_width:
            game_over = True
            loser = "Player 1"
    
    window.fill(BLUE)
    
    if game_over:
        game_over_text = font.render(f"{loser} LOSE!", True, RED)
        restart_text = small_font.render("Press SPACE to restart", True, WHITE)
        window.blit(game_over_text, (win_width//2 - 150, win_height//2 - 50))
        window.blit(restart_text, (win_width//2 - 130, win_height//2 + 20))
    else:
        racket_left.reset()
        racket_right.reset()
        ball.reset()
    
    display.update()
    clock.tick(FPS)

pygame.quit()