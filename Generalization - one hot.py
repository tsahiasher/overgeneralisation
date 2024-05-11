import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from net import Net
import matplotlib.pyplot as plt

DIM = 14
samplesNumber = 500
testNumber = 100
# nTrain = [500, 1000, 2000, 30000, 120000, 120000]
nTrain = [400, 1000, 2000, 3000, 6000, 3000]
nTest = [200, 200, 200, 300, 600, 100]


def createDummyData(samplesNumber, *_):
    x = np.concatenate(
        (np.random.uniform(0.5, 1, (samplesNumber, DIM)), np.random.uniform(-0.5, -1, (samplesNumber, DIM))))
    y = np.ones(samplesNumber * 2).astype(np.int32)
    y[0:samplesNumber] = 0
    # y[samplesNumber:2*samplesNumber, 1] = 0
    perm = np.random.permutation(samplesNumber * 2)

    return x[perm, :], y[perm]


def createData(samplesNumber, stage):
    x = np.zeros((samplesNumber, 70))
    y = np.ones(samplesNumber)
    c = np.eye(5).tolist()

    if stage == 1:
        for i in range(samplesNumber):
            a = np.random.permutation((0, 1)).astype(int)
            b = int(np.random.choice(a, 1))
            x[i, 0:5] = c[b]
            x[i, 5:20] = c[a[0]] * 3
            x[i, 20:30] = c[a[1]] * 2
            y[i] = 1 if b == a[0] else 0
    elif stage == 2:
        for i in range(samplesNumber):
            a = np.random.permutation((0, 1)).astype(int)
            b = int(np.random.choice(a, 1))
            x[i, 0:5] = c[b]
            ind = random.randint(-5, -1)
            tmp = np.full(25, c[a[0]] * 5)
            for j in range(ind, ind + 2):
                tmp[j * 5:j * 5 + 4] = c[a[1]][0:4]
                tmp[j * 5 + 4] = c[a[1]][4]
            x[i, 5:30] = tmp
            y[i] = 1 if b == a[0] else 0
    elif stage == 3:
        for i in range(samplesNumber):
            a = np.random.choice((0, 1, 2, 3, 4), 2, replace=False).astype(int)
            b = int(np.random.choice(a, 1))
            x[i, 0:5] = c[b]
            ind = random.randint(-5, -1)
            tmp = np.full(25, c[a[0]] * 5)
            for j in range(ind, ind + 2):
                tmp[j * 5:j * 5 + 4] = c[a[1]][0:4]
                tmp[j * 5 + 4] = c[a[1]][4]
            x[i, 5:30] = tmp
            y[i] = 1 if b == a[0] else 0
    elif stage == 4:
        for i in range(samplesNumber):
            a = np.random.choice((0, 1, 2, 3, 4), 2, replace=False).astype(int)
            b = int(np.random.choice(a, 1))
            x[i, 0:5] = c[b]
            total = random.randint(6, 13)
            tmp = np.full(total * 5, c[a[0]] * total)
            ind = random.randint(total * -1, -1)
            for j in range(ind, ind + 2):
                tmp[j * 5:j * 5 + 4] = c[a[1]][0:4]
                tmp[j * 5 + 4] = c[a[1]][4]
            x[i, 5:(total + 1) * 5] = tmp
            y[i] = 1 if b == a[0] else 0
    elif stage == 5:
        for i in range(samplesNumber):
            a = np.random.choice((0, 1, 2, 3, 4), 2, replace=False).astype(int)
            b = int(np.random.choice(a, 1))
            x[i, 0:5] = c[b]
            total = random.randint(7, 13)
            tmp = np.full(total * 5, c[a[0]] * total)
            least = random.randint(3, int((total - 1) / 2))
            ind = random.randint(total * -1, -1)
            for j in range(ind, ind + least):
                tmp[j * 5:j * 5 + 4] = c[a[1]][0:4]
                tmp[j * 5 + 4] = c[a[1]][4]
            x[i, 5:(total + 1) * 5] = tmp
            y[i] = 1 if b == a[0] else 0
    elif stage == 6:
        for i in range(samplesNumber):
            a = np.random.choice((0, 1, 2, 3, 4), 3, replace=False).astype(int)
            b = int(np.random.choice(a, 1))
            x[i, 0:5] = c[b]
            total = random.randint(11, 13)
            tmp = np.full(total * 5, c[a[0]] * total)
            least = 2
            mid = 3
            ind = random.randint(total * -1, -1)
            d = np.random.choice([least, mid], 2, replace=False)
            for j in range(ind, ind + d[0]):
                tmp[j * 5:j * 5 + 4] = c[a[1]][0:4]
                tmp[j * 5 + 4] = c[a[1]][4]
            for j in range(ind + d[0], ind + d[0] + d[1]):
                tmp[j * 5:j * 5 + 4] = c[a[2]][0:4]
                tmp[j * 5 + 4] = c[a[2]][4]
            if d[0] == least and b == a[2]:
                x[i, 0:5] = c[a[1]]
            if d[1] == least and b == a[1]:
                x[i, 0:5] = c[a[2]]
            x[i, 5:(total + 1) * 5] = tmp
            y[i] = 1 if b == a[0] else 0

    # x = (x[:] - np.mean(x, axis=1, keepdims=True)) / np.std(x, axis=1, keepdims=True)

    # print(stage, np.unique(x,axis=0).shape[0])

    X = torch.as_tensor(x, dtype=torch.float32).requires_grad_()
    Y = torch.as_tensor(y, dtype=torch.float32).reshape(samplesNumber, 1)

    return X, Y


def train(model, optimizer, criterion, X_train, Y_train, X_test, Y_test):
    train_loss = []
    train_acc = []
    test_loss = []
    test_acc = []
    numCheck = X_train.size(0) / 10
    for i in range(0, X_train.size(0)):
        model.train()
        optimizer.zero_grad()
        y_hat = model(X_train[i:i + 1, :])
        loss = criterion(y_hat, Y_train[i:i + 1, :])
        loss.backward()
        optimizer.step()

        if (i + 1) % numCheck == 0:
            with torch.no_grad():
                model.eval()
                y_hat = model(X_train)
                train_acc.append(1 - torch.sum(
                    torch.abs(torch.round(torch.sigmoid(y_hat)) - Y_train)).detach().numpy() / X_train.size(0))
                train_loss.append(criterion(y_hat, Y_train))
                y_hat = model(X_test)
                test_acc.append(
                    1 - torch.sum(torch.abs(torch.round(torch.sigmoid(y_hat)) - Y_test)).detach().numpy() / X_test.size(0))
                test_loss.append(criterion(y_hat, Y_test))
                print("Iteration: %d Train Acc %.2f Test Acc %.2f" % (
                    i + 1, train_acc[int(i / numCheck)], test_acc[int(i / numCheck)]))
    return train_loss, train_acc, test_loss, test_acc


def main():
    model = Net()
    optimizer = optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))
    # optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    criterion = nn.BCEWithLogitsLoss()  # y*log(sigmoid((predict)) + (1-y)*log(sigmoid(1-predict)) - binary_cross_entropy
    for stage in range(1, len(nTrain) + 1):
        print("Stage - ", stage)
        X_train, Y_train = createData(nTrain[stage - 1], stage)
        X_test, Y_test = createData(nTest[stage - 1], stage)
        train_loss, train_acc, test_loss, test_acc = train(model, optimizer, criterion, X_train, Y_train, X_test, Y_test)
        # plt.plot(train_acc)
        # plt.plot(train_loss)
        # plt.show()

    torch.save(model, "./torchModel.pt")


if __name__ == '__main__':
    main()
