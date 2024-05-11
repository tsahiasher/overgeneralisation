import os
import random
import datetime
import numpy as np
import matplotlib.pyplot as plt

## constants
TRAIN_SIZE = 25000
TEST_SIZE = 12500
DEV_RATIO = 0.1
IMAGE_HEIGHT = IMAGE_WIDTH = 128

LEARNING_RATE = 0.0001
MINIBATCH_SIZE = 32
INPUT_SIZE = IMAGE_HEIGHT * IMAGE_WIDTH * 3
OUTPUT_SIZE = 2

def initialize_parameters(n_x, n_h, n_y):
    """
    Argument:
    n_x -- size of the input layer
    n_h -- size of the hidden layer
    n_y -- size of the output layer

    Returns:
    params -- python dictionary containing your parameters:
                    W1 -- weight matrix of shape (n_h, n_x)
                    b1 -- bias vector of shape (n_h, 1)
                    W2 -- weight matrix of shape (n_y, n_h)
                    b2 -- bias vector of shape (n_y, 1)
    """

    W1 = np.random.randn(n_h, n_x) * 0.01
    b1 = np.zeros((n_h, 1))
    W2 = np.random.randn(n_y, n_h) * 0.01
    b2 = np.zeros((n_y, 1))

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}

    return parameters

def sigmoid(z):
    s = 1.0 / (1.0 + np.exp(-1.0 * z))
    return s

def forward_propagation(X, parameters):
    """
    Argument:
    X -- input data of size (n_x, m)
    parameters -- python dictionary containing your parameters (output of initialization function)
            W1 -- weight matrix of shape (n_h, n_x)
            b1 -- bias vector of shape (n_h, 1)
            W2 -- weight matrix of shape (n_y, n_h)
            b2 -- bias vector of shape (n_y, 1)

    Returns:
    A2 -- The sigmoid output of the second activation
    cache -- a dictionary containing "Z1", "A1", "Z2" and "A2"
    """
    # Retrieve each parameter from the dictionary "parameters"
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]

    # Implement Forward Propagation to calculate A2 (probabilities)
    # print(W1.shape, X.shape)
    # print(np.matmul(W1, X).shape, b1.shape)
    Z1 = np.add(np.matmul(W1, X), b1)
    A1 = np.tanh(Z1)
    Z2 = np.add(np.matmul(W2, A1), b2)
    A2 = sigmoid(Z2)

    assert (A2.shape == (1, X.shape[1]))

    cache = {"Z1": Z1,
             "A1": A1,
             "Z2": Z2,
             "A2": A2}

    return A2, cache


def compute_cost(A2, Y, parameters):
    """
    Computes the cross-entropy cost given in equation (13)

    Arguments:
    A2 -- The sigmoid output of the second activation, of shape (1, number of examples)
    Y -- "true" labels vector of shape (1, number of examples)
    parameters -- python dictionary containing your parameters W1, b1, W2 and b2

    Returns:
    cost -- cross-entropy cost given equation (13)
    """

    m = Y.shape[1]  # number of example

    # Compute the cross-entropy cost
    logprobs = np.multiply(Y, np.log(A2)) + np.multiply((1 - Y), np.log(1 - A2))
    # print(logprobs.shape)
    cost = (-1.0 / m) * np.sum(logprobs)

    cost = np.squeeze(cost)  # makes sure cost is the dimension we expect.
    # E.g., turns [[17]] into 17
    assert (isinstance(cost, float))

    return cost

def backward_propagation(parameters, cache, X, Y):
    """
    Implement the backward propagation using the instructions above.

    Arguments:
    parameters -- python dictionary containing our parameters 
    cache -- a dictionary containing "Z1", "A1", "Z2" and "A2".
    X -- input data of shape (2, number of examples)
    Y -- "true" labels vector of shape (1, number of examples)

    Returns:
    grads -- python dictionary containing your gradients with respect to different parameters
    """
    m = X.shape[1]

    # First, retrieve W1 and W2 from the dictionary "parameters".
    W1 = parameters["W1"]
    W2 = parameters["W2"]

    # Retrieve also A1 and A2 from dictionary "cache".
    A1 = cache["A1"]
    A2 = cache["A2"]

    # Backward propagation: calculate dW1, db1, dW2, db2. 
    dZ2 = A2 - Y
    dW2 = (1.0 / m) * np.matmul(dZ2, np.transpose(A1))
    db2 = (1.0 / m) * np.sum(dZ2, axis=1, keepdims=True)
    dZ1 = np.matmul(np.transpose(W2), dZ2) * (1 - np.power(A1, 2))
    dW1 = (1.0 / m) * np.matmul(dZ1, np.transpose(X))
    db1 = (1.0 / m) * np.sum(dZ1, axis=1, keepdims=True)

    grads = {"dW1": dW1,
             "db1": db1,
             "dW2": dW2,
             "db2": db2}

    return grads

