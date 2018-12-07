import cv2
import os
import glob

COLORS = {'Car': (255, 0, 255),
          'Pedestrian': (0, 255, 255),
          'Cyclist': (255, 255, 0)}


def validation(img_path, test_txt, detection_path, win_name):
    with open(test_txt, 'r') as f:
        lines = f.readlines()
        for line in lines:
            img = os.path.join(img_path, '{}.jpg'.format(line.strip()))
            im = cv2.imread(img)
            det = os.path.join(detection_path, '{}.txt'.format(line.strip()))
            if os.path.exists(det):
                with open(det, 'r') as fd:
                    dlines = fd.readlines()
                    cls_list = []
                    for dline in dlines:
                        str_line = dline.strip().split(' ')
                        cls, x1, y1, x2, y2 = str_line[0], str_line[4], str_line[5], str_line[6], str_line[7]
                        cls_list.append(cls)
                        x1 = int(float(x1))
                        x2 = int(float(x2))
                        y1 = int(float(y1))
                        y2 = int(float(y2))
                        # print(x1, y1, x2, y2)
                        cv2.rectangle(im, (x1, y1), (x2, y2), COLORS[cls], 2)
                        cv2.putText(im, cls, (x1 + 2, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLORS[cls])
            # print(cls_list)
            # if 'Cyclist' not in cls_list:
            #     continue
            cv2.imshow(win_name, im)
            key = cv2.waitKey() & 0xff
            if key == ord('q'):
                break


# for validation
img_path = '/media/yangshun/0008EB70000B0B9F/PycharmProjects/roi_roi/data/KITTIVOC/JPEGImages'
test_txt = '/media/yangshun/0008EB70000B0B9F/PycharmProjects/roi_roi/data/KITTIVOC/ImageSets/Main/test.txt'
detection_path = '/media/yangshun/0008EB70000B0B9F/roi_roi/txt_result/new/fpn_fuse_phase_conelt320/data'
rf_detection_path = '/media/yangshun/0008EB70000B0B9F/roi_roi/txt_result/new/fpn/data'


validation(img_path, test_txt, detection_path, '0')


def testing(img_path, detection_path):
    imgs = glob.glob(os.path.join(img_path, '*'))
    imgs = sorted(imgs)
    for img in imgs:
        im = cv2.imread(img)
        det = os.path.join(detection_path, '{}.txt'.format(os.path.split(img)[1].split('.')[0]))
        if os.path.exists(det):
            with open(det, 'r') as fd:
                dlines = fd.readlines()
                for dline in dlines:
                    str_line = dline.strip().split(' ')
                    cls, x1, y1, x2, y2 = str_line[0], str_line[4], str_line[5], str_line[6], str_line[7]
                    x1 = int(float(x1))
                    x2 = int(float(x2))
                    y1 = int(float(y1))
                    y2 = int(float(y2))
                    # print(x1, y1, x2, y2)
                    cv2.rectangle(im, (x1, y1), (x2, y2), (255, 0, 255), 1)
                    cv2.putText(im, cls, (x1 + 2, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 255))
        cv2.imshow('0', im)
        key = cv2.waitKey() & 0xff
        if key == ord('q'):
            break

# for testing
# img_path = '/media/yangshun/0008EB70000B0B9F/Datasets/KITTI/data_object_image_2/KITTI/testing/image_2'
# detection_path = '/home/yangshun/PycharmProjects/roi_roi/txt_result/fpnc_context_test/data'
#
# testing(img_path, detection_path)

