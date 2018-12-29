import pygame, sys
import numpy as np
from game_elements import Pipes
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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

    pygame.display.update()

    pygame.time.wait(20)