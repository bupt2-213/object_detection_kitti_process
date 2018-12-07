# change test datasets images from png to jpg
import os
import glob
import cv2

test_img_dir = '/media/yangshun/0008EB70000B0B9F/Datasets/KITTI/data_object_image_2/KITTI/testing/image_2'
save_dir = '/media/yangshun/0008EB70000B0B9F/Datasets/KITTI/data_object_image_2/KITTI/testing/image_2_jpg'

if not os.path.exists(save_dir):
    os.mkdir(save_dir)
else:
    print(' save dir exists')
    # exit()

imgs = glob.glob(os.path.join(test_img_dir, '*'))
imgs = sorted(imgs)


for img in imgs:
    im = cv2.imread(img)
    name = os.path.split(img)[1].split('.')[0]
    save_path = os.path.join(save_dir, '{}.jpg'.format(name))
    print(save_path)
    cv2.imwrite(save_path, im)
