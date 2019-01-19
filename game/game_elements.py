import pygame, sys
import numpy as np
from math import atan, pi

class Pipes(pygame.sprite.Sprite):

    pipe_image_bot = pygame.image.load('./images/wall_bot.png')
    pipe_image_top = pygame.image.load('./images/wall_top.png')
    green = [0, 255, 0]
    
    def __init__(self, gap_width, pipe_width, screen_x, screen_y):
        pygame.sprite.Sprite.__init__(self)
        self.gap_width = np.round(gap_width * screen_y, 0)
        if self.gap_width % 2 != 0:
            self.gap_width + 1
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.pipe_width = np.round(pipe_width * screen_x)
        
    def create_pipes(self, x_pos, gap_height):
        gap_height = np.round(self.screen_y * gap_height, 0)
        # bottom pipe
        bot_pipe_height = gap_height - self.gap_width/2
        bot_pipe_start_position = self.screen_y - bot_pipe_height
        self.bot_pipe_rect = pygame.rect.Rect(int(x_pos), int(bot_pipe_start_position), int(self.pipe_width), int(bot_pipe_height))

        # top pipe
        top_pipe_height = self.screen_y - self.gap_width - bot_pipe_height
        self.top_pipe_rect = pygame.rect.Rect(int(x_pos), int(top_pipe_height - self.screen_y), int(self.pipe_width), int(self.screen_y))
    
    def draw_pipes(self, surface):
        surface.blit(self.pipe_image_bot, self.bot_pipe_rect)
        surface.blit(self.pipe_image_top, self.top_pipe_rect)
        # pygame.draw.rect(surface, self.green, self.bot_pipe_rect)
        # pygame.draw.rect(surface, self.green, self.top_pipe_rect)

    def move_pipes(self):
        self.bot_pipe_rect.move_ip(-2, 0)
        self.top_pipe_rect.move_ip(-2, 0)
    
    def remove(self):
        if self.bot_pipe_rect.x == -1 * self.pipe_width:
            self.kill()


class Bird(pygame.sprite.Sprite):

    yellow = [255, 255, 0]
    bird_pic = pygame.image.load('./images/fb44x30.png')

    def __init__(self, screen_x, screen_y, gravity, jump_velocity=0):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.gravity = gravity
        self.jump_velocity = jump_velocity

    def create_bird_rect(self, start_x, start_y, size_x, size_y):
        self.start_x = int(np.round(start_x * self.screen_x, 0))
        self.start_y = int(np.round(start_y * self.screen_y, 0))
        self.bird_rect = pygame.rect.Rect(self.start_x, self.start_y, size_x, size_y)

    def draw_bird(self, surface):
        angle = -atan(self.y_offset/15)/pi*180
        display_bird = pygame.transform.rotate(self.bird_pic, angle)
        surface.blit(display_bird, self.bird_rect)

    def move(self, t):
        new_y = self.gravity * t**2 + self.jump_velocity * t + self.start_y
        self.y_offset = new_y - self.bird_rect.y
        self.bird_rect.move_ip(0, self.y_offset)
    
    def die(self, list_of_rects):
        collision = self.bird_rect.collidelist(list_of_rects)
        bird_top = self.bird_rect.y
        bird_bot = self.bird_rect.y + self.bird_rect.size[1]
        
        if bird_top >= self.screen_y:
            return True
        elif bird_bot <= 0:
            return True
        if collision == -1:
            return False
        else:
            return True


