import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
from torchvision import datasets, models, transforms
import torchvision
import matplotlib.pyplot as plt
import time
import os
import copy

# ordered
mean_ordered = [[0.14698932, 0.07864558, 0.07864558],
        [0.1470285, 0.07893109, 0.07893109],
        [0.10425095, 0.09806027, 0.06648784],
        [0.16401494, 0.15427534, 0.10460336],
        [0.17739601, 0.16686181, 0.11313736],
        [0.18770611, 0.17655967, 0.11971281]]
std_ordered = [[0.33980202, 0.26861356, 0.26861356],
       [0.33989204, 0.26905882, 0.26905882],
       [0.27920483, 0.26909579, 0.22966473],
       [0.33592059, 0.32442553, 0.28106323],
       [0.34594089, 0.33427331, 0.2906474],
       [0.35312213, 0.34135106, 0.29765486]]

mean_dispersed = [[0.1485085, 0.07972562, 0.07972562],
        [0.1485085, 0.07972562, 0.07972562],
        [0.10530034,0.09904735, 0.06715711],
        [0.1723193, 0.16208656, 0.1098996 ],
        [0.19028167,0.1793008,  0.12116231],
        [0.18749268,0.17634825, 0.11966386]]
std_dispersed = [[0.34127658, 0.27029246, 0.27029246],
       [0.34127658, 0.27029246, 0.27029246],
       [0.28040959, 0.27026595, 0.23072036],
       [0.34223538, 0.33062806, 0.28707876],
       [0.35507738, 0.34346676, 0.29920025],
       [0.35292448, 0.34116759, 0.29759443]]

mean = [[0.1617112, 0.14061562, 0.10040056]]
std = [[0.33757988, 0.31674016, 0.27994369]]

def train_model(model, criterion, optimizer, scheduler, device, dataloaders, dataset_sizes, num_epochs=25):
    since = time.time()

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    losses = []
    accuracies = []

    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                # scheduler.step()
                model.train()  # Set model to training mode
            else:
                model.eval()  # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                phase, epoch_loss, epoch_acc))

            # deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())

            if phase == 'train':
                losses.append(epoch_loss)
                accuracies.append(epoch_acc)

        print()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model, losses, accuracies


def visualize_model(model, device, dataloaders, class_names, stageMean, stageStd, num_images=6):
    was_training = model.training
    model.eval()
    images_so_far = 0
    fig = plt.figure()

    with torch.no_grad():
        for i, (inputs, labels) in enumerate(dataloaders['val']):
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)

            for j in range(inputs.size()[0]):
                images_so_far += 1
                ax = plt.subplot(num_images // 2, 2, images_so_far)
                ax.axis('off')
                ax.set_title('predicted: {}'.format(class_names[preds[j]]))
                imshow(inputs.cpu().data[j], stageMean, stageStd, )

                if images_so_far == num_images:
                    model.train(mode=was_training)
                    return
        model.train(mode=was_training)


def imshow(inp, stageMean, stageStd, title=None):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    inp = stageStd * inp + stageMean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated


def main():
    # plt.ion()  # interactive mode

    device = 'cpu'  # torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    #alexnet = torch.load("./alexnetModel2.pt", map_location=torch.device('cpu'))

    alexnet = models.alexnet(pretrained=True)
    for param in alexnet.parameters():
        param.requires_grad = True

    # in_ftrs = alexnet.classifier[1].out_features
    # out_ftrs = alexnet.classifier[6].in_features
    # alexnet.classifier[4] = nn.Linear(in_ftrs, out_ftrs)
    # for param in alexnet.classifier[4].parameters():
    #    param.requires_grad = True

    in_ftrs = alexnet.classifier[4].out_features
    alexnet.classifier[6] = nn.Linear(in_ftrs, 2)
    for param in alexnet.classifier[6].parameters():
        param.requires_grad = True

    # for idx, m in enumerate(alexnet.classifier.modules()):
    #     print(idx, '->', m)

    alexnet = alexnet.to(device)

    criterion = nn.CrossEntropyLoss()
    # optimizer_ft = optim.SGD(alexnet.parameters(), lr=0.001, momentum=0.9)
    #optimizer_ft = optim.Adam(alexnet.parameters(), lr=0.00004)
    optimizer_ft = optim.Adam(alexnet.parameters(), lr=0.00004)
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=8, gamma=0.3)

    epocs = 10
    for stage in [1]:
        print("Stage - ", stage)
        data_dir = './DataSet/Stage2' #+ str(stage)

        data_transforms = {
            'train': transforms.Compose([
                transforms.Resize(224),
                transforms.ToTensor(),
                transforms.Normalize(np.array(mean[stage - 1]), np.array(std[stage - 1]))
            ]),
            'val': transforms.Compose([
                transforms.Resize(224),
                transforms.ToTensor(),
                transforms.Normalize(np.array(mean[stage - 1]), np.array(std[stage - 1]))
            ]),
        }

        image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in
                          ['train', 'val']}
        dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=5, shuffle=True, num_workers=4)
                       for x in ['train', 'val']}
        dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}

        alexnet, loss, acc = train_model(alexnet, criterion, optimizer_ft, exp_lr_scheduler, device, dataloaders,
                                         dataset_sizes, num_epochs=epocs)

        torch.save(alexnet, "./model" + str(stage) + ".pt")

        p = range(epocs)
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.set_title('Accuracy per epoc stage ' + str(stage))
        ax.set_xlabel('Epocs')
        ax.plot(p, acc, c='b')
        ax1 = ax.twinx()
        ax1.plot(p, loss, c='tab:orange')
        ax.grid(axis='both', alpha=0.5, linestyle='--', linewidth=1)
        plt.show()

    class_names = image_datasets['train'].classes
    inputs, classes = next(iter(dataloaders['train']))
    out = torchvision.utils.make_grid(inputs)
    imshow(out, np.array(mean[stage - 1]), np.array(std[stage - 1]), title=[class_names[x] for x in classes])
    visualize_model(alexnet, device, dataloaders, class_names, np.array(mean[stage - 1]), np.array(std[stage - 1]))

    # plt.ioff()
    plt.show()


if __name__ == '__main__':
    main()
