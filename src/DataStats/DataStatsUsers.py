import pickle
import lzma as compressor
import json
import os
COMPRESSOR_EXTENSION = 'xz'

def userstats(file):
	if os.path.getsize("statsusers2.pickle") > 0: 
		with open("statsusers2.pickle", 'rb') as saved_value:
			result = pickle.load(saved_value)
	else:
		result = {}
	with compressor.open(file, 'rb') as read_file:
		current_pickle = pickle.load(read_file)
		for line in current_pickle:
			streamer = json.dumps(line['room'])
			streamer = streamer.lower()
			if not streamer:
					break
			user = json.dumps(line['from'])
			
			try:
				result[streamer]
			except KeyError:
				result[streamer] = []
			
			if user not in result[streamer]:
				result[streamer].append(user)
	
	with open("statsusers2.pickle", 'wb') as output_file:
		pickle.dump(result, output_file)		
	

if __name__ == "__main__":
	#test_pickle = "D:/Onedrive/TwitchToxicity/data/videos/MLG/G2 vs Cloud9 - Group D  - MLG CSGO Major-v57640742.rechat-filtered.pickle.xz"
	#userstats(test_pickle)
	for root, dirs, files in os.walk("D:/Onedrive/TwitchToxicity/data/videos", topdown=False):
		for name in files:
			if name.endswith('rechat-filtered.pickle.{0}'.format(COMPRESSOR_EXTENSION)):
				userstats(os.path.join(root, name))
	with open("statsusers2.pickle", 'rb') as results:
		for line in results:
			print(line)