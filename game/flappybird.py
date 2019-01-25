import pygame, sys
import numpy as np
from game.game_elements import Pipes, Bird
from game.game_tools import Score, BirdPipeRelation, TransitionGenerator, convert_pipes_group_to_pipe_rect
import time

class FlappyBird:

    def __init__(self):

        pygame.init()
        self.background = pygame.image.load('./images/background.jpg')
        self.screen_x = 640
        self.screen_y = 480
        self.gap_width = 0.3
        self.pipe_width = 0.1
        self.space_between_pipes = 4.5 # a multiple of the pipe width
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
        self.pipes_group = pygame.sprite.Group()
        self._create_pipes()
        self.bird = Bird(screen_x = self.screen_x, screen_y = self.screen_y, gravity = 1.15)
        self.bird.create_bird_rect(start_x = 0.5, start_y = 0.2, size_x = 44, size_y = 30)
        self.t=0
        self.jump_velocity = -14
        self.scoring = Score()
        self.state = TransitionGenerator.create_state(self.bird, self.pipes_group)
        self.die = False

    def play(self):
        while True:
            self.run_frame()
    
    def run_frame(self, action=0, train = False):
        self.t = self.t+1
        self.action = action
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.action = 1

        self.screen.blit(self.background, (0,0))

        self._create_pipes()

        if self.action == 1:
            self.t=0
            self.bird.jump_velocity = self.jump_velocity
            self.bird.start_y = self.bird.bird_rect.y

        pipe_rect_list = convert_pipes_group_to_pipe_rect(pipe_group = self.pipes_group)
        self.die = self.bird.die(list_of_rects = pipe_rect_list)

        if self.die:
            self._restart_game()
        else:
            self._continue_game()

        pygame.display.update()

        if train is False:
            pygame.time.wait(20)
        else:
            pass

    def _create_pipes(self):
        if len(self.pipes_group)==0:
            gap_height = np.random.uniform(0.2, 0.8)
            Pipes(gap_width = self.gap_width, pipe_width = self.pipe_width, screen_x = self.screen_x, screen_y = self.screen_y).add(self.pipes_group)
            self.pipes_group.sprites()[0].create_pipes(x_pos = self.screen_x, gap_height = gap_height)
        else:
            max_index = len(self.pipes_group.sprites())-1
            new_pipe_x = self.screen_x - int(np.round(self.pipes_group.sprites()[max_index].pipe_width * self.space_between_pipes, 0))
            if self.pipes_group.sprites()[max_index].bot_pipe_rect.x < new_pipe_x:
                gap_height = np.random.uniform(0.2, 0.8)
                Pipes(gap_width = self.gap_width, pipe_width = self.pipe_width, screen_x = self.screen_x, screen_y = self.screen_y).add(self.pipes_group)
                self.pipes_group.sprites()[max_index+1].create_pipes(x_pos = self.screen_x, gap_height = gap_height)
            else: 
                pass

    def _restart_game(self):
        self.pipes_group.empty()
        self.bird = Bird(screen_x = self.screen_x, screen_y = self.screen_y, gravity = 1.2)
        self.bird.create_bird_rect(start_x = 0.5, start_y = 0.2, size_x = 44, size_y = 30)
        self.t=0
        self.scoring = Score()
        self.distance = 0
        self.state = TransitionGenerator.create_state(self.bird, self.pipes_group)
    
    def _continue_game(self):
        self.scoring.update_score(self.bird, self.pipes_group)
        self.scoring.display_score(surface = self.screen)
        
        self.bird.move(t = self.t)
        self.bird.draw_bird(surface = self.screen)

        for pipe in self.pipes_group:
            pipe.remove()
            pipe.move_pipes()
            pipe.draw_pipes(surface=self.screen)

        self.state = TransitionGenerator.create_state(self.bird, self.pipes_group)

    def get_state(self):
        return self.state
    
    def get_action(self):
        return self.action
    
    def get_score(self):
        return self.scoring.score