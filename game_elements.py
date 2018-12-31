import pygame, sys
import numpy as np

class Pipes(pygame.sprite.Sprite):

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
        self.top_pipe_rect = pygame.rect.Rect(int(x_pos), int(0), int(self.pipe_width), int(top_pipe_height))
    
    def draw_pipes(self, surface):
        pygame.draw.rect(surface, self.green, self.bot_pipe_rect)
        pygame.draw.rect(surface, self.green, self.top_pipe_rect)

    def move_pipes(self):
        self.bot_pipe_rect.move_ip(-2, 0)
        self.top_pipe_rect.move_ip(-2, 0)
    
    def remove(self):
        if self.bot_pipe_rect.x == -1 * self.pipe_width:
            self.kill()


class Bird(pygame.sprite.Sprite):

    yellow = [255, 255, 0]

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
        pygame.draw.rect(surface, self.yellow, self.bird_rect)

    def move(self, t):
        new_y = self.gravity * t**2 + self.jump_velocity * t + self.start_y
        y_offset = new_y - self.bird_rect.y
        self.bird_rect.move_ip(0, y_offset)


