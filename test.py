import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy


def main():
    # plt.ion()  # interactive mode


    acc = []
    acc.append(1)
    acc.append(2)

    loss = []
    loss.append(6)
    loss.append(4)

    p = range(2)
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlabel('Epocs')
    ax.plot(p, acc, c='b')
    ax.grid(axis='both', alpha=0.5, linestyle='--', linewidth=1)

    ax1 = ax.twinx()
    ax1.plot(p, loss, c='tab:orange')

    plt.show()



if __name__ == '__main__':
    main()
