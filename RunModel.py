import torch
import numpy as np
import random
from net import Net

samplesNumber = 2000


def createData(test):
    x = np.ones((samplesNumber, 70))
    y = np.ones((samplesNumber, 1))
    c = np.eye(5).tolist()

    if test == 1:
        for i in range(samplesNumber):
            a = np.random.choice((0, 1, 2, 3, 4), 3, replace=False).astype(int)
            x[i, 0:5] = c[a[0]]
            total = 13
            tmp = np.full(total * 5, c[a[0]] * total)
            least = 2
            mid = 4
            ind = random.randint(total * -1, -1)
            b = np.random.choice([least, mid], 2, replace=False)
            for j in range(ind, ind + b[0]):
                tmp[j * 5:j * 5 + 4] = c[a[1]][0:4]
                tmp[j * 5 + 4] = c[a[1]][4]
            for j in range(ind + b[0], ind + b[0] + b[1]):
                tmp[j * 5:j * 5 + 4] = c[a[2]][0:4]
                tmp[j * 5 + 4] = c[a[2]][4]
            x[i, 5:(total + 1) * 5] = tmp
            y[i] = 1
    elif test == 2:
        for i in range(samplesNumber):
            a = np.random.choice((0, 1, 2, 3, 4), 3, replace=False).astype(int)
            total = 13
            tmp = np.full(total * 5, c[a[0]] * total)
            least = 2
            mid = 4
            ind = random.randint(total * -1, -1)
            b = np.random.choice([least, mid], 2, replace=False)
            x[i, 0:5] = c[a[1]] if least == b[0] else c[a[2]]
            for j in range(ind, ind + b[0]):
                tmp[j * 5:j * 5 + 4] = c[a[1]][0:4]
                tmp[j * 5 + 4] = c[a[1]][4]
            for j in range(ind + b[0], ind + b[0] + b[1]):
                tmp[j * 5:j * 5 + 4] = c[a[2]][0:4]
                tmp[j * 5 + 4] = c[a[2]][4]
            x[i, 5:(total + 1) * 5] = tmp
            y[i] = 0
    if test == 3:
        for i in range(samplesNumber):
            a = np.random.choice((0, 1, 2, 3, 4), 3, replace=False).astype(int)
            total = 13
            tmp = np.full(total * 5, c[a[0]] * total)
            least = 3
            mid = 4
            ind = random.randint(total * -1, -1)
            b = np.random.choice([least, mid], 2, replace=False)
            x[i, 0:5] = c[a[1]] if least == b[0] else c[a[2]]
            for j in range(ind, ind + b[0]):
                tmp[j * 5:j * 5 + 4] = c[a[1]][0:4]
                tmp[j * 5 + 4] = c[a[1]][4]
            for j in range(ind + b[0], ind + b[0] + b[1]):
                tmp[j * 5:j * 5 + 4] = c[a[2]][0:4]
                tmp[j * 5 + 4] = c[a[2]][4]
            x[i, 5:(total + 1) * 5] = tmp
            y[i] = 0
    if test == 4:
        for i in range(samplesNumber):
            a = np.random.choice((0, 1, 2, 3, 4), 3, replace=False).astype(int)
            x[i, 0:5] = c[a[0]]
            total = 13
            tmp = np.full(total * 5, c[a[0]] * total)
            least = 3
            mid = 4
            ind = random.randint(total * -1, -1)
            b = np.random.choice([least, mid], 2, replace=False)
            for j in range(ind, ind + b[0]):
                tmp[j * 5:j * 5 + 4] = c[a[1]][0:4]
                tmp[j * 5 + 4] = c[a[1]][4]
            for j in range(ind + b[0], ind + b[0] + b[1]):
                tmp[j * 5:j * 5 + 4] = c[a[2]][0:4]
                tmp[j * 5 + 4] = c[a[2]][4]
            x[i, 5:(total + 1) * 5] = tmp
            y[i] = 1
    if test == 5:
        for i in range(samplesNumber):
            a = np.random.choice((0, 1, 2, 3, 4), 3, replace=False).astype(int)
            total = 13
            tmp = np.full(total * 5, c[a[0]] * total)
            least = 3
            mid = 4
            ind = random.randint(total * -1, -1)
            b = np.random.choice([least, mid], 2, replace=False)
            x[i, 0:5] = c[a[1]] if mid == b[0] else c[a[2]]
            for j in range(ind, ind + b[0]):
                tmp[j * 5:j * 5 + 4] = c[a[1]][0:4]
                tmp[j * 5 + 4] = c[a[1]][4]
            for j in range(ind + b[0], ind + b[0] + b[1]):
                tmp[j * 5:j * 5 + 4] = c[a[2]][0:4]
                tmp[j * 5 + 4] = c[a[2]][4]
            x[i, 5:(total + 1) * 5] = tmp
            y[i] = 0
    if test == 6:
        for i in range(samplesNumber):
            a = np.random.choice((0, 1, 2, 3, 4), 3, replace=False).astype(int)
            total = 13
            tmp = np.full(total * 5, c[a[0]] * total)
            least = 2
            mid = 4
            ind = random.randint(total * -1, -1)
            b = np.random.choice([least, mid], 2, replace=False)
            x[i, 0:5] = c[a[1]] if mid == b[0] else c[a[2]]
            for j in range(ind, ind + b[0]):
                tmp[j * 5:j * 5 + 4] = c[a[1]][0:4]
                tmp[j * 5 + 4] = c[a[1]][4]
            for j in range(ind + b[0], ind + b[0] + b[1]):
                tmp[j * 5:j * 5 + 4] = c[a[2]][0:4]
                tmp[j * 5 + 4] = c[a[2]][4]
            x[i, 5:(total + 1) * 5] = tmp
            y[i] = 0

    # x = (x[:] - np.mean(x, axis=1, keepdims=True)) / np.std(x, axis=1, keepdims=True)

    X = torch.as_tensor(x, dtype=torch.float32).requires_grad_()
    # Y = torch.as_tensor(y, dtype=torch.float32).reshape(samplesNumber, 1)

    return X, y


def main():
    model = torch.load("./torchModel.pt")
    model.eval()

    for i, test in enumerate(["8.1U", "8.2U", "8.3U", "8.4A", "8.5A", "8.6A"]):
        X_test, Y_test = createData(i + 1)
        with torch.no_grad():
            y_hat = model(X_test)
            acc = 1 - np.sum(np.abs(np.round(torch.sigmoid(y_hat).detach().numpy()) - Y_test)) / X_test.size(0)
            print(str(test) + " test accuracy = %.2f" % acc)
            result = np.column_stack((np.round(torch.sigmoid(y_hat).detach().numpy()), Y_test, X_test.detach().numpy()))
        np.savetxt("result" + test + ".csv", result, delimiter=",")


if __name__ == '__main__':
    main()
