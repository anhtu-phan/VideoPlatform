# Code for "ActionCLIP: ActionCLIP: A New Paradigm for Action Recognition"
# arXiv:
# Mengmeng Wang, Jiazheng Xing, Yong Liu

from datasets.transforms_ss import *
from randaugment import RandAugment

class GroupTransform(object):
    def __init__(self, transform):
        self.worker = transform

    def __call__(self, img_group):
        return [self.worker(img) for img in img_group]

def get_augmentation(training, config):
    # shanghaiTech
    #input_mean = [0.4762, 0.4815, 0.4770]
    #input_std = [0.1957, 0.1856, 0.1931]
    # UCFCrime
    
    input_mean = [0.485, 0.456, 0.406]
    input_std = [0.229, 0.224, 0.225]
    
    scale_size = config.data.input_size * 256 // 224
    if training:

        unique = torchvision.transforms.Compose([GroupMultiScaleCrop(config.data.input_size, [1, .875, .75, .66]),
                                                 GroupRandomHorizontalFlip(is_sth='some' in config.data.dataset),
                                                 GroupRandomColorJitter(p=0.8, brightness=0.4, contrast=0.4,
                                                                        saturation=0.2, hue=0.1),
                                                 GroupRandomGrayscale(p=0.2),
                                                 GroupGaussianBlur(p=0), 
                                                 GroupSolarization(p=0)] 
                                                )
    else:
        unique = torchvision.transforms.Compose([GroupScale(scale_size),
                                                 GroupCenterCrop(config.data.input_size)])

    common = torchvision.transforms.Compose([Stack(roll=False),
                                             ToTorchFormatTensor(div=True),
                                             GroupNormalize(input_mean,
                                                            input_std)])
    return torchvision.transforms.Compose([unique, common])

def randAugment(transform_train,config):
    print('Using RandAugment!')
    transform_train.transforms.insert(0, GroupTransform(RandAugment(config.data.randaug.N, config.data.randaug.M)))
    return transform_train

def get_inference_augmentation(config):
    # input_mean = [0.48145466, 0.4578275, 0.40821073]
    # input_std = [0.26862954, 0.26130258, 0.27577711]
    # UCFCrime
    input_mean = [0.485, 0.456, 0.406]
    input_std = [0.229, 0.224, 0.225]
    scale_size = config.data.input_size * 256 // 224
    unique = torchvision.transforms.Compose([GroupScale(scale_size),
                                                GroupCenterCrop(config.data.input_size)])

    common = torchvision.transforms.Compose([Stack(roll=False),
                                             ToTorchFormatTensor(div=True),
                                             GroupNormalize(input_mean,
                                                            input_std)])
    return torchvision.transforms.Compose([unique, common])