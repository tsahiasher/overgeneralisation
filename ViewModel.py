import torch
import numpy as np
from torchvision import datasets, models, transforms
import torch.nn as nn
import matplotlib.pyplot as plt
from math import sqrt, ceil

def visualize_grid(Xs, ubound=255.0, padding=1):
  """
  Reshape a 4D tensor of image data to a grid for easy visualization.

  Inputs:
  - Xs: Data of shape (N, H, W, C)
  - ubound: Output grid will have values scaled to the range [0, ubound]
  - padding: The number of blank pixels between elements of the grid
  """
  (N, H, W, C) = Xs.shape
  grid_size = int(ceil(sqrt(N)))
  grid_height = H * grid_size + padding * (grid_size - 1)
  grid_width = W * grid_size + padding * (grid_size - 1)
  if C==1:
      grid = np.zeros((grid_height, grid_width))
  else:
      grid = np.zeros((grid_height, grid_width, C))
  next_idx = 0
  y0, y1 = 0, H
  for y in range(grid_size):
    x0, x1 = 0, W
    for x in range(grid_size):
      if next_idx < N:
        img = Xs[next_idx]
        if C==1:
            img = img.reshape(H, W)
        low, high = np.min(img), np.max(img)
        grid[y0:y1, x0:x1] = ubound * (img - low) / (high - low)
        # grid[y0:y1, x0:x1] = Xs[next_idx]
        next_idx += 1
      x0 += W + padding
      x1 += W + padding
    y0 += H + padding
    y1 += H + padding
  # grid_max = np.max(grid)
  # grid_min = np.min(grid)
  # grid = ubound * (grid - grid_min) / (grid_max - grid_min)
  return grid


def main():

    device = 'cpu' # torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    #myalexnet = torch.load("./FullalexnetModelSingle6.pt")
    #myalexnet = torch.load("./FullalexnetModelSingle6.pt")
    alexnet = models.alexnet(pretrained=True)
    alexnet = alexnet.to(device)

    #myalexnet = myalexnet.to(device)

    W1 = alexnet.features[0].weight.data.numpy()
    #myW1 = myalexnet.features[0].weight.data.numpy()
    #print(np.isclose(W1, myW1, rtol=1e-01, atol=1e-02))

    W1 = W1.transpose(0, 3, 2, 1)
    plt.imshow(visualize_grid(W1, padding=3).astype('uint8'))
    plt.gca().axis('off')
    plt.show()

    W2 = alexnet.features[3].weight.data.numpy()
    W2 = W2[0].reshape(64,1,5,5).transpose(0, 3, 2, 1)
    W = visualize_grid(W2, padding=3)
    plt.imshow(W , cmap='gray')
    plt.gca().axis('off')
    plt.show()

if __name__ == '__main__':
    main()
