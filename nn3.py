import numpy as np
import random

class FF(object):
    """docstring for FF"""
    def __init__(self, layerDims):
        super(FF, self).__init__()
        self.n_layers = len(layerDims)-1
        self.weights = []
        self.biases = []
        for i in range(self.n_layers):
            self.weights.append(0.1 * np.random.randn(layerDims[i + 1], layerDims[i]))
            self.biases.append(np.zeros((layerDims[i + 1], 1)))

    def save(self):
        for i in range(self.n_layers):
            np.save("weight" + str(i), self.weights[i])

    def load(self):
        for i in range(self.n_layers):
            self.weights[i] = np.load("weight" + str(i)+".npy")

    def sgd(self, X, y, epochs, eta, mb_size, Xtest, ytest):
        N = X.shape[1]

        acc = self.eval_test(Xtest, ytest)

        updates = 0
        steps = [updates]
        test_acc = [acc]
        print("Starting training, test accuracy: {0}".format(acc))

        for i in range(epochs):
            for j in range(N):
                gradsW, gradsB = self.backprop(X[:, j:j+1], y[:, j:j+1])

                for k in range(self.n_layers):
                    self.weights[k] = self.weights[k] - (eta/mb_size)*gradsW[k]
                    self.biases[k] = self.biases[k] - (eta/mb_size)*gradsB[k]

                updates = updates + 1
                if updates%50 == 0:
                    steps.append(updates)
                    acc = self.eval_test(Xtest, ytest)
                    test_acc.append(acc)
                    #print (acc)

            acc = self.eval_test(Xtest, ytest)
            print("Done epoch {0}, test accuracy: {1}".format(i+1, acc))

        steps = np.asarray(steps)

        return steps, test_acc

        return steps, test_acc

    def backprop(self,X,y):
        # X is a matrix of size input_dim*mb_size
        # y is a matrix of size output_dim*mb_size
        # you should return a list 'grads' of length(weights) such
        # that grads[i] is a matrix containing the gradients of the
        # loss with respect to weights[i].

        # ForwardPass
        h = []
        s = [X]
        for i in range(self.n_layers):
            h.append(np.dot(self.weights[i], s[i]) + self.biases[i])
            s.append(FF.activation(h[i]))

        # BackwardPass
        d = [None] * self.n_layers
        d[self.n_layers - 1] = FF.activation_deriv(h[self.n_layers-1]) * FF.loss_deriv(y, s[self.n_layers])

        for i in range(self.n_layers - 2, -1, -1):
            d[i] = FF.activation_deriv(h[i]) * np.dot(self.weights[i + 1].T, d[i + 1])

        gw = []
        gb = []
        # Gradients
        for i in range(self.n_layers):
            gw.append(np.dot(d[i], s[i].T))
            gb.append(np.mean(d[i]))

        return gw, gb

    def predict(self,x):
        a = x
        for i in range(self.n_layers):
            a = FF.activation(np.dot(self.weights[i], a) + self.biases[i])

        return a

    def eval_test(self,Xtest, ytest):
        ypred = self.predict(Xtest)
        ypred = ypred == np.max(ypred, axis=0)

        return np.mean(np.all(ypred==ytest,axis=0))

    def activation(x):
        return np.tanh(x)

    def activation_deriv(x):
        return 1-(np.tanh(x)**2)

    def loss_deriv(output, target):
        # Derivative of loss function with respect to the activations
        # in the output layer.
        # we use quadratic loss, where L=0.5*||output-target||^2
        
        # YOUR CODE HERE
        return target - output

