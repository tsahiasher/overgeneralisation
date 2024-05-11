import torch
import numpy as np
from torchvision import datasets, transforms
from PIL import Image
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt

features_output = None


def class4_hook(module, input_, output):
    global features_output
    features_output = output


def main():
    global features_output
    s = 2000
    t = 50
    se = s - t - 1

    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.19887728, 0.18706746, 0.12683741], [0.36040904, 0.34855344, 0.3049059]),
    ])

    mean = np.array([0.19887728, 0.18706746, 0.12683741])
    std = np.array([0.36040904, 0.34855344, 0.3049059])
    data_dir = 'DataSet-ordered-most/vis'  # -ordered-most
    image_datasets = datasets.ImageFolder(data_dir, transform)
    dataloaders = torch.utils.data.DataLoader(image_datasets, batch_size=500, shuffle=True)
    myalexnet = torch.load("./alexnetModelSingle6.pt",
                           map_location=torch.device('cpu'))  # alexnetModelSingleDispersed6.pt
    myalexnet.eval()
    myalexnet.classifier[4].register_forward_hook(class4_hook)
    inputs, labels = next(iter(dataloaders))
    outputs = myalexnet(inputs).detach().numpy()
    features_output = TSNE(n_components=2, random_state=0).fit_transform(features_output.detach().numpy())

    inp = (np.clip((std * (inputs.detach().numpy().transpose((0, 2, 3, 1))) + mean), 0, 1) * 255.0).astype(np.uint8)
    img = []
    for i in range(len(outputs)):
        img.append(Image.fromarray(inp[i], 'RGB').resize((t, t)))
    colors = 'r', 'b'

    for a, fname in zip([outputs, features_output], ['vis-ordered', 't-sne-ordered']):  # -dispersed -ordered
        plt.subplots(figsize=(7, 7))
        for i, c in zip([0, 1], colors):
            plt.scatter(a[labels.detach().numpy() == i, 0], a[labels.detach().numpy() == i, 1], c=c, label=str(i))
        plt.legend()
        plt.savefig(fname + '-label.png')

        a -= a.min(axis=0)
        a *= se / a.max(axis=0)
        npimg = np.zeros((s, s, 3))
        for i in range(len(outputs)):
            n = int(a[i, 0])
            m = se - int(a[i, 1])
            npimg[m:m + t, n:n + t, :] = np.array(img[i])
        Image.fromarray(npimg.astype(np.uint8), "RGB").save(fname + '-img.png')


if __name__ == '__main__':
    main()
