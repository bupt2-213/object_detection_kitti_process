# Visual detection result on KITTI dataset

import os
import cv2
import glob


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
            cv2.rectangle(im, (x1, y1), (x2, y2), (0, 255, 0), 2)
            text = str(cls) + ": " + str(format(score*100, '.2f'))
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(im, text, (x1, y1), font, .4, (0, 0, 255), 1)
    return im


RESULT_DIR = '/media/yangshun/0008EB70000B0B9F/ROI_ROI_RESULT/debug/'

methods = [s for s in os.listdir(RESULT_DIR)]
paths = [RESULT_DIR + s + '/data' for s in methods]

img_path = '/media/yangshun/0008EB70000B0B9F/PycharmProjects/roi_roi/data/KITTIVOC/JPEGImages'
test_txt = '/media/yangshun/0008EB70000B0B9F/PycharmProjects/faster_rcnn/data/KITTIVOC/ImageSets/Main/test.txt'

with open(test_txt, 'rb') as f:
    lines = map(str.strip, f.readlines())

for line in lines:
    print(line)
    img = os.path.join(img_path, line+'.jpg')
    im = cv2.imread(img)
    for path in paths:
        name = path.split('/')[-2]
        txt = os.path.join(path, line+'.txt')
        cv2.namedWindow(name)
        im_copy = im.copy()
        im_copy = draw(txt, im_copy)
        cv2.imshow(name, im_copy)
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        break
cv2.destroyAllWindows()

