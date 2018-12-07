# convert from voc dataset to coco dataset format

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import sys
import argparse
import numpy as np
import json
import xml.etree.ElementTree as ET
import itertools
import pprint
import logging

id = 0

# CLASSES = [
#         '__background__',
#         'aeroplane', 'bicycle', 'bird', 'boat',
#         'bottle', 'bus', 'car', 'cat', 'chair',
#         'cow', 'diningtable', 'dog', 'horse',
#         'motorbike', 'person', 'pottedplant',
#         'sheep', 'sofa', 'train', 'tvmonitor'
#     ]

CLASSES = ['__background__', 'car']


def parse_args():
    """Parse input arguments."""
    # example to use: voc2coco.py --voc /path/to/VOC2007 --out /path/to/json_save_path
    #
    # the dir tree of VOC2007 shows as follow:
    # |-VOC2007
    #   |--Annotations
    #      |---000001.xml
    #      |--- ....
    #   |--ImageSets
    #      |---Layout  (do not care this folder)
    #      |---Main
    #         |----train.txt
    #         |----val.txt
    #         |----trainval.txt
    #         |----test.txt
    #      |---Segmentation (do not care this folder)
    #   |--JPEGImages  (do not care this folder)
    #   |--SegmentationClass  (do not care this folder)
    #   |--SegmentationObject  (do not care this folder)

    # If files in Main exist, correspond json file will generate,
    # else nothing will generate.

    parser = argparse.ArgumentParser(description='Convert VOC dataset to Pascal voc format')
    parser.add_argument('--voc', dest='voc',
                        help='path to voc root',
                        default='./data/VOC2007', type=str)
    parser.add_argument('--out', dest='out_dir',
                        help='json save path',
                        default='./data', type=str)
    # parser.add_argument('--mode', dest='mode',
    #                     help='list of train, val, trainval, and test',
    #                     default=0, type=str)
    if len(sys.argv) == 1:
        parser.print_help()
        # sys.exit(1)
    args = parser.parse_args()
    return args


def xywh_to_xyxy(xywh):
    """Convert [x1 y1 w h] box format to [x1 y1 x2 y2] format."""
    if isinstance(xywh, (list, tuple)):
        # Single box given as a list of coordinates
        assert len(xywh) == 4
        x1, y1 = xywh[0], xywh[1]
        x2 = x1 + np.maximum(0., xywh[2] - 1.)
        y2 = y1 + np.maximum(0., xywh[3] - 1.)
        return x1, y1, x2, y2


def xyxy_to_xywh(xyxy):
    """Convert [x1 y1 x2 y2] box format to [x1 y1 w h] format."""
    if isinstance(xyxy, (list, tuple)):
        # Single box given as a list of coordinates
        assert len(xyxy) == 4
        x1, y1 = xyxy[0], xyxy[1]
        w = xyxy[2] - x1 + 1
        h = xyxy[3] - y1 + 1
        return [x1, y1, w, h]


def cls_to_index(cls, cls_list):
    """Return the index of correspond class name"""
    return cls_list.index(cls)


def get_segment(bbox):
    """Get the segmentation from bbox."""
    segmentation = []
    seg_2 = []
    x1 = bbox[0]
    y1 = bbox[1]
    x2 = bbox[2] + x1
    y2 = bbox[3] + y1
    c = itertools.product([x1, x2], [y1, y2])
    for i, tu in enumerate(c):
        if i == 2:
            seg_2 = list(tu)
            continue
        else:
            segmentation.append(list(tu))
    segmentation.append(seg_2)
    segmentation = np.reshape(segmentation, (1, -1)).tolist()
    return segmentation


def get_ann_dict(area, bbox, category_id, id, ignore, image_id, iscrowd, segmentation):
    """Get coco annotation format dict of one object """
    ann_dict = dict()
    ann_dict['area'] = area
    ann_dict['bbox'] = bbox
    ann_dict['category_id'] = category_id
    ann_dict['id'] = id
    ann_dict['ignore'] = ignore
    ann_dict['image_id'] = image_id
    ann_dict['iscrowd'] = iscrowd
    ann_dict['segmentation'] = segmentation
    return ann_dict


def get_image_dict(file_name, height, id, width):
    """Get coco images format dict of one object """
    images_dict = dict()
    images_dict['file_name'] = file_name
    images_dict['height'] = height
    images_dict['width'] = width
    images_dict['id'] = id
    return images_dict


