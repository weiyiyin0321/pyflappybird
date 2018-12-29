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
        self.bot_pipe_rect.move_ip(-1, 0)
        self.top_pipe_rect.move_ip(-1, 0)
    
    def remove(self):
        if self.bot_pipe_rect.x == -1 * self.pipe_width:
            self.kill()


