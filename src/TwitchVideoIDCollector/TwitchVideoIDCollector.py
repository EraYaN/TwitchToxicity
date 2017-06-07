from twitch import TwitchClient
import pickle
from datetime import datetime
from collections import OrderedDict

chat_replay_implemented = datetime(2016, 2, 23) # Date from (https://blog.twitch.tv/update-chat-replay-is-now-live-the-official-twitch-blog-aac0b82305b6)
PAGE_SIZE = 100

class VideoParser:

    def __init__(self):
        self.top100 = ['syndicate', 'riotgames', 'summit1g', 'esl_csgo', 'esltv_cs', 'nightblue3', 'imaqtpie', 'lirikk',
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
        self.videolist = []

    def get_user_data(self, client, user):
        channel = client.channels.get_by_id(user.id)
        lastpage = False
        offset = 0
        count = 0
        duplicates = 0
        discarded = 0
        while not lastpage:
            print("\rAdded {} videos of {}. Grabbing videos page {:d} for {}...".format(count,count+discarded,int(offset/PAGE_SIZE)+1,user['name']),end='')
            videos = client.channels.get_videos(channel.id, limit=PAGE_SIZE, offset=offset, sort="views")
            if len(videos) < 100:
                lastpage = True
            videodicts = []
            for v in [OrderedDict(v) for v in videos]:
                v['channel'] = OrderedDict(v['channel'])
                if v['published_at'] > chat_replay_implemented:
                    if v['id'] not in self.videolist:
                        v['duplicate'] = False
                        self.videolist.append(v['id'])                        
                    else:
                        v['duplicate'] = True
                        duplicates += 1

                    videodicts.append(v)
                    count += 1
                else:
                    discarded += 1
                    #print('Discarded video {} from {} from {} because it is too old.'.format(v['id'],user['name'],v['recorded_at']))

            offset += PAGE_SIZE
        print("\rFor user {} added {} videos of {} in {} pages. {} were duplicates.          ".format(user['name'],count,count+discarded,int(offset/PAGE_SIZE),duplicates))
        return {
            'user'    : OrderedDict(user),
            'videos': videodicts
        }
        
    def run(self, filename):
        print("Initializing Twitch API...")
        client = TwitchClient('df1trcokk8t1si5eloxe1lg1e0040f', 'aikw60xp68fz1tblq0vqyzb5cdz7m2')
        users = client.users.translate_usernames_to_ids(self.top100)
        count = 1
        data = OrderedDict()
        
        for user in users:
            print("Loading data for user {:03d} of {:03d}: {}".format(count, len(users), user.name))
            data[user.name] = self.get_user_data(client, user)
            print("Done loading data for user {:03d} of {:03d}: {}\n".format(count, len(users), user.name))
            count += 1

        print("Writng all results to {}...".format(filename))
        with open(filename, "wb") as f:
            pickle.dump(data, f)

###########################################
if __name__ == '__main__':
	parser = VideoParser()
	parser.run("data\\video-ids\\top100-videos-per-user.pickle")