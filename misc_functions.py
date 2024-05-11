"""
Created on Thu Oct 21 11:09:09 2017

@author: Utku Ozbulak - github.com/utkuozbulak
"""
import os
import copy
import numpy as np
from PIL import Image
import matplotlib.cm as mpl_color_map

import torch
from torchvision import models

mean = [0.19887728, 0.18706746, 0.12683741]
std = [0.36040904, 0.34855344, 0.3049059]
# mean = [0.485, 0.456, 0.406]
# std = [0.229, 0.224, 0.225]
out_dir = './test'

def convert_to_grayscale(im_as_arr):
    """
        Converts 3d image to grayscale

    Args:
        im_as_arr (numpy arr): RGB image with shape (D,W,H)

    returns:
        grayscale_im (numpy_arr): Grayscale image with shape (1,W,D)
    """
    grayscale_im = np.zeros((len(im_as_arr), 1, im_as_arr.shape[2], im_as_arr.shape[3]))
    for i in range(len(im_as_arr)):
        grayscale_im[i][0] = np.sum(np.abs(im_as_arr[i]), axis=0)
        im_max = np.percentile(grayscale_im[i][0], 99)
        im_min = np.min(grayscale_im[i][0])
        grayscale_im[i][0] = (np.clip((grayscale_im[i][0] - im_min) / (im_max - im_min), 0, 1))
        #grayscale_im[i] = np.expand_dims(grayscale_im[i][0], axis=0)
    return grayscale_im


def save_gradient_images(im_as_arr, file_name, suff):
    """
        Exports the original gradient image

    Args:
        gradient (np arr): Numpy array of the gradient with shape (3, 224, 224)
        file_name (str): File name to be exported
    """
    gradient = np.copy(im_as_arr)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    # Save image
    for i in range(len(gradient)):
        # Normalize
        gradient[i] = gradient[i] - gradient[i].min()
        gradient[i] /= gradient[i].max()
        path_to_file = os.path.join(out_dir, file_name[i]+suff + '.jpg')
        save_image(gradient[i], path_to_file)


def save_class_activation_images(org_img, activation_map, file_name, all = True):
    """
        Saves cam activation map and activation map on the original image

    Args:
        org_img (PIL img): Original image
        activation_map (numpy arr): Activation map (grayscale) 0-255
        file_name (str): File name of the exported image
    """
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    # Grayscale activation map
    heatmap, heatmap_on_image = apply_colormap_on_image(org_img, activation_map, 'hsv')
    for i in range(len(org_img)):
        # Save colored heatmap
        path_to_file = os.path.join(out_dir, file_name[i]+'_Cam_Heatmap.png')
        save_image(heatmap[i], path_to_file)
        # Save heatmap on iamge
        path_to_file = os.path.join(out_dir, file_name[i]+'_Cam_On_Image.png')
        save_image(heatmap_on_image[i], path_to_file)
        # SAve grayscale heatmap
        if (all):
            path_to_file = os.path.join(out_dir, file_name[i]+'_Cam_Grayscale.png')
            save_image(activation_map[i], path_to_file)


def apply_colormap_on_image(org_im, activation, colormap_name):
    """
        Apply heatmap on image
    Args:
        org_img (PIL img): Original image
        activation_map (numpy arr): Activation map (grayscale) 0-255
        colormap_name (str): Name of the colormap
    """
    # Get colormap
    color_map = mpl_color_map.get_cmap(colormap_name)
    cmapImage = color_map(activation.astype(np.uint8))
    # Change alpha channel in colormap to make sure original image is displayed
    heatmap = copy.copy(cmapImage)
    heatmap[:, :, :, 3] = 0.4
    heatmap_on_image = []
    no_trans_heatmap  = []
    for i in range(len(heatmap)):
        heatmapImg = Image.fromarray((heatmap[i]*255).astype(np.uint8))
        no_trans_heatmap.append(Image.fromarray((cmapImage[i]*255).astype(np.uint8)))

        # Apply heatmap on iamge
        tmp = Image.new("RGBA", org_im[i].size)
        tmp = Image.alpha_composite(tmp, org_im[i].convert('RGBA'))
        tmp = Image.alpha_composite(tmp, heatmapImg)
        heatmap_on_image.append(tmp)
    return no_trans_heatmap, heatmap_on_image


