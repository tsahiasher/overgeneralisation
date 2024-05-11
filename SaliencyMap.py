import torch
import numpy as np
from torchvision import transforms, models
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.io import imsave
from PIL import Image
from torchvision.utils import make_grid


def preprocess(img):
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.19887728, 0.18706746, 0.12683741], [0.36040904, 0.34855344, 0.3049059]),
        transforms.Lambda(lambda x: x[None]),
    ])
    return transform(img)


def rgb2gray(rgb):
        return np.dot(rgb, [0.299, 0.587, 0.114])

def compute_saliency_maps(X, y, model):
    scores = model(X)

    scores = scores.gather(1, y.view(-1, 1)).squeeze()
    scores.backward(torch.FloatTensor([1.0, 1.0, 1.0]))
    # scores.backward(torch.FloatTensor([1.0]).data[0], retain_graph = True)
    #scores.backward()


    saliency = X.grad.data
    saliency = saliency.abs()
    saliency, i = torch.max(saliency, dim=1)

    #saliency = saliency[0].detach().numpy().transpose(2,1,0)
    #saliency = np.sum(np.abs(saliency), axis=2)
    #saliency = rgb2gray(saliency)
    return saliency


def show_saliency_maps(X, y, model):
    X_tensor = torch.cat([preprocess(Image.fromarray(x)) for x in X], dim=0)
    y_tensor = torch.LongTensor(y)
    X_tensor.requires_grad = True

    saliency = compute_saliency_maps(X_tensor, y_tensor, model)

    #saliency = saliency.numpy()
    N = X.shape[0]
    for i in range(N):
        plt.subplot(2, N, i + 1)
        plt.imshow(X[i])
        plt.axis('off')
        plt.title(y[i]) 
        plt.subplot(2, N, N + i + 1)
        plt.imshow(saliency[i], cmap=plt.cm.hot)
        plt.axis('off')
    plt.show()


def main():
    img = np.zeros((3, 400, 400, 3)).astype(np.uint8)
    img[0] = (imread('s1.png')[:, :, :3]).astype(np.uint8)
    img[1] = (imread('s2.png')[:, :, :3]).astype(np.uint8)
    img[2] = (imread('s3.png')[:, :, :3]).astype(np.uint8)
    y = np.ones(3)
    #myalexnet = models.alexnet(pretrained=True)
    myalexnet = torch.load("./alexnetModelSingle6.pt", map_location=torch.device('cpu'))
    myalexnet.eval()
    show_saliency_maps(img, y, myalexnet)


if __name__ == '__main__':
    main()
