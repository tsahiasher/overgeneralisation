import torch
from torchvision import datasets, models, transforms
import torch.nn as nn

def test_model(model, criterion, device, iter_dataloaders, dataset_sizes):

    running_loss = 0.0
    running_corrects = 0
    counter=0

    # Iterate over data.
    for inputs, labels in iter_dataloaders:
        inputs = inputs.to(device)
        labels = labels.to(device)

        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)
        loss = criterion(outputs, labels)

        # statistics
        running_loss += loss.item() * inputs.size(0)
        running_corrects += torch.sum(preds == labels.data)
        counter += iter_dataloaders.batch_sampler.batch_size
        print('\r', counter, '/', iter_dataloaders.batch_sampler.sampler.num_samples, '    ', end='')

    loss = running_loss / dataset_sizes
    acc = running_corrects.double() / dataset_sizes

    print('Loss: {:.4f} Acc: {:.4f}'.format(loss, acc))

    print()


def main():
    device = 'cpu' # torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    alexnet = torch.load("./ordered models/alexnetModel2_6_3.pt", map_location=torch.device('cpu'))
    alexnet = alexnet.to(device)
    alexnet.eval()
    criterion = nn.CrossEntropyLoss()

    data_transforms = transforms.Compose([
            transforms.Resize(224),
            transforms.ToTensor(),
            transforms.Normalize([0.16401494, 0.15427534, 0.10460336],[0.33592059, 0.32442553, 0.28106323])
        ])

    #for i, stage in enumerate(["Stage8.1", "Stage8.2", "Stage8.3", "Stage8.4", "Stage8.5", "Stage8.6"]):
    for i, stage in enumerate(["Stage1"]):
        print(stage)
        data_dir = './DataSet-ordered-most/' + str(stage)+'/train'
        image_datasets = datasets.ImageFolder(data_dir, data_transforms)
        dataloaders = torch.utils.data.DataLoader(image_datasets, batch_size=1, shuffle=True, num_workers=4)
        iter_dataloaders = iter(dataloaders)
        dataset_sizes = len(image_datasets)
        test_model(alexnet, criterion, device, iter_dataloaders, dataset_sizes)


if __name__ == '__main__':
    main()