def save_image(im, path):
    """
        Saves a numpy matrix of shape D(1 or 3) x W x H as an image
    Args:
        im_as_arr (Numpy array): Matrix of shape DxWxH
        path (str): Path to the image
    """
    if isinstance(im, np.ndarray):
        if len(im.shape) == 2:
            im = np.expand_dims(im, axis=0)
        if im.shape[0] == 1:
            # Converting an image with depth = 1 to depth = 3, repeating the same values
            # For some reason PIL complains when I want to save channel image as jpg without
            # additional format in the .save()
            im = np.repeat(im, 3, axis=0)
            # Convert to values to range 1-255 and W,H, D
        if im.shape[0] == 3:
            im = im.transpose(1, 2, 0) * 255
        im = Image.fromarray(im.astype(np.uint8))
    im.save(path)


def preprocess_image(pil_im, resize_im=True):
    """
        Processes image for CNNs

    Args:
        PIL_img (PIL_img): Image to process
        resize_im (bool): Resize to 224 or not
    returns:
        im_as_var (torch variable): Variable that contains processed float tensor
    """
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
    # Convert to Pytorch variable
    im_as_var = im_as_ten
    im_as_ten.requires_grad = True
    return im_as_var


def recreate_image(im_as_var):
    """
        Recreates images from a torch variable, sort of reverse preprocessing
    Args:
        im_as_var (torch variable): Image to recreate
    returns:
        recreated_im (numpy arr): Recreated image in array
    """

    recreated_im = copy.copy(im_as_var.data.numpy()[0])
    for c in range(3):
        recreated_im[c] *= std[c]
        recreated_im[c] += mean[c]
    recreated_im[recreated_im > 1] = 1
    recreated_im[recreated_im < 0] = 0
    recreated_im = np.round(recreated_im * 255)

    recreated_im = np.uint8(recreated_im).transpose(1, 2, 0)
    return recreated_im


def get_positive_negative_saliency(gradient):
    """
        Generates positive and negative saliency maps based on the gradient
    Args:
        gradient (numpy arr): Gradient of the operation to visualize

    returns:
        pos_saliency ( )
    """
    pos_saliency = (np.maximum(0, gradient))
    neg_saliency = (np.maximum(0, -gradient))
    return pos_saliency, neg_saliency


def get_example_params():
    """
        Gets used variables for almost all visualizations, like the image, model etc.

    Args:
        example_index (int): Image id to use from examples

    returns:
        original_image (numpy arr): Original image read from the file
        prep_img (numpy_arr): Processed image
        target_class (int): Target class for the image
        file_name_to_export (string): File name to export the visualizations
        pretrained_model(Pytorch model): Model to use for the operations
    """
    # Pick one of the examples
    # 56
    example_list = np.array([['s0d.png', 0],['s1d.png', 1],
                    ['s2d.png', 0],
                    ['s3d.png', 0]])
    target_class = example_list[:, 1]
    file_name_to_export = example_list[:, 0]
    # Read image
    original_image = []
    for i in range(len(example_list)):
        original_image.append(Image.open(example_list[i,0]).convert('RGB'))
        file_name_to_export[i] = file_name_to_export[i][file_name_to_export[i].rfind('/')+1:file_name_to_export[i].rfind('.')]
    # Define model
    prep_img = torch.cat([preprocess_image(original_image[i]) for i in range(len(example_list))], dim=0)
    target_class = torch.LongTensor(example_list[:, 1].astype(np.uint8))
    #pretrained_model = models.alexnet(pretrained=True)
    pretrained_model = torch.load("./alexnetModelSingleDispersed6.pt", map_location=torch.device('cpu'))
    return (original_image,
            prep_img,
            target_class,
            file_name_to_export,
            pretrained_model)


def get_example_params2(example_list, model_name):
    original_image = []
    for i in range(len(example_list)):
        original_image.append(Image.open(example_list[i]).convert('RGB'))
        example_list[i] = example_list[i][example_list[i].rfind('/')+1:example_list[i].rfind('.')]
    prep_img = torch.cat([preprocess_image(original_image[i]) for i in range(len(example_list))], dim=0)
    pretrained_model = torch.load(model_name, map_location=torch.device('cpu'))
    return (original_image, prep_img, example_list, pretrained_model)
