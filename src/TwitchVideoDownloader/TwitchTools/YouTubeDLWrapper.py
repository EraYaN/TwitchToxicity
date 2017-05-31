import subprocess
import youtube_dl
import json

class YouTubeDLWrapper:
    

    lastfilename = None    

    def __init__(self):
        self.ydl_opts = {
            'writeinfojson':True,
            'writeannotations':True,
            'writeannotations':True,        
            'writethumbnail':True,
            #'writesubtitles':True,
            #'writeautomaticsub':True,
            #'allsubtitles':True,
            'prefer_ffmpeg':True,
            'encoding': 'utf-8',
            'cachedir': 'cache/',
            'outtmpl': 'data/%(uploader)s/%(title)s-%(id)s.%(ext)s',
            'call_home': False,
            'format':'bestaudio/audio_oly/Audio_Only',
            'progress_hooks': [ self.progress_hook ] #TODO trigger rechat download
        }

    def download_video(self, vod_info):
        try:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                urls = ['https://twitch.tv/videos/{}'.format(vod_info['id'][1:])] # Strip the v, so youtube-dl is not confused.
                ydl.download(urls)
        except KeyboardInterrupt:
            print('\n\nReceived interrupt...\n')
        
    
    def progress_hook(self, d):
        """unused as of yet"""
        if d['status'] == 'finished':
            self.lastfilename = d['filename']
            print('Done downloading, now converting...')

