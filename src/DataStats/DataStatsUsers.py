import pickle
import lzma as compressor
import json
import os
COMPRESSOR_EXTENSION = 'xz'
#os.chdir('D:\Onedrive\TwitchToxicity')

def userstats(file):
	if os.path.getsize("statsUsers3.pickle") > 0: 
		with open("statsUsers3.pickle", 'rb') as saved_value:
			results = pickle.load(saved_value)
	else:
		results = {}
	with compressor.open(file, 'rb') as read_file:
		current_pickle = pickle.load(read_file)
		for line in current_pickle:
			streamer = json.dumps(line['room'])
			streamer = streamer.lower()
			if not streamer:
					break
			user = json.dumps(line['from'])
			
			try:
				results[streamer]
				result = results[streamer]
			except KeyError:
				results[streamer] = []
				result = []
			
			if user not in result:
				result.append(user)
		results[streamer] = result
	with open("statsusers3.pickle", 'wb') as output_file:
		pickle.dump(results, output_file)		
	

if __name__ == "__main__":
	#test_pickle = "./data/videos/MLG/G2 vs Cloud9 - Group D  - MLG CSGO Major-v57640742.rechat-filtered.pickle.xz"
	#userstats(test_pickle)
	for root, dirs, files in os.walk("./data/videos", topdown=False):
		for name in files:
			if name.endswith('rechat-filtered.pickle.{0}'.format(COMPRESSOR_EXTENSION)):
				print("Now precessing: ")
				try:	
					print(root+name)
				except UnicodeEncodeError:
					print("Can't print name!")
				userstats(os.path.join(root, name))