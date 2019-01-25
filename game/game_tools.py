import pygame
import numpy
from ai.memory import Transition

class Score:

    def __init__(self):
        pygame.font.init()
        self.score_font = pygame.font.SysFont('Calibri', 60)
        self.score = 0
        self.between_pipe_sum = 0

    def update_score(self, bird, pipes_group):
        new_between_pipe_list = []
        for pipe in pipes_group:
            new_between_pipe_list.append(BirdPipeRelation(bird, pipe).is_bird_between_pipe())
        new_between_pipe_sum = sum(new_between_pipe_list)
        if new_between_pipe_sum==0 and self.between_pipe_sum==1:
            self.score = self.score + 1
        self.between_pipe_sum = new_between_pipe_sum

    def display_score(self, surface):
        score_text = self.score_font.render(str(self.score), False, [255, 255, 255], [0, 0, 0])
        surface.blit(score_text, (0,0))

class BirdPipeRelation:

    def __init__(self, bird, pipes):
        self.bird_left = bird.bird_rect.x
        self.bird_right = bird.bird_rect.x + bird.bird_rect.size[0]
        self.bird_top = bird.bird_rect.y
        self.bird_bot = bird.bird_rect.y - bird.bird_rect.size[1]
        self.pipe_left = pipes.bot_pipe_rect.x
        self.pipe_right = pipes.bot_pipe_rect.x + pipes.bot_pipe_rect.size[0]
        self.pipe_top_y = pipes.top_pipe_rect.y + pipes.top_pipe_rect.size[1]
        self.pipe_bot_y = pipes.bot_pipe_rect.y
        self.gap_height = pipes.gap_height
    
    def is_bird_between_pipe(self):
        if (self.bird_right > self.pipe_left) & (self.bird_left < self.pipe_right):
            return True
        else:
            return False

class TransitionGenerator:

    @staticmethod
    def create_state(bird, pipe_group):
        for pipes in pipe_group:
            bird_pipe_relation = BirdPipeRelation(bird, pipes)
            if bird_pipe_relation.bird_left > bird_pipe_relation.pipe_right:
                continue
            else:
                state = [
                    bird_pipe_relation.pipe_left,
                    bird_pipe_relation.pipe_right,
                    bird_pipe_relation.pipe_bot_y,
                    bird_pipe_relation.pipe_top_y,
                    bird_pipe_relation.bird_left,
                    bird_pipe_relation.bird_right,
                    bird_pipe_relation.bird_top,
                    bird_pipe_relation.bird_bot,
                    1 if bird_pipe_relation.is_bird_between_pipe() else 0
                ]
                return state

    @staticmethod
    def calc_reward(state):
        gap_height = (state[2] + state[3])/2
        bird_height = (state[6] + state[7])/2
        reward = -1 * abs(gap_height - bird_height)
        return reward

    @staticmethod
    def create_transition(state, action, next_state, reward):
        return Transition(state, action, next_state, reward)

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




