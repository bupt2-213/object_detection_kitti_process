# use all training dataset for train

import os
import shutil


def write_file(train_txt, test_txt, new_train_txt, new_test_txt):
    with open(train_txt, 'rb') as f:
        lines_train = f.readlines()
    with open(test_txt, 'rb') as f:
        lines_test = f.readlines()
    new_lines = lines_train + lines_test
    new_lines = sorted(new_lines)

    with open(new_train_txt, 'w') as f:
        f.writelines(new_lines)
    with open(new_test_txt, 'w') as f:
        f.writelines(' ')

voc_path = '/media/yangshun/0008EB70000B0B9F/Datasets/KITTI/KITTIVOC/ImageSets/Main/'
save_path = os.path.join(voc_path, 'All')
if not os.path.exists(save_path):
    os.makedirs(save_path)

# these four lines don't need to change
train_file = 'train.txt'
test_file = 'test.txt'
car_train_file = 'car_train.txt'
car_test_file = 'car_test.txt'

train_txt = os.path.join(voc_path, train_file)
test_txt = os.path.join(voc_path, test_file)
new_train_txt = os.path.join(voc_path, 'All', train_file)
new_test_txt = os.path.join(voc_path, 'All', test_file)

write_file(train_txt, test_txt, new_train_txt, new_test_txt)
shutil.copyfile(new_train_txt, os.path.join(voc_path, 'All', 'val.txt'))
shutil.copyfile(new_train_txt, os.path.join(voc_path, 'All', 'trainval.txt'))

train_txt = os.path.join(voc_path, car_train_file)
test_txt = os.path.join(voc_path, car_test_file)
new_train_txt = os.path.join(voc_path, 'All', car_train_file)
new_test_txt = os.path.join(voc_path, 'All', car_test_file)

write_file(train_txt, test_txt, new_train_txt, new_test_txt)
shutil.copyfile(new_train_txt, os.path.join(voc_path, 'All', 'car_val.txt'))
shutil.copyfile(new_train_txt, os.path.join(voc_path, 'All', 'car_trainval.txt'))