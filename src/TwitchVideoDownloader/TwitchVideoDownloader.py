import subprocess
import os
import pickle
try:
    import ujson as json
except:
    import json
import TwitchTools.YouTubeDLWrapper as yt
import TwitchTools.RechatScraper as rs
from datetime import datetime

CID = 'df1trcokk8t1si5eloxe1lg1e0040f'

def ProcessVideo(video_info):
    print("Initializing YouTubeDLWrapper....")
    ydlw = yt.YouTubeDLWrapper()
    print("Downloading video....")

    ydlw.download_video(video_info)

    base = os.path.splitext(ydlw.lastfilename)[0]
    api_info_file = base + '.apiinfo.pickle'
    print("Saving Twitch API video info....")
    with open(api_info_file,'wb') as f:
        info = pickle.dump(video_info,f)

    info_file = base + '.info.json'

    print("Reading YouTube-DL info....")
    with open(info_file,'r') as f:
        info = json.load(f)    

    rs.download_rechat(CID, video_info, base + '.rechat.pickle')

if __name__ == '__main__':
    
    print("Loading data....")
    with open("data\\video-ids\\top100-videos-per-user.pickle",'rb') as top100file:
        top100_videos = pickle.load(top100file,encoding='utf-8',fix_imports=True)

    #Testing only
    #TODO Deduplicate
    video_info = None
    
    for user in top100_videos:
        print('Checking user {} for test video.'.format(user))
        for v in top100_videos[user]['videos']:            
            if v['length'] < 30*60: ## Short length
                video_info = v
                print('Found video {} from {} for test video with length {} from {}.'.format(v['id'],user,v['length'],v['recorded_at'] ))
                break
            else:
                print('Passed video {} from {} for test video with length {} from {}.'.format(v['id'],user,v['length'],v['recorded_at'] ))
        if video_info != None:
            break

    if video_info == None:
        print("Could not find short test video....")
   
    ProcessVideo(video_info)

    print('Done.')