def get_cate_list(class_list):
    """Get categories list"""
    cate_list = list()
    for index, cls in enumerate(class_list):
        cate_dict = dict()
        if cls == '__background__':
            continue
        cate_dict['id'] = index
        cate_dict['name'] = cls
        cate_dict['supercategory'] = 'none'
        cate_list.append(cate_dict)
    return cate_list


def parsexmlfiles(xml_file):
    global id
    if not xml_file.endswith('.xml'):
        print('{} should be xml file'.format(xml_file))

    tree = ET.ElementTree(file=xml_file)
    root = tree.getroot()
    if root.tag != 'annotation':
        raise Exception('pascal voc xml root element should be annotation, rather than {}'.format(root.tag))

    filename = root.findtext('filename')
    image_id = int(filename.split('.')[0])
    width = int(root.findtext('size/width'))
    height = int(root.findtext('size/height'))
    iscrowd = 0
    # print(filename, image_id, width, height, iscrowd)

    annotation = list()
    images_list = list()

    image_dict = get_image_dict(filename, height, image_id, width)
    images_list.append(image_dict)
    # pprint.pprint(images_list)

    for item in root.iterfind('object'):
        id = id + 1
        cls = item.findtext('name')
        category_id = cls_to_index(cls, CLASSES)
        ignore = 0  # int(item.findtext('difficult'))
        bbox = []
        bbox.append(int(item.findtext('bndbox/xmin')) - 1)  # x1
        bbox.append(int(item.findtext('bndbox/ymin')) - 1)  # y1
        bbox.append(int(item.findtext('bndbox/xmax')) - 1)  # x2
        bbox.append(int(item.findtext('bndbox/ymax')) - 1)  # y2

        bbox = xyxy_to_xywh(bbox)
        area = bbox[2] * bbox[3]
        segmentation = get_segment(bbox)
        # print(ignore, cls, category_id, bbox, area, segmentation)

        ann_dict_one_obj = get_ann_dict(area, bbox, category_id, id, ignore, image_id, iscrowd, segmentation)
        annotation.append(ann_dict_one_obj)

    # pprint.pprint(annotation)
    return images_list, annotation


def generate_json(xml_files, save_name):
    images = list()
    annotations = list()
    for file in xml_files:
        if not os.path.exists(file):
            logging.info('{} does not exist!'.format(file))
        images_list, annotations_list = parsexmlfiles(file)
        images.extend(images_list)
        annotations.extend(annotations_list)
    categories = get_cate_list(CLASSES)
    type = 'instances'
    json_dict = dict()
    json_dict['annotations'] = annotations
    json_dict['categories'] = categories
    json_dict['images'] = images
    json_dict['type'] = type
    # pprint.pprint(json_dict)
    with open(save_name, 'w') as f:
        json.dump(json_dict, f, separators=(',', ':'))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')
    args = parse_args()

    _voc_dir = args.voc
    _output_dir = args.out_dir
    # _mode = args.mode
    # assert _mode in [0, 1, 2, 3]

    annotations_path = os.path.join(_voc_dir, 'Annotations')
    if not os.path.exists(annotations_path):
        raise Exception('{} is not exist!'.format(annotations_path))

    txt_path = os.path.join(_voc_dir, 'ImageSets', 'Main')
    if not os.path.exists(txt_path):
        raise Exception('{} is not exist!'.format(txt_path))

    train_txt = os.path.join(txt_path, 'train.txt')
    val_txt = os.path.join(txt_path, 'val.txt')
    trainval_txt = os.path.join(txt_path, 'trainval.txt')
    test_txt = os.path.join(txt_path, 'test.txt')

    txt_file = [train_txt, val_txt, trainval_txt, test_txt]

    for i in range(len(txt_file)):
        if not os.path.exists(txt_file[i]):
            logging.info('{} does not exist!'.format(txt_file[i]))
            logging.info('{} will not be generated!\n'.format(os.path.split(txt_file[i])[-1].split('.')[0]))
        else:
            logging.info('generate {} ......'.format('{}.json'.format(os.path.split(txt_file[i])[-1].split('.')[0])))
            with open(txt_file[i], 'r') as f:
                lines = f.readlines()
            xml_list = [os.path.join(annotations_path, '{}.xml'.format(line.strip())) for line in lines]
            # pprint.pprint(xml_list)
            if not os.path.exists(_output_dir):
                os.makedirs(_output_dir)
            save_path = os.path.join(_output_dir, '{}.json'.format(os.path.split(txt_file[i])[-1].split('.')[0]))
            generate_json(xml_list, save_path)
            logging.info('done!')





