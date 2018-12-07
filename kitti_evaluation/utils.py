import numpy as np
import matplotlib.pyplot as plt


# use txt local to validation kitti result
def calculate_average(txt_name):
    matrix = np.loadtxt(txt_name)
    matrix = np.transpose(matrix)
    need = matrix[::4]
    acc = need.sum(axis=0)/11.0
    return acc


# use txt download from kitti server after submit the result to test
def calculate_average_submit(txt_name):
    result = np.loadtxt(txt_name)  # 41 result
    need = result[::4]  # step 4 to get 11 result
    acc = need.sum(axis=0)[1:]/11.0  # average
    return acc


def print_acc(acc):
    title = ['Easy', 'Moderate', 'Hard']
    line = '\t#' + ('-' * 10 + '#')*3
    print('result: \n')
    print(line)
    print('\t|{:^10}|{:^10}|{:^10}|'.format(*title))
    print(line)
    print('\t|{:^10.4f}|{:^10.4f}|{:^10.4f}|'.format(*acc))
    print(line)


# parse txt to numpy matrix
def parse_result_txt(txtfile):
    x = np.linspace(0.0, 1.0, 41)
    x = np.expand_dims(x, axis=0)
    matrix = np.loadtxt(txtfile)
    if matrix.shape[0] == 3:
        matrix = np.row_stack((x, matrix))
    if matrix.shape[1] == 4:
        matrix = np.transpose(matrix)
    return matrix


def plot_curve(matrix):
    fig, ax = plt.subplots()
    easy = ax.plot(matrix[0], matrix[1], lw=2, label='Easy')
    moderate = ax.plot(matrix[0], matrix[2], lw=2, label='Moderate')
    hard = ax.plot(matrix[0], matrix[3], lw=2, label='Hard')
    ax.legend()
    ax.set_title('Car')
    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    ax.set_xlim(.0, 1.)
    ax.set_ylim(.0, 1.)
    plt.show()

