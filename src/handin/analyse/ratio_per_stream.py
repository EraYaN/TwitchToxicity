import json

import numpy as np

import os

# os.chdir('D:\Onedrive\TwitchToxicity')
from operator import itemgetter

with open('ratio_per_room.json', 'r') as result_file:
    data = json.loads(result_file.read())

    max = 0
    for room in data:
        deleted = data[room]['deleted']
        total = data[room]['total']
        ratio = data[room]['ratio']
        print("{},{},{},{}".format(room, deleted, total, ratio))