def update_parameters(parameters, grads, learning_rate=1.2):
    """
    Updates parameters using the gradient descent update rule given above

    Arguments:
    parameters -- python dictionary containing your parameters 
    grads -- python dictionary containing your gradients 

    Returns:
    parameters -- python dictionary containing your updated parameters 
    """
    # Retrieve each parameter from the dictionary "parameters"
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]

    # Retrieve each gradient from the dictionary "grads"
    dW1 = grads["dW1"]
    db1 = grads["db1"]
    dW2 = grads["dW2"]
    db2 = grads["db2"]

    # Update rule for each parameter
    W1 = W1 - learning_rate * dW1
    b1 = b1 - learning_rate * db1
    W2 = W2 - learning_rate * dW2
    b2 = b2 - learning_rate * db2

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}

    return parameters

def nn_model(X, Y, n_h, num_iterations=10000, learning_rate=1.2, print_cost=False):
    """
    Arguments:
    X -- dataset of shape (n_x, number of examples)
    Y -- labels of shape (n_y, number of examples)
    n_h -- size of the hidden layer
    num_iterations -- Number of iterations in gradient descent loop
    print_cost -- if True, print the cost every 1000 iterations

    Returns:
    parameters -- parameters learnt by the model. They can then be used to predict.
    """

    n_x = X.shape[0]
    n_y = Y.shape[0]

    # Initialize parameters, then retrieve W1, b1, W2, b2. Inputs: "n_x, n_h, n_y". Outputs = "W1, b1, W2, b2, parameters".
    parameters = initialize_parameters(n_x, n_h, n_y)
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]

    # Loop (gradient descent)
    costs = []
    for i in range(0, num_iterations):

        # Forward propagation. Inputs: "X, parameters". Outputs: "A2, cache".
        A2, cache = forward_propagation(X, parameters)

        # Cost function. Inputs: "A2, Y, parameters". Outputs: "cost".
        cost = compute_cost(A2, Y, parameters)
        costs.append(cost)

        # Backpropagation. Inputs: "parameters, cache, X, Y". Outputs: "grads".
        grads = backward_propagation(parameters, cache, X, Y)

        # Gradient descent parameter update. Inputs: "parameters, grads". Outputs: "parameters".
        parameters = update_parameters(parameters, grads, learning_rate=learning_rate)

        # cache all about model
        trained_model = {
            "layer_sizes": (n_x, n_h, n_y),
            "learning_rate": learning_rate,
            "costs": costs,
            "parameters": parameters
        }

        # Print the cost every 1000 iterations
        if print_cost and i % 1000 == 0:
            print("Cost after iteration %i: %f" % (i, cost))

    return trained_model

def predict(parameters, X):
    """
    Using the learned parameters, predicts a class for each example in X

    Arguments:
    parameters -- python dictionary containing your parameters 
    X -- input data of size (n_x, m)

    Returns
    predictions -- vector of predictions of our model (red: 0 / blue: 1)
    """

    # Computes probabilities using forward propagation, and classifies to 0/1 using 0.5 as the threshold.
    A2, cache = forward_propagation(X, parameters)
    predictions = A2 > 0.5

    return predictions

def plot_costs(trained_model):
    # Plot learning curve (with costs)
    costs = np.squeeze(trained_model["costs"])
    plt.plot(costs)
    plt.ylabel('cost')
    plt.xlabel('iterations (per hundreds)')
    plt.title("Learning rate ={}\n, layer_sizes={}\n, accuracy:{}, m:{}\n".format(
        trained_model["learning_rate"], trained_model["layer_sizes"],
        trained_model.get("accuracy"), trained_model.get("m")
    ))
    plt.show()

DIM = 2
TSAMPLES = 10
train_images = np.concatenate((np.random.uniform(0,10,(DIM,TSAMPLES)),np.random.uniform(90,100,(DIM,TSAMPLES))),axis=1)
train_labels = np.concatenate(([np.zeros(TSAMPLES)],[np.ones(TSAMPLES)]),axis=1).astype(int)

