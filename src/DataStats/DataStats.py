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
	
def pickleStats(file):
	with compressor.open(file, 'rb') as read_file:
		if os.path.getsize("stats.pickle") > 0: 
			with open("stats.pickle", 'rb') as wordlist:
				wordcount = pickle.load(wordlist)
		else:
			wordcount = {}
		test_pickle = pickle.load(read_file)
		for line in test_pickle:
			text = json.dumps(line['message-filtered'])
			words = text.split()
			for word in words:
				word = re.sub(r'\W+', '', word)
				word = word.lower()
				if not word:
					break
				if word not in wordcount:
					wordcount[word] = 1
				else:
					wordcount[word] += 1
			
	with open("stats.pickle", 'wb') as output_file:
		pickle.dump(wordcount, output_file)

if __name__ == "__main__":
	test_pickle = "./data/videos/MLG/G2 vs Cloud9 - Group D  - MLG CSGO Major-v57640742.rechat-filtered.pickle.xz"
	with open("stats.pickle", 'w+') as test:
		print(test)
	for root, dirs, files in os.walk("./data/videos", topdown=False):
		for name in files:
			if name.endswith('rechat-filtered.pickle.{0}'.format(COMPRESSOR_EXTENSION)):
				pickleStats(os.path.join(root, name))
	with open("stats.pickle", 'rb') as wordlist:
		wordcount = pickle.load(wordlist)
	wordcount = sorted(wordcount.items(), key=itemgetter(1), reverse = True)
	with open('wordcount.csv','w', newline='') as f:
		w = csv.writer(f, delimiter=";")
		w.writerow(['Word','Wordcount'])
		for row in wordcount:
			w.writerow(row)
		