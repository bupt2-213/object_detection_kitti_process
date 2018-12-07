# extract car, van, truck and convert to car label, keep dontcare

import os
import glob
from tqdm import tqdm

kitti_path = '/media/yangshun/0008EB70000B0B9F/Datasets/KITTI/data_object_image_2/KITTI'
labels_path = os.path.join(kitti_path, 'training/label_2')
save_path = os.path.join(kitti_path, 'training/label_2_car_new')

if not os.path.exists(save_path):
    os.makedirs(save_path)

labels = glob.glob(os.path.join(labels_path, '*'))
labels = sorted(labels)

for label in tqdm(labels):
    name = os.path.split(label)[1].split('.')[0]
    with open(label, 'rb') as f:
        lines = f.readlines()
    save_file = os.path.join(save_path, '{}.txt'.format(name))
    with open(save_file, 'wb') as ff:
        flag = False
        for line in lines:
            strs = line.split(' ')
            if strs[0] in ['Car', 'Van', 'Truck']:
                flag = True
                strs[0] = 'Car'
                new_label = ' '.join(strs)
                ff.writelines(new_label)
            if strs[0] == 'DontCare' and flag is True:
                new_label = ' '.join(strs)
                ff.writelines(new_label)
    if flag is not True:
        os.remove(save_file)