dev_images = np.concatenate((np.random.uniform(0,10,(DIM,TSAMPLES)),np.random.uniform(90,100,(DIM,TSAMPLES))),axis=1)
dev_labels = np.concatenate((np.zeros(TSAMPLES),np.ones(TSAMPLES))).astype(int)

n_x = train_images.shape[0]  # size of input layer
n_h = 4  # hard code the hidden layer size to be 4
n_y = train_labels.shape[0]  # size of output layer

layer_sizes = (n_x, n_h, n_y)
print(layer_sizes)

# Example of a picture that was wrongly classified.
trained_model = nn_model(train_images, train_labels, n_h, num_iterations=50)


# ### 6. Lab

print("num of training data:{}".format(train_images.shape[1]))


# This may take about 2 minutes to run
m = 180
hidden_layer_sizes = [1, 2, 3, 4, 5, 20, 50]
learning_rate = 1.2
num_iterations = 50
trained_models = []

for n_h in hidden_layer_sizes:
    trained_model = nn_model(train_images, train_labels, n_h, num_iterations=num_iterations,
                             learning_rate=learning_rate)
    predictions = predict(trained_model["parameters"], dev_images)
    accuracy = float(
        (np.dot(dev_labels, predictions.T) + np.dot(1 - dev_labels, 1 - predictions.T)) / float(dev_labels.size) * 100)
    print("Accuracy for {} hidden units: {} %".format(n_h, accuracy))
    ## cache trained_model
    trained_model["accuracy"] = accuracy
    trained_model["m"] = m
    trained_model["num_iterations"] = num_iterations
    trained_models.append(trained_model)
    ## plot costs
    plt.figure(num=None, figsize=(15, 6), dpi=50, facecolor='w', edgecolor='k')
    plot_costs(trained_model)

