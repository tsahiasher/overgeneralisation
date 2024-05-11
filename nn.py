import numpy as np
import matplotlib.pyplot as plt
import math

def sigmoid(x):
    return 1.0/(1+ np.exp(-x))

def sigmoid_derivative(x):
    return x * (1.0 - x)

class NeuralNetwork:
    def __init__(self, x, y0):
        self.x = x
        self.w1 = np.random.rand(self.x.shape[1],4)
        self.w2 = np.random.rand(4,1)
        self.y0 = y0
        self.y = np.zeros(self.y0.shape)

    def feedforward(self):
        self.layer1 = sigmoid(np.dot(self.x, self.w1))
        self.y = sigmoid(np.dot(self.layer1, self.w2))

    def backprop(self):
        error = 2*(self.y0 - self.y)
        delta2 = error * sigmoid_derivative(self.y)
        dw2 = np.dot(self.layer1.T, delta2)
        delta1 = np.dot(delta2, self.w2.T) * sigmoid_derivative(self.layer1)
        dw1 = np.dot(self.x.T, delta1)
        self.w2 += dw2
        self.w1 += dw1

def main():
    x = np.array([[0, 0, 1],
                  [0, 1, 1],
                  [1, 0, 1],
                  [1, 1, 1]])
    y0 = np.array([[0], [1], [1], [0]])
    nn = NeuralNetwork(x, y0)

    for i in range(1500):
        nn.feedforward()
        nn.backprop()

    print(nn.y)

if __name__ == "__main__":
    main()