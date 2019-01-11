import torch
import torch.nn as nn

class DQN(nn.Module):

    def __init__(self):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(in_features=6, out_features=6)
        self.fc2 = nn.Linear(in_features=6, out_features=1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x