'''
# ** 6.2 More Training data **
# 
# set m = 9800, hidden_layer_sizes = [5, 20, 50]

images, labels = load_data(file_count=25000)
dev_images, train_images = split_data(images)
dev_labels, train_labels = split_data(labels)


# This may take about 2 minutes to run
m = 22500
hidden_layer_sizes = [5, 20, 50]
num_iterations = 50
learning_rate = 1.2

print(datetime.datetime.now())
hidden_layer_sizes = [5, 20, 50]
for n_h in hidden_layer_sizes:
    trained_model = nn_model(train_images, train_labels, 5, num_iterations=num_iterations, learning_rate=learning_rate)
    predictions = predict(trained_model["parameters"], dev_images)
    accuracy = float(
        (np.dot(dev_labels, predictions.T) + np.dot(1 - dev_labels, 1 - predictions.T)) / float(dev_labels.size) * 100)
    print("Accuracy for {} hidden units: {} %".format(n_h, accuracy))
    ## cache trained_model
    trained_model["accuracy"] = accuracy
    trained_model["m"] = m
    trained_model["num_iterations"] = num_iterations
    trained_models.append(trained_model)
    ## plot costs
    plt.figure(num=None, figsize=(15, 6), dpi=50, facecolor='w', edgecolor='k')
    plot_costs(trained_model)

    print(datetime.datetime.now())

# ** 6.3 Less learning_rate **
# 
# set m = 9800, hidden_layer_sizes = 5, learning_rates = [1.2, 0.5, 0.1, 0.05, 0.01]


images, labels = load_data(file_count=10000)
dev_images, train_images = split_data(images)
dev_labels, train_labels = split_data(labels)


m = 22500
hidden_layer_size = 5
learning_rates = [1.2, 0.5, 0.1, 0.05, 0.01]
num_iterations = 50

print(datetime.datetime.now())
for learning_rate in learning_rates:
    trained_model = nn_model(train_images, train_labels, hidden_layer_size, num_iterations=num_iterations,
                             learning_rate=learning_rate, print_cost=True)
    predictions = predict(trained_model["parameters"], dev_images)
    accuracy = float(
        (np.dot(dev_labels, predictions.T) + np.dot(1 - dev_labels, 1 - predictions.T)) / float(dev_labels.size) * 100)
    print("Accuracy for {} learning_rate: {} %".format(learning_rate, accuracy))
    ## cache trained_model
    trained_model["accuracy"] = accuracy
    trained_model["m"] = m
    trained_model["num_iterations"] = num_iterations
    trained_models.append(trained_model)
    ## plot costs
    plt.figure(num=None, figsize=(15, 6), dpi=50, facecolor='w', edgecolor='k')
    plot_costs(trained_model)

    print(datetime.datetime.now())

# ** 6.4 More num_iterations **
# 
# set m = 9800, hidden_layer_sizes = 5, learning_rates = 0.05, num_iterations = [50, 100, 500, 2000] 


images, labels = load_data(file_count=10000)
dev_images, train_images = split_data(images)
dev_labels, train_labels = split_data(labels)

m = 9800
hidden_layer_sizes = 5
num_iterations = [50, 100, 500, 1000]
learning_rate = 0.05

print(datetime.datetime.now())
for num in num_iterations:
    trained_model = nn_model(train_images, train_labels, hidden_layer_sizes, num_iterations=num,
                             learning_rate=learning_rate)
    predictions = predict(trained_model["parameters"], dev_images)
    accuracy = float(
        (np.dot(dev_labels, predictions.T) + np.dot(1 - dev_labels, 1 - predictions.T)) / float(dev_labels.size) * 100)
    print("Accuracy for {} iterations: {} %".format(num, accuracy))

    ## cache trained_model
    trained_model["accuracy"] = accuracy
    trained_model["m"] = m
    trained_model["num_iterations"] = num
    trained_models.append(trained_model)
    ## plot costs
    plt.figure(num=None, figsize=(15, 6), dpi=50, facecolor='w', edgecolor='k')
    plot_costs(trained_model)

    print(datetime.datetime.now())

# ** 6.5 Less learning_rate **
# 
# set m = 9800, hidden_layer_sizes = 5, num_iterations=200, learning_rates = [0.05, 0.01, 0.005]


images, labels = load_data(file_count=10000)
dev_images, train_images = split_data(images)
dev_labels, train_labels = split_data(labels)

m = 9800
hidden_layer_sizes = 5
num_iterations = 200
learning_rates = [0.05, 0.01, 0.005]

print(datetime.datetime.now())
for learning_rate in learning_rates:
    trained_model = nn_model(train_images, train_labels, hidden_layer_sizes, num_iterations=num_iterations,
                             learning_rate=learning_rate)
    predictions = predict(trained_model["parameters"], dev_images)
    accuracy = float(
        (np.dot(dev_labels, predictions.T) + np.dot(1 - dev_labels, 1 - predictions.T)) / float(dev_labels.size) * 100)
    print("Accuracy for {} learning_rate: {} %".format(learning_rate, accuracy))

    ## cache trained_model
    trained_model["m"] = m
    trained_model["accuracy"] = accuracy
    trained_model["num_iterations"] = num_iterations
    ## plot costs
    plt.figure(num=None, figsize=(15, 6), dpi=50, facecolor='w', edgecolor='k')
    plot_costs(trained_model)

    print(datetime.datetime.now())

# ** 6.6 More num_iterations **
# 
# set m = 9800, hidden_layer_sizes = 5, learning_rates = 0.01, num_iterations = [200, 500] 


images, labels = load_data(file_count=10000)
dev_images, train_images = split_data(images)
dev_labels, train_labels = split_data(labels)

m = 22500
hidden_layer_sizes = 5
num_iterations = [200, 500]
learning_rate = 0.01

print(datetime.datetime.now())
for num in num_iterations:
    trained_model = nn_model(train_images, train_labels, hidden_layer_sizes, num_iterations=num,
                             learning_rate=learning_rate)
    predictions = predict(trained_model["parameters"], dev_images)
    accuracy = float(
        (np.dot(dev_labels, predictions.T) + np.dot(1 - dev_labels, 1 - predictions.T)) / float(dev_labels.size) * 100)
    print("Accuracy for {} iterations: {} %".format(num, accuracy))

    ## cache trained_model
    trained_model["accuracy"] = accuracy
    trained_model["m"] = m
    trained_model["num_iterations"] = num
    trained_models.append(trained_model)
    ## plot costs
    plt.figure(num=None, figsize=(15, 6), dpi=50, facecolor='w', edgecolor='k')
    plot_costs(trained_model)

    print(datetime.datetime.now())

import pandas as pd

df = pd.DataFrame(trained_models)


df.head(10)


len(trained_models)


plt.figure(num=None, figsize=(20, 20), dpi=200, facecolor='w', edgecolor='k')
for i in range(len(trained_models)):
    plt.subplot(921 + i)
    plot_costs(trained_models[i])

'''