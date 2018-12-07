import os
import glob
from tqdm import tqdm


def change_name():
    base_path = '/media/yangshun/0008EB70000B0B9F/IMG_9037/'
    images = os.listdir(base_path)

    images_new = [base_path + image.split('_')[0] + '_' + image.split('_')[1].zfill(7) for image in images]
    images = [base_path + image for image in images]

    for i in tqdm(range(len(images))):
        os.rename(images[i], images_new[i])

file_path = '/media/yangshun/0008EB70000B0B9F/roi_roi/txt_result/new/fpnc_softnms'

files = glob.glob(os.path.join(file_path, '*'))
files = sorted(files)

for file in tqdm(files):
    if os.path.isdir(file):
        continue
    newname = file[-10:]
    print(newname)
    os.rename(file, os.path.join(file_path, newname))