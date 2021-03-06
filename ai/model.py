import torch
import torch.nn as nn

class DQN(nn.Module):

    def __init__(self):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(in_features=9, out_features=27)
        self.fc2 = nn.Linear(in_features=27, out_features=2)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x