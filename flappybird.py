import pygame, sys
import numpy as np
from game_elements import Pipes, Bird
from game_mechanics import Score, BirdPipeRelation, convert_pipes_group_to_pipe_rect, convert_pipes_group_to_pipe_rect_pairs
from game_memory import create_state, create_memory
import time

class FlappyBird:

    def __init__(self):

        pygame.init()
        self.background = pygame.image.load('./images/background.jpg')
        self.screen_x = 640
        self.screen_y = 480
        self.gap_width = 0.3
        self.pipe_width = 0.1
        self.space_between_pipes = 3 # a multiple of the pipe width
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
        self.pipes_group = pygame.sprite.Group()
        self.bird = Bird(screen_x = self.screen_x, screen_y = self.screen_y, gravity = 1.15)
        self.bird.create_bird_rect(start_x = 0.5, start_y = 0.2, size_x = 44, size_y = 30)
        self.t=0
        self.jump_velocity = -14
        self.score = 0
        self.scoring = Score()

    def play(self):
        while True:
            self.run_frame()
    
    def run_frame(self, action=False):
        self.t = self.t+1
        self.action = action
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.action = True

        self.screen.blit(self.background, (0,0))

        self.create_pipes()
        self.state = create_state(bird = self.bird, pipes_group = self.pipes_group)

        if self.action:
            self.t=0
            self.bird.jump_velocity = self.jump_velocity
            self.bird.start_y = self.bird.bird_rect.y

        pipe_rect_list = convert_pipes_group_to_pipe_rect(pipe_group = self.pipes_group)
        self.die = self.bird.die(list_of_rects = pipe_rect_list)

        if self.die:
            self.restart_game()
        else:
            self.continue_game()

        pygame.display.update()

        pygame.time.wait(20)
        

    def create_pipes(self):
        if len(self.pipes_group)==0:
            gap_height = np.random.uniform(0.2, 0.8)
            Pipes(gap_width = self.gap_width, pipe_width = self.pipe_width, screen_x = self.screen_x, screen_y = self.screen_y).add(self.pipes_group)
            self.pipes_group.sprites()[0].create_pipes(x_pos = self.screen_x, gap_height = gap_height)
        else:
            max_index = len(self.pipes_group.sprites())-1
            new_pipe_x = self.screen_x - int(np.round(self.pipes_group.sprites()[max_index].pipe_width * self.space_between_pipes, 0))
            if self.pipes_group.sprites()[max_index].bot_pipe_rect.x == new_pipe_x:
                gap_height = np.random.uniform(0.2, 0.8)
                Pipes(gap_width = self.gap_width, pipe_width = self.pipe_width, screen_x = self.screen_x, screen_y = self.screen_y).add(self.pipes_group)
                self.pipes_group.sprites()[max_index+1].create_pipes(x_pos = self.screen_x, gap_height = gap_height)
            else: 
                pass

    def restart_game(self):
        self.pipes_group.empty()
        self.bird = Bird(screen_x = self.screen_x, screen_y = self.screen_y, gravity = 1.2)
        self.bird.create_bird_rect(start_x = 0.5, start_y = 0.2, size_x = 44, size_y = 30)
        self.t=0
        self.score=0
        self.distance = 0
        self.reward = 0
    
    def continue_game(self):
        self.score, score_reward = self.scoring.new_score(bird = self.bird, pipes_group = self.pipes_group, score = self.score)
        self.scoring.display_score(score = self.score, surface = self.screen)
        self.reward = 1 + 5 * score_reward
        self.bird.move(t = self.t)
        self.bird.draw_bird(surface = self.screen)

        for pipe in self.pipes_group:
            pipe.remove()
            pipe.move_pipes()
            pipe.draw_pipes(surface=self.screen)
        
        self.next_state = create_state(bird = self.bird, pipes_group = self.pipes_group)
        self.memory_frag = create_memory(state = self.state, action = self.action, next_state = self.next_state, reward = self.reward)

    def get_memory(self):
        return self.memory_frag