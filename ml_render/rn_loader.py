import numpy as np
import os
from skimage import io, transform
import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils


class RenderNetDataset(Dataset):
    def __init__(self, csv_file, root_dir, transform=None):
        self.scene_matrix = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.scene_matrix) - 1

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = os.path.join(self.root_dir, "render%05d" % idx + ".png")
        image = io.imread(img_name)
        image = np.delete(image, (3), axis=2)
        #print(img_name)
        #print(image.shape)

        scene_vec = self.scene_matrix.loc[idx].to_numpy()
        
        if self.transform:
            #print(image)
            image = self.transform(image)

        return { 'image': image, 'scene': scene_vec}

"""

rnet_dataset = RenderNetDataset(csv_file='data/labels.csv', root_dir='data/judkins_box')

for i in range(len(rnet_dataset)):
    sample = rnet_dataset[i]
"""
