import torch.nn as nn


class Net(nn.Module):

    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(70, 40)
        self.relu1 = nn.ReLU()
        # self.dout = nn.Dropout(0.2)
        self.fc2 = nn.Linear(50, 100)
        self.relu = nn.ReLU(1)
        self.out = nn.Linear(40, 1)
        # self.out_act = nn.Sigmoid()

    def forward(self, input_):
        a1 = self.fc1(input_)
        h1 = self.relu1(a1)
        # dout = self.dout(h1)
        # a2 = self.fc2(h1)
        # h2 = self.relu(a2)
        y = self.out(h1)
        # y = self.out_act(a3)
        return y
