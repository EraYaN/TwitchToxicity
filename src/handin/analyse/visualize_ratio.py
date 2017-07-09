import json

import numpy as np

import os

# os.chdir('D:\Onedrive\TwitchToxicity')

with open('ratio_deleted.json', 'r') as result_file:
    data = json.loads(result_file.read())

    xt = list(range(1, 101))

    # Streams:
    # mlg
    # eleague
    # dreamhackcs


    mlg_count = {}
    eleaguetv_count = {}
    dreamhackcs_count = {}

    for i in xt:
        mlg_count[i] = 0
        eleaguetv_count[i] = 0
        dreamhackcs_count[i] = 0

    for user in data['mlg']:
        ratio = round(user[1] * 100)
        if ratio is not 0:
            mlg_count[ratio] += 1

    for user in data['eleaguetv']:
        ratio = round(user[1] * 100)
        if ratio is not 0:
            eleaguetv_count[ratio] += 1

    for user in data['dreamhackcs']:
        ratio = round(user[1] * 100)
        if ratio is not 0:
            dreamhackcs_count[ratio] += 1

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

dhc_x = []
dhc_y = []
for key in dreamhackcs_count:
    dhc_x.append(key)
    dhc_y.append(dreamhackcs_count[key])

import matplotlib.pyplot as plt
from scipy.interpolate import spline

# Two subplots, the axes array is 1-d
# f, axarr = plt.subplots(2, sharex=True)
# axarr[0].plot(mlg_x, mlg_y)
# axarr[0].set_title('Sharing X axis')
# axarr[1].plot(etv_x, etv_y)
xnew = np.linspace(min(mlg_x), max(mlg_x), 300)
mlg_y = [(float(i) / sum(mlg_y)) * 100 for i in mlg_y]
etv_y = [(float(i) / sum(etv_y)) * 100 for i in etv_y]
dhc_y = [(float(i) / sum(dhc_y)) * 100 for i in dhc_y]
smooth1 = spline(mlg_x, mlg_y, xnew)
smooth2 = spline(etv_x, etv_y, xnew)
smooth3 = spline(dhc_x, dhc_y, xnew)
mlg_plot = plt.plot(xnew, smooth1, 'r', label="MLG")
etv_plot = plt.plot(xnew, smooth2, 'b', label="ELEAGE TV")
dhc_plot = plt.plot(xnew, smooth3, 'g', label="Dreamhackcs")

plt.legend()
plt.xlabel('Percentage of deleted messages')
plt.ylabel('Percentage of users')

plt.show()
