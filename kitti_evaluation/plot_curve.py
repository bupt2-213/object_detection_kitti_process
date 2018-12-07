import matplotlib.pyplot as plt

x = [i/40.0 for i in range(0, 41)]
fpn_2_layer = '/home/yangshun/PycharmProjects/KITTI_progress/data/curve_txt/fpn_2_layer.txt'
fpn_context = '/home/yangshun/PycharmProjects/KITTI_progress/data/curve_txt/fpn_context.txt'
fpn = '/home/yangshun/PycharmProjects/KITTI_progress/data/curve_txt/roi_roi34no5.txt'
roi_roi345 = '/home/yangshun/PycharmProjects/KITTI_progress/data/curve_txt/fpn.txt'


def read_txt_as_list(txt_path):
    y = []
    with open(txt_path, 'rb') as f:
        lines = f.readlines()
        for line in lines:
            y_ = line.strip().split(' ')
            y.append(y_)
    return y

y_2_layer = read_txt_as_list(fpn_2_layer)
y_context = read_txt_as_list(fpn_context)
y_roi = read_txt_as_list(roi_roi345)
y_fpn = read_txt_as_list(fpn)


def plot(y, label, title, rate):
    lw = 2
    curve1, = plt.plot(x[:len(y[0])], y[0], lw=lw, label=label[3]+rate[0])
    curve2, = plt.plot(x[:len(y[1])], y[1], lw=lw, label=label[2]+rate[1])
    curve3, = plt.plot(x[:len(y[2])], y[2], lw=lw, label=label[1]+rate[2])
    curve4, = plt.plot(x[:len(y[3])], y[3], lw=lw, label=label[0]+rate[3])
    plt.axis([0, 1, 0, 1])
    plt.legend(handles=[curve4, curve3, curve2, curve1], prop={'size': 11})
    plt.title(title)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.grid('on')
    plt.savefig('../images/'+title+'.eps', format='eps')


y = [[], [], []]
for i in range(len(y_roi)):
    y[i].append(y_2_layer[i])
    y[i].append(y_context[i])
    y[i].append(y_fpn[i])
    y[i].append(y_roi[i])

labels = ['roi-context-',
          'feature pyramid with 3 layers-',
          'feature pyramid and context with 3 layers-',
          'feature pyramid and context with 2 layers-']
plt.figure()
plot(y[0], labels, 'Easy', ['0.9299', '0.9296', '0.9248', '0.9401'])

plt.figure()
plot(y[1], labels, 'Moderate', ['0.7826', '0.8567', '0.8398', '0.8589'])

plt.figure()
plot(y[2], labels, 'Hard', ['0.6847', '0.6995', '0.6897', '0.7008'])

plt.show()
