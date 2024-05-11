import tensorflow as tf
import numpy as np
import random

RANDOM_SEED = 444
DIM = 70
TSAMPLES = 2000
MID_LAYER_NEURONS = 50
nTrain = [400, 1000, 2000, 3000, 6000, 3000]
nTest = [200, 200, 200, 300, 600, 300]
learning_rate = 0.01


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
    return x, y


def createDummyData(samplesNumber, stage=None):
    '''
    N, M = t.shape
    x = np.ones((N, M + 1))
    x[:, :-1] = t
    '''
    x = np.concatenate((np.random.uniform(1, 10, (TSAMPLES, DIM)), np.random.uniform(11, 20, (TSAMPLES, DIM))))
    y = np.ones(TSAMPLES * 2).astype(np.int32)
    y[0:TSAMPLES] = 0
    perm = np.random.permutation(TSAMPLES * 2);
    return x[perm], y[perm]


def main():
    '''
    tf.set_random_seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)
    '''

    # Layer's sizes
    x_size = DIM  # Number of input dimensions
    h1_size = MID_LAYER_NEURONS  # Number of hidden nodes
    y_size = 1  # Y_train.shape[0]   # Number of outcomes

    # Symbols
    x = tf.placeholder("float", shape=[None, x_size], name="x")
    y = tf.placeholder("int32", shape=None, name="y")

    # Weight initializations
    w_1 = tf.Variable(tf.truncated_normal([x_size, h1_size], mean=0, stddev=1 / np.sqrt(x_size)), name='weights1')
    b_1 = tf.Variable(tf.zeros([h1_size]), name='biases1')

    w_2 = tf.Variable(tf.random_normal([h1_size, y_size + 1], mean=0, stddev=1 / np.sqrt(h1_size)), name='weights')
    b_2 = tf.Variable(tf.zeros([y_size + 1]), name='biases2')

    # Forward propagation
    h1 = tf.nn.relu(tf.matmul(x, w_1) + b_1)  # The activation function
    # h = tf.nn.sigmoid(tf.matmul(x, w_1))  # The activation function

    yhat = tf.matmul(h1, w_2) + b_2  # The \varphi function

    # Backward propagation
    cost = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=yhat))
    # Loss function with L2 Regularization with beta=0.01
    # regularizers = tf.nn.l2_loss(weights_1) + tf.nn.l2_loss(weights_2)
    # loss = tf.reduce_mean(loss + beta * regularizers)

    updates = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

    predict = tf.argmax(yhat, axis=1, name="predict")
    tf.summary.histogram("predict", predict)
    # predict = tf.nn.softmax(yhat, axis=1)

    tf.summary.scalar('cost', cost)

    saver = tf.train.Saver()

    # Run SGD
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)
    writer = tf.summary.FileWriter("./TrainResults")
    writer.add_graph(sess.graph)
    graph = tf.get_default_graph()
    batchSize = 1

    for stage in range(1, len(nTrain) + 1):
        print("Stage - " + str(stage))
        X_train, Y_train = createData(nTrain[stage - 1], stage)
        X_test, Y_test = createData(nTest[stage - 1], stage)
        numCheck = X_train.shape[0] / 10
        for i in range(X_train.shape[0]):
            # merged_summary = tf.summary.merge_all()
            # summary, _ = sess.run([merged_summary, updates], feed_dict={X: train_X[i: i + batchSize], y: Y_train[i: i + batchSize]})
            sess.run(updates, feed_dict={x: X_train[i: i + batchSize], y: Y_train[i: i + batchSize]})
            # writer.add_summary(summary, i)
            if (i + 1) % numCheck == 0:
                train_accuracy = np.mean(Y_train == sess.run(predict, feed_dict={x: X_train, y: Y_train}))
                predictedY = sess.run(predict, feed_dict={x: X_test, y: Y_test})
                test_accuracy = np.mean(Y_test == predictedY)

                print("train accuracy = %.2f%%, test accuracy = %.2f%%" % (100. * train_accuracy, 100. * test_accuracy))

        train_accuracy = np.mean(Y_train == sess.run(predict, feed_dict={x: X_train, y: Y_train}))
        predictedY = sess.run(predict, feed_dict={x: X_test, y: Y_test})
        test_accuracy = np.mean(Y_test == predictedY)

        print("train accuracy = %.2f%%, test accuracy = %.2f%%" % (100. * train_accuracy, 100. * test_accuracy))

        result = np.column_stack((predictedY, Y_test,
                                  X_test))
        np.savetxt("result" + str(stage) + ".csv", result, delimiter=",")

    # write results to summary file
    # writer.add_summary(summary, epoch)

    saver.save(sess, "./model.ckpt")

    sess.close()


if __name__ == '__main__':
    main()
