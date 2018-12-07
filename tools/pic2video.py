# encoding: UTF-8
import glob as glob
import cv2
import os
from tqdm import tqdm


def change_name():
    base_path = '/media/yangshun/0008EB70000B0B9F/IMG_9037/'
    images = os.listdir(base_path)

    images_new = [base_path + image.split('_')[0] + '_' + image.split('_')[1].zfill(7) for image in images]
    images = [base_path + image for image in images]

    for i in tqdm(range(len(images))):
        os.rename(images[i], images_new[i])

img_path = glob.glob("/media/yangshun/0008EB70000B0B9F/IMG_9037/*")
img_path = sorted(img_path)
# print(img_path)
videoWriter = cv2.VideoWriter('testperson.avi', cv2.VideoWriter_fourcc(*'MJPG'), 20, (640, 480))  # w, h

for path in tqdm(img_path):
    img = cv2.imread(path)
    img = cv2.resize(img, (640, 480))
    videoWriter.write(img)
videoWriter.release()





