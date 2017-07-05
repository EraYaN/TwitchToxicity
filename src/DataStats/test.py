import pickle
import lzma as compressor
import re
import os
import csv
COMPRESSOR_EXTENSION = 'xz'
from operator import itemgetter
try:
    import ujson as json
except:
    import json
	
with compressor.open('D:/Onedrive/TwitchToxicity/data/videos/MLG/G2 vs Cloud9 - Group D  - MLG CSGO Major-v57640742.rechat-filtered.pickle.xz', 'rb') as read_file:
	current_pickle = pickle.load(read_file)
	for line in current_pickle:
		print(line)