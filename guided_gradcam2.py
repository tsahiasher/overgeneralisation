"""
Created on Thu Oct 23 11:27:15 2017

@author: Utku Ozbulak - github.com/utkuozbulak
"""
import glob
import numpy as np

from misc_functions import (get_example_params2,
                            convert_to_grayscale,
                            save_gradient_images,
                            save_class_activation_images)
from gradcam import GradCam
from guided_backprop import GuidedBackprop


def guided_grad_cam(grad_cam_mask, guided_backprop_mask):
    """
        Guided grad cam is just pointwise multiplication of cam mask and
        guided backprop mask

    Args:
        grad_cam_mask (np_arr): Class activation map mask
        guided_backprop_mask (np_arr):Guided backprop mask
    """
    cam_gb = np.zeros(guided_backprop_mask.shape, dtype=np.float32)
    for i in range(guided_backprop_mask.shape[0]):
        cam_gb[i] = np.multiply(grad_cam_mask[i], guided_backprop_mask[i])
    return cam_gb


if __name__ == '__main__':
    # Get params
    model_name = "./ordered models/alexnetModel2_6_3.pt"
    example_list = ["test/s2.png", "test/s2A.png"]
    #example_list = ['s3d.png', 'square.png', 'star.png', 'random.png', '14.png', '15.png', '16.png']
    '''example_list = []
    for img in glob.glob('test/*.*'):
        example_list.append(img)'''
    (original_image, prep_img, file_name_to_export, pretrained_model) = get_example_params2(example_list, model_name)
    # Grad cam
    gcv2 = GradCam(pretrained_model, target_layer=11)
    target_class, outputs = gcv2.get_classes(prep_img)
    print(example_list, model_name)
    print(target_class, outputs)
    #exit(0)
    # Generate cam mask
    cam = gcv2.generate_cam(prep_img, target_class)
    print('Grad cam completed')

    # Guided backprop
    GBP = GuidedBackprop(pretrained_model)
    # Get gradients
    guided_grads = GBP.generate_gradients(prep_img, target_class)
    print('Guided backpropagation completed')

    # Guided Grad cam
    save_class_activation_images(original_image, cam, file_name_to_export, True)
    cam_gb = guided_grad_cam(cam, guided_grads)
    grayscale_cam_gb = convert_to_grayscale(cam_gb)
    save_gradient_images(grayscale_cam_gb, file_name_to_export, '_GGrad_Cam_gray')
    print('Guided grad cam completed')
