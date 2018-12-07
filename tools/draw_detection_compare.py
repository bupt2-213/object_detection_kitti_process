import cv2
import glob
import os
import numpy as np

COLORS = {'Car': (255, 0, 255),
          'Pedestrian': (0, 255, 255),
          'Cyclist': (255, 255, 0)}

# kitti_test_img_dir = '/media/yangshun/0008EB70000B0B9F/Datasets/KITTI/data_object_image_2/KITTI/testing/image_2'
# kitti_test_txt_dir = '/home/yangshun/PycharmProjects/roi_roi/output/roi_roi_val_txt_all345/data'

kitti_test_img_dir = '/media/yangshun/0008EB70000B0B9F/Datasets/KITTI/data_object_image_2/KITTI/training/image_2'
test_txt = '/media/yangshun/0008EB70000B0B9F/PycharmProjects/roi_roi/data/KITTIVOC/ImageSets/Main/test.txt'
with open(test_txt, 'rb') as f:
    lines = f.readlines()
test_imgs = [os.path.join(kitti_test_img_dir, '{}.png'.format(line.strip())) for line in lines]
kitti_test_txt_dir = '/media/yangshun/0008EB70000B0B9F/roi_roi/txt_result/new/fpn_fuse_phase_concat/data'
kitti_test_txt_dir1 = '/media/yangshun/0008EB70000B0B9F/roi_roi/txt_result/new/fpn_fuse_phase_concat300/data'
# test_imgs = glob.glob(os.path.join(kitti_test_img_dir, '*'))
# test_imgs = sorted(test_imgs)
test_txts = glob.glob(os.path.join(kitti_test_txt_dir, '*'))
test_txts = sorted(test_txts)

test_txts1 = glob.glob(os.path.join(kitti_test_txt_dir1, '*'))
test_txts1 = sorted(test_txts1)


def draw(txt_file, im):
    with open(txt_file, 'rb') as f:
        lines = f.readlines()
    for line in lines:
        lists = line.strip().split(' ')
        cls = lists[0]
        x1 = int(float(lists[4]))
        y1 = int(float(lists[5]))
        x2 = int(float(lists[6]))
        y2 = int(float(lists[7]))
        score = float(lists[-1])
        if score > 0.7:
            cv2.rectangle(im, (x1, y1), (x2, y2), COLORS[cls], 2)
            text = str(cls) + ": " + str(format(score * 100, '.2f'))
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(im, text, (x1, y1-3), font, .4, COLORS[cls], 1)
    return im

m = 0

for i in range(len(test_imgs)):
    im = cv2.imread(test_imgs[i])
    im1 = np.copy(im)
    im2 = np.copy(im)
    im3 = np.copy(im)

    im = draw(test_txts[i], im)
    cv2.imshow('fpn', im)

    im3 = draw(test_txts1[i], im3)
    cv2.imshow('fpn_fuse', im3)

    if cv2.waitKey(0) & 0xFF == ord('q'):  # press q to quit
        break
    # elif cv2.waitKey(0) & 0xFF == ord('s'):
    #     cv2.imwrite('/home/yangshun/PycharmProjects/KITTI_progress/data/imgs/{}.png'.format(m), im)
    #     cv2.imwrite('/home/yangshun/PycharmProjects/KITTI_progress/data/imgs/{}.png'.format(m+1), im3)
    #     m = m + 2
    #     continue
    else:
        continue
cv2.destroyAllWindows()
