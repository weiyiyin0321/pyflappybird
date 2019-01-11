import pygame
import numpy

class Score:

    def __init__(self):
        pygame.font.init()
        self.score_font = pygame.font.SysFont('Calibri', 60)

    def new_score(self, bird, pipes_group, score):
        for pipe in pipes_group:
            if pipe.bot_pipe_rect.x + pipe.pipe_width == bird.bird_rect.x:
                score = score+1
        return score, 1

    def display_score(self, score, surface):
        score_text = self.score_font.render(str(score), False, [255, 255, 255], [0, 0, 0])
        surface.blit(score_text, (0,0))

class BirdPipeRelation:

    def __init__(self, bird_rect, pipe_rect_bot, pipe_rect_top):
        self.bird_left = bird_rect.x
        self.bird_right = bird_rect.x + bird_rect.size[0]
        self.pipe_left = pipe_rect_bot.x
        self.pipe_right = pipe_rect_bot.x + pipe_rect_bot.size[0]
        self.pipe_top_y = pipe_rect_top.y + pipe_rect_top.size[1]
        self.pipe_bot_y = pipe_rect_bot.y
    
    def is_bird_between_pipe(self):
        if (self.bird_right > self.pipe_left) & (self.bird_left < self.pipe_right):
            return True
        else:
            return False

    def calculate_distance_x(self):
        return self.pipe_left - self.bird_right

def convert_pipes_group_to_pipe_rect_pairs(pipe_group):
    pipe_pairs_rect_list = []
    for pipe in pipe_group:
        pipe_pairs_rect_list.append([pipe.bot_pipe_rect, pipe.top_pipe_rect])
    return pipe_pairs_rect_list

def convert_pipes_group_to_pipe_rect(pipe_group):
    pipe_rect_list = []
    for pipe in pipe_group:
        pipe_rect_list.extend([pipe.bot_pipe_rect, pipe.top_pipe_rect])
    return pipe_rect_list

