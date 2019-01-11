from game_mechanics import BirdPipeRelation, convert_pipes_group_to_pipe_rect_pairs
from ai.memory import Transition


def create_memory(state, action, next_state, reward):
    return Transition(state, action, next_state, reward)

def create_state(bird, pipes_group):
    pipe_pairs_rect_list = convert_pipes_group_to_pipe_rect_pairs(pipes_group)

    pipe_distance = []
    pipe_bot_y = []
    pipe_top_y = []
    within_pipe = False

    for pipe_pair in pipe_pairs_rect_list:
        relation = BirdPipeRelation(bird_rect = bird.bird_rect, pipe_rect_bot = pipe_pair[0], pipe_rect_top = pipe_pair[1])
        if within_pipe is not True:
            if relation.is_bird_between_pipe():
                within_pipe = True
            else:
                pass
        else:
            pass
        if relation.calculate_distance_x()>0:
            pipe_distance.append(relation.calculate_distance_x())
            pipe_bot_y.append(relation.pipe_bot_y)
            pipe_top_y.append(relation.pipe_top_y)
        else:
            pass
    
    min_distance_index = pipe_distance.index(min(pipe_distance))

    pipe_distance = pipe_distance.pop(min_distance_index)
    pipe_bot_y = pipe_bot_y.pop(min_distance_index)
    pipe_top_y = pipe_top_y.pop(min_distance_index)  

    state = [
        bird.bird_rect.size[0], 
        bird.bird_rect.size[1],
        bird.bird_rect.y,
        pipe_distance,
        pipe_bot_y,
        pipe_top_y,
        within_pipe
    ]

    return state
