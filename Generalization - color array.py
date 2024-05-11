import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.optim as optim
import numpy as np
import random
import matplotlib.pyplot as plt

DIM = 14
samplesNumber = 500
testNumber = 100
#nTrain = [500, 1000, 2000, 30000, 120000, 120000]
nTrain = [500, 1000, 2000, 4000, 8000, 12000]
nTest = [200, 200, 200, 400, 800, 1200]

def createDummyData(samplesNumber, *_):

    x = np.concatenate((np.random.uniform(0.5, 1, (samplesNumber, DIM)), np.random.uniform(-0.5, -1, (samplesNumber, DIM))))
    y = np.ones(samplesNumber * 2).astype(np.int32)
    y[0:samplesNumber] = 0
    # y[samplesNumber:2*samplesNumber, 1] = 0
    perm = np.random.permutation(samplesNumber * 2);

    return (x[perm, :], y[perm])

def createData(samplesNumber, stage):

    x = np.ones((samplesNumber, 14))
    y = np.ones(samplesNumber)
    c = np.identity(5)
    c = (c - np.mean(c)) / np.std(c)

    if stage == 1:
        for i in range(samplesNumber):
            a = np.random.permutation(c[0:2])
            x[i, 0] = np.random.choice(a, 1)
            x[i, 1:4] = a[0]
            x[i, 4:6] = a[1]
            x[i, 6:14] = -1
            y[i] = 1 if x[i, 0] == a[0] else 0
    elif stage == 2:
        for i in range(samplesNumber):
            a = np.random.choice(c[0:2], 2, replace=False)
            x[i, 0] = np.random.choice(a, 1)
            ind = random.randint(-5, -1)
            tmp = np.full(5, a[0])
            for j in range (ind, ind+2):
                tmp[j]= a[1]
            x[i, 1:6] = tmp
            x[i, 6:14] = -1
            y[i] = 1 if x[i,0] == a[0] else 0
    elif stage == 3:
        for i in range(samplesNumber):
            a = np.random.choice(c, 2, replace=False)
            x[i, 0] = np.random.choice(a, 1)
            tmp = np.full(5, a[0])
            ind = random.randint(-5, -1)
            for j in range (ind, ind+2):
                tmp[j]= a[1]
            x[i, 1:6] = tmp
            x[i, 6:14] = -1
            y[i] = 1 if x[i,0] == a[0] else 0
    elif stage == 4:
        for i in range(samplesNumber):
            a = np.random.choice(c, 2, replace=False)
            x[i, 0] = np.random.choice(a, 1)
            total = random.randint(6, 13)
            tmp = np.full(total, a[0])
            ind = random.randint(total*-1, -1)
            for j in range (ind, ind+2):
                tmp[j]= a[1]
            x[i, 1:total+1] = tmp
            x[i, total+1:14] = -1
            y[i] = 1 if x[i,0] == a[0] else 0
    elif stage == 5:
        for i in range(samplesNumber):
            a = np.random.choice(c, 2, replace=False)
            x[i, 0] = np.random.choice(a, 1)
            total = random.randint(7, 13)
            tmp = np.full(total, a[0])
            min = random.randint(3, int((total-1)/2))
            most = total - min
            ind = random.randint(total*-1, -1)
            for j in range (ind, ind+min):
                tmp[j]= a[1]
            x[i, 1:total+1] = tmp
            x[i, total+1:14] = -1
            y[i] = 1 if x[i,0] == a[0] else 0
    elif stage == 6:
        for i in range(samplesNumber):
            a = np.random.choice(c, 3, replace=False)
            x[i, 0] = np.random.choice(a, 1)
            total = random.randint(11, 13)
            tmp = np.full(total, a[0])
            min = 2
            mid = 3
            ind = random.randint(total*-1, -1)
            b = np.random.choice([min,mid],2, replace=False)
            for j in range (ind, ind+b[0]):
                tmp[j]= a[1]
            for j in range(ind+b[0], ind + b[0] + b[1]):
                tmp[j] = a[2]
            if b[0] == min and x[i, 0] == a[2]:
                x[i, 0] = a[1]
            if b[1] == min and x[i, 0] == a[1]:
                x[i, 0] = a[2]
            x[i, 1:total+1] = tmp
            x[i, total+1:14] = -1
            y[i] = 1 if x[i,0] == a[0] else 0

    #x = (x[:] - np.mean(x, axis=1, keepdims=True)) / np.std(x, axis=1, keepdims=True)

    #print(stage, np.unique(x,axis=0).shape[0])

    X = torch.as_tensor(x, dtype=torch.float32).requires_grad_()
    Y = torch.as_tensor(y, dtype=torch.float32).reshape(samplesNumber, 1)

    return X, Y

class Net(nn.Module):

    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(14, 50)
        self.relu1 = nn.ReLU()
        #self.dout = nn.Dropout(0.2)
        self.fc2 = nn.Linear(50, 100)
        self.relu = nn.ReLU(1)
        self.out = nn.Linear(100, 1)
        #self.out_act = nn.Sigmoid()

    def forward(self, input_):
        a1 = self.fc1(input_)
        h1 = self.relu1(a1)
        #dout = self.dout(h1)
        a2 = self.fc2(h1)
        h2 = self.relu(a2)
        y = self.out(h2)
        #y = self.out_act(a3)
        return y

def train(model, optimizer, criterion, X_train, Y_train, X_test, Y_test):
    train_loss = []
    train_acc = []
    test_loss = []
    test_acc = []
    numCheck = X_train.size(0)/10
    for i in range(0, X_train.size(0)):
        model.train()
        optimizer.zero_grad()
        y_hat = model(X_train[i:i+1, :])
        loss = criterion(y_hat, Y_train[i:i+1, :])
        loss.backward()
        optimizer.step()

        if (i+1) % numCheck == 0:
            with torch.no_grad():
                model.eval()
                y_hat = model(X_train)
                train_acc.append(1 - torch.sum(torch.abs(torch.round(torch.sigmoid(y_hat)) - Y_train)).detach().numpy()/X_train.size(0))
                train_loss.append(criterion(y_hat, Y_train))
                y_hat = model(X_test)
                test_acc.append(1 - torch.sum(torch.abs(torch.round(torch.sigmoid(y_hat)) - Y_test)).detach().numpy() / X_test.size(0))
                test_loss.append(criterion(y_hat, Y_test))
                print("Iteration: %d Train Acc %.2f Test Acc %.2f" % (i+1, train_acc[(int)(i/numCheck)], test_acc[(int)(i/numCheck)]))
    return train_loss, train_acc, test_loss, test_acc

def main():

    model = Net()
    optimizer = optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))
    #optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    criterion = nn.BCEWithLogitsLoss() #y*log(predict) + (1-y)*log(1-predict) - binary_cross_entropy
    for stage in range(1, len(nTrain)+1):
        print("Stage - ", stage)
        X_train, Y_train = createData(nTrain[stage - 1], stage)
        X_test, Y_test = createData(nTest[stage - 1], stage)
        train_loss, train_acc, test_loss, test_acc = train(model, optimizer, criterion, X_train, Y_train, X_test, Y_test)
        # plt.plot(train_acc)
        # plt.plot(train_loss)
        # plt.show()

    torch.save(model, "./torchModel1.pt")

if __name__ == '__main__':
    main()