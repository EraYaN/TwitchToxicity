import json

import numpy as np

with open('ratio_deleted.json', 'r') as result_file:
    data = json.loads(result_file.read())

    xt = list(range(1, 101))


    # Streams:
    # mlg
    # eleague


    mlg_count = {}
    eleaguetv_count = {}
    riotgames_count = {}

    for i in xt:
        mlg_count[i] = 0
        eleaguetv_count[i] = 0

    for user in data['mlg']:
        ratio = round(user[1] * 100)
        if ratio is not 0:
            mlg_count[ratio] += 1

    for user in data['eleaguetv']:
        ratio = round(user[1] * 100)
        if ratio is not 0:
            eleaguetv_count[ratio] += 1

mlg_x = []
mlg_y = []
for key in mlg_count:
    mlg_x.append(key)
    mlg_y.append(mlg_count[key])

etv_x = []
etv_y = []
for key in eleaguetv_count:
    etv_x.append(key)
    etv_y.append(eleaguetv_count[key])

import matplotlib.pyplot as plt

# Two subplots, the axes array is 1-d
f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(mlg_x, mlg_y)
axarr[0].set_title('Sharing X axis')
axarr[1].plot(etv_x, etv_y)

plt.show()
