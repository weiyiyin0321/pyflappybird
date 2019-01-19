from ai.model import DQN
from ai.memory import ReplayMemory
import random
from game.flappybird import FlappyBird
import torch
from math import exp

batch_size = 150
gamma = 0.99
eps_start = 0.9
eps_end = 0.05
eps_decay = 5000
action_set = [0, 1]
training_loop_count = 300
target_update = 10
decision_freq = 5

policy_net = DQN()
target_net = DQN()
game_memory = ReplayMemory(500)

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
        reward = current_state_reward
    else:
        next_state_optimal_reward = model(torch.Tensor([next_state])).max(1)[0].tolist()[0]
        reward = current_state_reward + next_state_optimal_reward
    return reward


def train():
    step = 0
    training_loop = 0
    flappy_bird = FlappyBird()
    current_score = 0
    optimizer = torch.optim.SGD(policy_net.parameters(), lr = 0.001)
    target_net.load_state_dict(policy_net.state_dict())
    target_net.eval()
    high_score = 0

    while current_score < 50:

        # step 1: run a cycle of the game with a AI / Random selected action
        random_select_prob = eps_end + (eps_start - eps_end) * exp(-1 * training_loop / eps_decay)
        print(random_select_prob, training_loop)
        current_state = flappy_bird.get_state()
        if flappy_bird.score > high_score:
            high_score = flappy_bird.score
            torch.save(policy_net.state_dict(), './ai/train_model_high_score_{}.pkl'.format(high_score))
        # print("step: {}".format(step))
        # print("training_loop: {}".format(training_loop))
        if step % decision_freq == 0:
            action = select_action(current_state, random_select_prob)
            flappy_bird.run_frame(action, train = True)
            memory_frag = flappy_bird.get_memory()
            current_score = flappy_bird.get_score()
            step = step + 1
            training_loop = training_loop + 1

            # step 2: store memory frag into game memory then sample if there is enough data for training
            game_memory.push(memory_frag)
            if batch_size <= game_memory.__len__():
                training_memory = game_memory.sample(batch_size)
                
            else:
                continue
            
            # step 3: train the cnn
            target_reward = torch.Tensor([[calc_reward(i, target_net)] for i in training_memory])
            input_states = torch.Tensor([i.state for i in training_memory])
            actions_taken = torch.Tensor([[i.action] for i in training_memory]).long()
            predicted_reward = policy_net(input_states).gather(1, actions_taken)
            loss = torch.nn.functional.smooth_l1_loss(predicted_reward, target_reward)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # step 4: update the target cnn
            if step % target_update == 0:
                target_net.load_state_dict(policy_net.state_dict())
        else:
            flappy_bird.run_frame(train=True)
            step = step + 1

    target_net.load_state_dict(policy_net.state_dict())
    torch.save(target_net.state_dict(), './ai/trained_model_state_dict.pkl')
    print('finished training')

train()






