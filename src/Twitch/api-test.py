from twitch import TwitchClient
from datetime import datetime
import json

class VideoParser:

	def __init__(self):
		self.top100 = [
			'syndicate', 'riotgames', 'summit1g', 'esl_csgo', 'esltv_cs', 'nightblue3', 'imaqtpie', 'lirikk',
			'lirik', 'sodapoppin', 'wolves_bjergsen', 'officialbjergsen', 'tsm_bjergsen', 'captainsparklez', 'Tsm_dyrus',
			'dyrus', 'theoriginalweed', 'joshog', 'goldglove', 'gosu', 'castro_1021', 'boxbox', 'dreamhackcs', 'timthetatman',
			'trick2g', 'nl_kripp', 'swiftor', 'doublelift', 'speeddemosarchivesda', 'gamesdonequick', 'sgdq', 'sivhd',
			'c9sneaky', 'iijeriichoii', 'meclipse', 'shroud', 'Voyboy', 'tsm_theoddone', 'pewdiepie', 'eleaguetv', 'Tsm_doublelift',
			'pashabiceps', 'faceittv', 'Faceit', 'amazhs', 'anomalyxd', 'izakooo', 'cohhcarnage', 'omgitsfirefoxx', 'trumpsc', 'trump',
			'kittyplaysgames', 'kittyplays', 'mlg_live', 'mlg', 'ungespielt', 'gassymexican', 'faker', 'kinggothalion', 'GiantWaffle',
			'bobross', 'nadeshot', 'thenadeshot', 'Gronkh', 'cryaotic', 'nick28t', 'monstercat', 'kaypealol', 'm0e_tv', 'nickbunyun',
			'montanablack88', 'legendarylea', 'loltyler1', 'reckful', 'yogscast', 'ProfessorBroman', 'forsenlol', 'olofmeister',
			'tsm_wildturtle', 'markiplier', 'rewinside', 'dansgaming', 'aphromoo', 'kyr_sp33dy', 'froggen', 'a_seagull', 'yoda',
			'stonedyooda', 'cheatbanned', 'towelliee', 'twitch', 'e3', 'starladder5', 'dendi', 'sp4zie', 'streamerhouse',
			'drdisrespectlive', 'esl_lol', 'esltv_lol', 'Aiekillu'
		]
		
	def serialize(self, obj):
		if isinstance(obj, datetime):
			serial = obj.isoformat()
			return serial
		raise TypeError ("Type not serializable")
		
	def write(self, data):
		f = open("videos-per-user.txt", "w+")
		f.write(json.dumps({'users': data}, default=self.serialize))
		f.close()
	
	def parseUser(self, client, user):
		channel = client.channels.get_by_id(user.id)
		videos = client.channels.get_videos(channel.id, limit=100, sort="views")
		
		return {
			'id'    : user.id,
			'name'  : user.name,
			'videos': videos
		}
		
	def run(self):
		client = TwitchClient('df1trcokk8t1si5eloxe1lg1e0040f', 'aikw60xp68fz1tblq0vqyzb5cdz7m2')
		users = client.users.translate_usernames_to_ids(self.top100)
		count = 1
		data = []
		
		for user in users:
			data.append(self.parseUser(client, user))
			print("User {:03d}: {}".format(count, user.name))
			count += 1
		
		self.write(data)

###########################################

if __name__ == '__main__':
	parser = VideoParser()
	parser.run()