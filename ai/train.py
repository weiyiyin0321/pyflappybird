from ai.model import DQN
from ai.memory import ReplayMemory
from game.game_tools import TransitionGenerator
import random
from game.flappybird import FlappyBird
import torch
from math import exp

batch_size = 300
gamma = 0.99
eps_start = 0.9
eps_end = 0.05
eps_decay = 500
action_set = [0, 1]
training_loop_count = 300
target_update = 10
decision_freq = 5

policy_net = DQN()
target_net = DQN()
game_memory = ReplayMemory(2000)

def select_action(state, random_select_prob):
    if random.random() < random_select_prob:
        action = random.choice(action_set)
    else:
        action = policy_net(torch.Tensor([state])).max(1)[1].tolist()[0]
    return action

def calc_reward(memory, model):
    current_state_reward = memory.reward
    next_state = memory.next_state
    if next_state is None:
        reward = current_state_reward - 480
    else:
        next_state_optimal_reward = model(torch.Tensor([next_state])).max(1)[0].tolist()[0]
        reward = current_state_reward + next_state_optimal_reward
    return reward

def train():
    step = 0
    training_loop = 0
    flappy_bird = FlappyBird()
    current_score = 0
    optimizer = torch.optim.SGD(policy_net.parameters(), lr = 0.01)
    target_net.load_state_dict(policy_net.state_dict())
    target_net.eval()
    high_score = 0
    current_state = None
    next_state = None
    action = None
    reward = None

    while current_score < 50:

        random_select_prob = eps_end + (eps_start - eps_end) * exp(-1 * training_loop / eps_decay)

        current_score = flappy_bird.get_score()
        print(step)
        print(training_loop)
        print(game_memory.__len__())

        if flappy_bird.get_score() > high_score:
            high_score = flappy_bird.get_score()
            torch.save(policy_net.state_dict(), './ai/train_model_high_score_{}.pkl'.format(high_score))

        if flappy_bird.die:
            transition = TransitionGenerator.create_transition(current_state, action, None, -1 * flappy_bird.screen_y)
            if transition.state is not None:
                game_memory.push(transition)
            flappy_bird.run_frame(train=True)
            step = step + 1
        elif step % decision_freq == 0:
            # step 1: make a transition & push into game_memory
            next_state = flappy_bird.get_state()
            reward = TransitionGenerator.calc_reward(next_state)
            transition = TransitionGenerator.create_transition(current_state, action, next_state, reward)
            if transition.state is not None:
                game_memory.push(transition)

            # step 2: store memory frag into game memory then sample if there is enough data for training
            if batch_size <= game_memory.__len__():
                training_memory = game_memory.sample(batch_size)

                # step 3: train the cnn
                target_reward = torch.Tensor([[calc_reward(i, target_net)] for i in training_memory])
                input_states = torch.Tensor([i.state for i in training_memory])
                actions_taken = torch.Tensor([[i.action] for i in training_memory]).long()
                predicted_reward = policy_net(input_states).gather(1, actions_taken)
                loss = torch.nn.functional.smooth_l1_loss(predicted_reward, target_reward)
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                training_loop = training_loop + 1

                # step 4: update the target cnn
                if step % target_update == 0:
                    target_net.load_state_dict(policy_net.state_dict())
            else:
                pass

            # step 5: move next_stage to current_state, select the action, and perform the action on the game 
            current_state = next_state
            action = select_action(current_state, random_select_prob)
            flappy_bird.run_frame(action, train = True)
            step = step + 1
            
        else:
            flappy_bird.run_frame(train=True)
            step = step + 1

    target_net.load_state_dict(policy_net.state_dict())
    torch.save(target_net.state_dict(), './ai/trained_model_state_dict.pkl')
    print('finished training')

train()