def createData(samplesNumber, stage = 1):

    x = np.ones((14, samplesNumber))
    y = np.ones((2, samplesNumber))

    if stage == 1:
        for i in range(samplesNumber):
            a = np.random.permutation([-0.5, 0.5])
            x[0, i] = np.random.choice(a, 1)
            x[1:4, i] = a[0]
            x[4:6, i] = a[1]
            x[6:14, i] = 0
            y[:, i] = [1, 0] if x[0, i] == a[0] else [0, 1]
    elif stage == 2:
        for i in range(samplesNumber):
            a = np.random.choice([-0.5, 0.5], 2, replace=False)
            x[0, i] = np.random.choice(a, 1)
            ind = random.randint(-5, -1)
            tmp = np.full(5, a[0])
            for j in range (ind, ind+2):
                tmp[j]= a[1]
            x[1:6, i] = tmp
            x[6:14, i] = 0
            y[:, i] = 1 if x[0, i] == a[0] else 0
    elif stage == 3:
        for i in range(samplesNumber):
            a = np.random.choice([10, 20, 30, 40, 50], 2, replace=False)
            a = (a - np.mean(a)) / np.std(a)
            x[0, i] = np.random.choice(a, 1)
            tmp = np.full(5, a[0])
            ind = random.randint(-5, -1)
            for j in range (ind, ind+2):
                tmp[j]= a[1]
            x[1:6, i] = tmp
            x[6:14, i] = -1
            y[:, i] = 1 if x[0, i] == a[0] else 0
    elif stage == 4:
        for i in range(samplesNumber):
            a = np.random.choice([10, 20, 30, 40, 50], 2, replace=False)
            a = (a - np.mean(a)) / np.std(a)
            x[0, i] = np.random.choice(a, 1)
            total = random.randint(6, 13)
            tmp = np.full(total, a[0])
            ind = random.randint(total*-1, -1)
            for j in range (ind, ind+2):
                tmp[j]= a[1]
            x[1:total+1, i] = tmp
            x[total+1:14, i] = -1
            y[:, i] = 1 if x[0, i] == a[0] else 0
    elif stage == 5:
        for i in range(samplesNumber):
            a = np.random.choice([10, 20, 30, 40, 50], 2, replace=False)
            a = (a - np.mean(a)) / np.std(a)
            x[0, i] = np.random.choice(a, 1)
            total = random.randint(7, 13)
            tmp = np.full(total, a[0])
            min = random.randint(3, int(total/2))
            most = total - min
            ind = random.randint(total*-1, -1)
            for j in range (ind, ind+min):
                tmp[j]= a[1]
            x[1:total+1, i] = tmp
            x[total+1:14, i] = -1
            y[:, i] = 1 if x[0, i] == a[0] else 0
    elif stage == 6:
        for i in range(samplesNumber):
            a = np.random.choice([10, 20, 30, 40, 50], 3, replace=False)
            a = (a - np.mean(a)) / np.std(a)
            x[0, i] = np.random.choice(a, 1)
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
            x[1:total+1, i] = tmp
            x[total+1:14, i] = -1
            y[:, i] = 1 if x[0, i] == a[0] else 0
    return x, y

def createDummyData(samplesNumber, stage = None):

    '''
    t = np.concatenate((np.random.uniform(1, 10, (DIM, samplesNumber)), np.random.uniform(11, 20, (DIM, samplesNumber))),axis=1)
    t = (t[:] - np.mean(t, axis=1, keepdims=True)) / np.std(t, axis=1, keepdims=True)
    N, M = t.shape
    x = np.ones((N + 1, M))
    x[:-1, :] = t
    '''

    x = np.concatenate((np.random.uniform(1, 10, (DIM, samplesNumber)), np.random.uniform(11, 20, (DIM, samplesNumber))), axis=1)
    x = (x[:] - np.mean(x, axis=1, keepdims=True)) / np.std(x, axis=1, keepdims=True)
    y = np.ones((2, samplesNumber * 2)).astype(np.int32)
    y[0, 0:samplesNumber] = 0
    y[1, samplesNumber: samplesNumber*2] = 0
    perm = np.random.permutation(samplesNumber * 2);
    return x[:, perm], y[:, perm]

DIM = 14
TSAMPLES = 2000
nTest = 1000

def main():

    np.random.seed(444)
    random.seed(444)
    layers_sizes = [DIM, 80, 2]
    epochs = 1
    eta = 0.05
    batch_size = 1

    net = FF(layers_sizes)
    for stage in range(1, 3):
        train_x, train_y = createData(TSAMPLES, stage)
        test_x, test_y = createData(nTest, stage)
        print("Stage " + str(stage))
        steps, test_acc = net.sgd(train_x, train_y, epochs, eta, batch_size, test_x, test_y)


if __name__ == '__main__':
    main()