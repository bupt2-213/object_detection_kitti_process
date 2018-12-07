import json
import os
import pprint

json_dir = '/home/yangshun/datasets/KITTIVOC/json'
train_json = os.path.join(json_dir, 'train.json')

with open(train_json, 'r') as f:
    train_anno = json.load(f)
pprint.pprint(train_anno)
