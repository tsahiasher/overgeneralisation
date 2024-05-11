import torch
import numpy as np
from torchvision import datasets, transforms
from PIL import Image
from matplotlib import pyplot as plt
from scipy.stats import pearsonr
import matplotlib.cm as cm

features_output = None


def class4_hook(module, input_, output):
    global features_output
    features_output = output


def main():
    global features_output
    device = 'cpu'
    mean = [0.19887728, 0.18706746, 0.12683741]
    std = [0.36040904, 0.34855344, 0.3049059]

    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])

    myalexnet = torch.load("./alexnetModel2_6_3d.pt", map_location=torch.device('cpu'))  # alexnetModelSingleDispersed6.pt
    myalexnet.eval()
    myalexnet.classifier[4].register_forward_hook(class4_hook)
    running_corrects = 0.0
    totalSamples = 0.0
    nc = np.array([])
    allFeaturs = np.array([])
    for j in range(3,28):
        if j==15:
            continue
        data_dir = 'data/Stage5/'+str(j)
        image_datasets = datasets.ImageFolder(data_dir, transform)
        dataloaders = torch.utils.data.DataLoader(image_datasets, batch_size=500, shuffle=True)
        iter_dataloaders = iter(dataloaders)
        totalSamples += iter_dataloaders.batch_sampler.sampler.num_samples
        counter=0
        print()
        for inputs, labels in iter_dataloaders:
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = myalexnet(inputs)  # .detach().numpy()
            _, preds = torch.max(outputs, 1)
            running_corrects += torch.sum(preds == labels.data)
            counter += inputs.shape[0]
            print('\r', j, ': ', counter, '/', iter_dataloaders.batch_sampler.sampler.num_samples, '    ', end='')
            nc = np.append(nc, np.full(inputs.shape[0],j))
            if allFeaturs.size == 0:
                allFeaturs = features_output.detach().numpy()
            else:
                allFeaturs = np.vstack((allFeaturs, features_output.detach().numpy()))
    print('\nNumber of corrects - ', running_corrects,' ',running_corrects.item()/totalSamples)
    np.save('allFeaturs1', allFeaturs)
    np.save('nc1',nc)
    allFeaturs = np.load('allFeaturs30.npy')
    nc = np.load('nc30.npy')
    corrCoef = np.zeros((4096,2))

    for i in range(4096):
        corrCoef[i,:] = pearsonr(allFeaturs[:,i], nc)
    mask = np.isnan(corrCoef)
    corrCoef[mask] = np.finfo(float).min
    sortedInd = np.argsort(corrCoef[:,0])[::-1]

    c = cm.rainbow(np.linspace(0, 1, 10))
    fig, ax = plt.subplots(figsize=(8, 8))

    imgIdx = np.random.random_integers(allFeaturs.shape[0], size=(10,)) - 1
    ncIdx = np.argsort(nc[imgIdx[:]])[::-1]

    for i in range(10):
        ax.plot(range(10), allFeaturs[imgIdx[ncIdx[i]],sortedInd[0:10]], color=c[i], label = str(nc[imgIdx[ncIdx[i]]]))
    ax.grid(axis='both', alpha=0.5, linestyle='--', linewidth=1)
    # ax.set_title('Neuron Rule')
    ax.legend(loc='upper left')
    ax.set_ylabel('Value')
    ax.set_xlabel('Neuron')
    ax.set_xticks(range(0, 10))
    plt.savefig('NeuronRule30.png')
    plt.show()

    exit()

    fig=plt.figure(figsize=(30, 30))
    for i in range(9):
        means = np.zeros((25))
        stds = np.zeros((25))
        for j in range(3,28):
            if j==15:
                continue
            means[j-3] = np.mean(allFeaturs[np.where(nc==j),sortedInd[i]])
            stds[j-3] = np.std(allFeaturs[np.where(nc==j),sortedInd[i]])
        ax = fig.add_subplot(3, 3, i+1)
        ax.grid(axis='both', alpha=0.5, linestyle='--', linewidth=1)
        #ax.set_title('Neuron Rule')
        #ax.scatter(nc, allFeaturs[:,sortedInd[i]], c='b', label = str(sortedInd[i]))
        ax.bar(np.arange(3,28), means, yerr=stds, align='center', alpha=0.5, ecolor='black', capsize=6, label = str(sortedInd[i]))
        text  = "r\u00b2 {:.2f}\np {:.2f}\n".format(corrCoef[sortedInd[i],0]*corrCoef[sortedInd[i],0], corrCoef[sortedInd[i],1])
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.05, 0.8, text, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        ax.legend(loc='upper left')
        ax.set_ylabel('Value')
        ax.set_xlabel('Number Congruent')
        ax.set_xticks(range(3,28))
    plt.savefig('NeuronRule5.png')
    plt.show()

if __name__ == '__main__':
    main()
