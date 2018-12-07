# first we split training data to train.txt and test.txt, include car, cyclist, and pedestrian
# from origin label, only reverse car
import os
import shutil


def get_only_car_txt(source, dest, label):
    '''
    :param source: origin train txt file with name(000000~7480) in it, 
                which [name].txt include car,cyclist and pedestrian.
    :param dest: new train txt file with name in it, which [name].txt only include car.
    :param label: label list of all txt name only have car. 
    :return: 
    '''
    with open(source, 'rb') as f:
        lines = f.readlines()
    new_train = []
    for line in lines:
        if line.strip() in label:
            new_train.append(line)
    print('Origin length: ' + str(len(lines)))
    print('Length after check: ' + str(len(new_train)))

    with open(dest, 'wb') as f:
        f.writelines(new_train)


def main():
    label_car_dir = '/media/yangshun/0008EB70000B0B9F/Datasets/KITTI/data_object_image_2/KITTI/training/' \
                    'label_2_car_new'
    label_car = os.listdir(label_car_dir)
    label_car_name = [name.split('.')[0] for name in label_car]

    train_txt = 'data/ImageSets/train.txt'
    test_txt = 'data/ImageSets/val.txt'

    txt_save_path = 'data/ImageSets_car_new'
    if not os.path.exists(txt_save_path):
        os.mkdir(txt_save_path)
    else:
        shutil.rmtree(txt_save_path)

    new_train_txt = os.path.join(txt_save_path, 'train.txt')
    new_text_txt = os.path.join(txt_save_path, 'test.txt')

    get_only_car_txt(train_txt, new_train_txt, label_car_name)
    get_only_car_txt(test_txt, new_text_txt, label_car_name)

    shutil.copyfile(new_train_txt, os.path.join(txt_save_path, 'val.txt'))
    shutil.copyfile(new_train_txt, os.path.join(txt_save_path, 'trainval.txt'))


if __name__ == '__main__':
    main()
