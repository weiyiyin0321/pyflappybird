from collections import namedtuple
import random


Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))

class GameMemory:
    
    def __init__(self, discount_factor):
        self.memory = []
        self.discount_factor = discount_factor
    
    def add_memory_frag(self, memory_frag):
        self.memory.append(memory_frag)

    def process_memory(self):
        sum_discounted_reward = self._calc_sum_discounted_reward()
        for i in self.memory:
            i.reward = sum_discounted_reward[i]

    def export_memory(self):
        return self.memory
    
    def _calc_sum_discounted_reward(self):
        reward = [i.reward for i in self.memory]
        sum_discount_reward = [self._calc_discounted_reward(reward = reward, start_position = i) for i, j in enumerate(reward)]
        return sum_discount_reward
    
    def _calc_discounted_reward(self, reward, start_position):
        discounted_reward_list = [j * (self.discount_factor ** (i - start_position)) for i, j in enumerate(reward) if i >= start_position]
        total_discounted_reward = sum(discounted_reward_list)
        return total_discounted_reward


class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)