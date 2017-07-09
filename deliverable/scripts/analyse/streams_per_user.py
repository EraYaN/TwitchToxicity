import pickle
import lzma as compressor
import json
import os
from operator import itemgetter
COMPRESSOR_EXTENSION = 'xz'
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline
os.chdir('D:\Onedrive\TwitchToxicity')

users = {}
with open("statsUsers.pickle", 'rb') as read_file:
	current_pickle = pickle.load(read_file)
	for line in current_pickle:
		current_users = current_pickle.get(line)
		for user in current_users:
			if "bot" not in user:
				if "twitchnotify" not in user:
					if user in users:
						users[user] += 1
					else:
						users[user] = 1

sorted_users = sorted(users.items(), key=itemgetter(1), reverse = True)
max_streams = max(users.values())

count = {}
for i in range(1, max_streams+1):
	count[i] = 0
for value in users.values():
	count[value] += 1
	
xnew = np.linspace(min(count.keys()),max(count.keys()),200)
smooth = spline(list(count.keys()),list(count.values()),xnew)
plt.plot(xnew,smooth)
#plt.plot(list(count.keys()),list(count.values()))
#plt.axis([1, max_streams, 0, (max(count.values()))])
#plt.yscale('log')
plt.xlabel('Number of differents streamers')
plt.ylabel('Number of users')
plt.show()
