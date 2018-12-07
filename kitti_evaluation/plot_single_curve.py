import matplotlib.pyplot as plt
import numpy as np
from utils import parse_result_txt, plot_curve

txtfile = '/media/yangshun/0008EB70000B0B9F/roi_roi_new/kitti/txt/frcnn/stats_car_detection.txt'

matrix = parse_result_txt(txtfile)
plot_curve(matrix)
