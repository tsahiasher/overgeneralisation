import torch
import numpy as np
from torchvision import models
import torch.nn as nn
import matplotlib.pyplot as plt
from torchvision.utils import make_grid
from PIL import Image
from torch.nn import ReLU


def preprocess_image(pil_im, resize_im=True):

    mean = [0.18770611, 0.17655967, 0.11971281]
    std = [0.35312213, 0.34135106, 0.29765486]
    # Resize image
    if resize_im:
        pil_im.thumbnail((224, 224))
    im_as_arr = np.float32(pil_im)
    im_as_arr = im_as_arr.transpose(2, 0, 1)  # Convert array to D,W,H
    # Normalize the channels
    for channel, _ in enumerate(im_as_arr):
        im_as_arr[channel] /= 255
        im_as_arr[channel] -= mean[channel]
        im_as_arr[channel] /= std[channel]
    # Convert to float tensor
    im_as_ten = torch.from_numpy(im_as_arr).float()
    # Add one more channel to the beginning. Tensor shape = 1,3,224,224
    im_as_ten.unsqueeze_(0)
    im_as_ten.requires_grad = True
    return im_as_ten

class GuidedBackprop():
    """
       Produces gradients generated with guided back propagation from the given image
    """
    def __init__(self, model):
        self.model = model
        self.gradients = None
        self.forward_relu_outputs = []
        # Put model in evaluation mode
        self.model.eval()
        self.update_relus()
        self.hook_layers()

    def hook_layers(self):
        def hook_function(module, grad_in, grad_out):
            self.gradients = grad_in[0]
        # Register hook to the first layer
        first_layer = list(self.model.features._modules.items())[0][1]
        first_layer.register_backward_hook(hook_function)

    def update_relus(self):
        """
            Updates relu activation functions so that
                1- stores output in forward pass
                2- imputes zero for gradient values that are less than zero
        """
        def relu_backward_hook_function(module, grad_in, grad_out):
            """
            If there is a negative gradient, change it to zero
            """
            # Get last forward output
            corresponding_forward_output = self.forward_relu_outputs[-1]
            corresponding_forward_output[corresponding_forward_output > 0] = 1
            modified_grad_out = corresponding_forward_output * torch.clamp(grad_in[0], min=0.0)
            del self.forward_relu_outputs[-1]  # Remove last forward output
            return (modified_grad_out,)

        def relu_forward_hook_function(module, ten_in, ten_out):
            """
            Store results of forward pass
            """
            self.forward_relu_outputs.append(ten_out)

        # Loop through layers, hook up ReLUs
        for pos, module in self.model.features._modules.items():
            if isinstance(module, ReLU):
                module.register_backward_hook(relu_backward_hook_function)
                module.register_forward_hook(relu_forward_hook_function)

    def generate_gradients(self, input_image, target_class, cnn_layer, filter_pos):
        self.model.zero_grad()
        # Forward pass
        x = input_image
        for index, layer in enumerate(self.model.features):
            # Forward pass layer by layer
            # x is not used after this point because it is only needed to trigger
            # the forward hook function
            x = layer(x)
            # Only need to forward until the selected layer is reached
            if index == cnn_layer:
                # (forward hook function triggered)
                break
        conv_output = torch.sum(torch.abs(x[0, filter_pos]))
        # Backward pass
        conv_output.backward()
        # Convert Pytorch variable to numpy array
        # [0] to get rid of the first channel (1,3,224,224)
        gradients_as_arr = self.gradients.data.numpy()[0]
        return gradients_as_arr

def main():

    device = 'cpu' # torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    #myalexnet = torch.load("./FullalexnetModelSingle6.pt").to(device)
    alexnet = models.alexnet(pretrained=True).to(device)

    GBP = GuidedBackprop(alexnet)

    original_image = Image.open('s1.png').convert('RGB')
    prep_img = preprocess_image(original_image)

    for index, layer in enumerate(alexnet.features):
        if isinstance(layer, nn.Conv2d):
            guided_grads = np.zeros((layer.out_channels,3,224,224))
            for i in range(layer.out_channels):
                guided_grads[i] = GBP.generate_gradients(prep_img, 0, index, i)

            npimg = make_grid(torch.from_numpy(guided_grads), padding=3, nrow=int(np.sqrt(layer.out_channels)),
                              normalize=True, scale_each=True).detach().numpy()

            img = Image.fromarray((255.0*npimg.transpose((1,2,0))).astype(np.int8),"RGB")
            img.save('Alayer_' + str(index) + '.png')


    '''W2 = alexnet.features[3].weight.data.numpy()
    W2 = W2[0].reshape(64,1,5,5)
    npimg = make_grid(torch.from_numpy(W2), padding=3, nrow=8, normalize=True, scale_each=True).detach().numpy()
    plt.imshow(npimg[0,:,:], cmap='gray')
    plt.gca().axis('off')
    plt.show()'''

if __name__ == '__main__':
    main()
