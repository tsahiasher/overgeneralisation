
import tensorflow as tf
import numpy as np
import random

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

    return x, y

def main():

    sess = tf.Session()
    saver = tf.train.import_meta_graph('model.ckpt.meta')
    saver.restore(sess, tf.train.latest_checkpoint('./'))

    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name("x:0")
    y = graph.get_tensor_by_name("y:0")
    predict = graph.get_tensor_by_name("predict:0")

    for i, test in enumerate(["8.1A", "8.2A", "8.3A", "8.4U", "8.5U", "8.6U"]):
        test_x, test_y = createData(i+1)
        test_z = (test_x[:] - np.mean(test_x, axis=1, keepdims=True)) / np.std(test_x, axis=1, keepdims=True)
        predictedY = sess.run(predict, feed_dict={x: test_z, y: test_y})
        test_accuracy = np.mean(test_y == predictedY)
        print(str(test) + " test accuracy = %.2f%%" % (100. * test_accuracy))
        result = np.column_stack((predictedY, test_y, test_x))
        np.savetxt("result" + test + ".csv", result, delimiter=",")
    # print(sess.run(predict, feed_dict={x: test_x, y: test_y}))

    sess.close()

if __name__ == '__main__':
    main()