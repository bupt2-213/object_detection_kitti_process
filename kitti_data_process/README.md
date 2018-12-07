## introduce of each file

* extract_car_label.sh: 只保留训练数据集标签中含有 'car' 类的标签，并生成新的 labels;

* extract_car_label.py: 保留训练数据集标签中含有 'car' 和 'van' 类的标签，并将 'van' 类转换为 'car' 类，生成新的 labels;

* check_data.py: 'data/ImageSets/' 是将训练集分为了训练集和验证集，各包含约50%数据，并且训练集与验证集之间没有相关的序列图片（因为这些图片是从视频序列中选取的，因此有些图片来自于同一个序列，为了减少相关性对训练的影响，尽量保证训练集和验证集不相关）。该程序将提取的只含有'car'的标签分为训练集和验证集;

* kitti2_voc_car.py: 将kitti数据类型转换为voc数据类型（只针对训练数据集，测试集没提供labels）;

* kitti2voc_test_data: 将测试集图像有png转换为jpg格式;

* kitti_train_all.py: 将所有的训练数据集用作训练时，生成对应的ImageSets

## data descripution


>In total, 7481 images are available for training/validation, and 7518 for testing. Since no ground truth is available for the test set, follow [1], splitting the trainval set into training and validation sets. In all ablation experiments, the training set was used for learning and the validation set for evaluation. Following [5], a model was trained for car detection and another for pedestrian/cyclist detection.  [in MSCNN]







## Reference 

[1] Chen, X., Kundu, K., Zhu, Y., Berneshawi, A., Ma, H., Fidler, S., Urtasun, R.: 3d object proposals for accurate object class detection. In: NIPS. (2015)

