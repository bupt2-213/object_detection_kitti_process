import os
import numpy as np
from utils import calculate_average, print_acc

file_root = '/media/yangshun/0008EB70000B0B9F/roi_roi_new/kitti/txt/pytorch/context/'

car_stats = os.path.join(file_root, 'stats_car_detection.txt')

accuracy = calculate_average(car_stats)
print_acc(accuracy)


