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
        return score

    def display_score(self, score, surface):
        score_text = self.score_font.render(str(score), False, [255, 255, 255], [0, 0, 0])
        surface.blit(score_text, (0,0))



