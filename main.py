import pygame, sys
import numpy as np
from game_elements import Pipes, Bird
import time

pygame.init()

red = [255, 0, 0]
background = [0, 0, 0]
screen_x = 640
screen_y = 480
gap_width = 0.2
pipe_width = 0.1
space_between_pipes = 2.5 # a multiple of the pipe width
screen = pygame.display.set_mode((screen_x, screen_y))
pipes_group = pygame.sprite.Group()
bird = Bird(screen_x = screen_x, screen_y = screen_y, gravity = 1.2)
bird.create_bird_rect(start_x = 0.5, start_y = 0.2, size_x = 20, size_y = 20)
t=0
jump_velocity = -15

while True:
    t = t+1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                t=0
                bird.jump_velocity = jump_velocity
                bird.start_y = bird.bird_rect.y

    screen.fill(background)

    if len(pipes_group)==0:
        gap_height = np.random.uniform(0.1, 0.9)
        Pipes(gap_width = gap_width, pipe_width = pipe_width, screen_x = screen_x, screen_y = screen_y).add(pipes_group)
        pipes_group.sprites()[0].create_pipes(x_pos = screen_x, gap_height = gap_height)
    else:
        max_index = len(pipes_group.sprites())-1
        new_pipe_x = screen_x - int(np.round(pipes_group.sprites()[max_index].pipe_width * space_between_pipes, 0))
        if pipes_group.sprites()[max_index].bot_pipe_rect.x == new_pipe_x:
            gap_height = np.random.uniform(0.1, 0.9)
            Pipes(gap_width = gap_width, pipe_width = pipe_width, screen_x = screen_x, screen_y = screen_y).add(pipes_group)
            pipes_group.sprites()[max_index+1].create_pipes(x_pos = screen_x, gap_height = gap_height)
        else: 
            pass
    
    for pipe in pipes_group:
        pipe.remove()
        pipe.move_pipes()
        pipe.draw_pipes(surface=screen)

    bird.move(t = t)
    bird.draw_bird(surface = screen)

    pygame.display.update()

    pygame.time.wait(20)