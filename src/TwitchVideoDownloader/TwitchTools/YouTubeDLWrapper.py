import subprocess
import youtube_dl
import json
import logging
import os

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

class YouTubeDLWrapper:
    

    lastresult = None   
    progress_messages = 50
    def __init__(self, id, root):
        self.logger = logging.getLogger(id)
        self.ydl_opts = {
            'writeinfojson':True,       
            'writethumbnail':True,
            #'writesubtitles':True,
            #'writeautomaticsub':True,
            #'allsubtitles':True,
            'noprogress':True,
            'quiet':True,
            'prefer_ffmpeg':True,
            'encoding': 'utf-8',
            'cachedir': 'cache/',
            'outtmpl': os.path.realpath(os.path.join(root,'data/videos/%(uploader)s/%(title)s-%(id)s.%(ext)s')),
            'call_home': False,
            'logger': self.logger,
            'format':'bestaudio/audio_only/Audio_Only',
            'skip_download':True,
            'progress_hooks': [ self.progress_hook ]
        }

    def download_video(self, vod_info):
        try:
            self.progress = -1
            self.lastresult = None
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                urls = ['https://twitch.tv/videos/{}'.format(vod_info['id'][1:])] # Strip the v, so youtube-dl is not confused.
                ydl.download(urls)
        except KeyboardInterrupt:
            self.logger.critical('Received interrupt...')

    def LogProgress(self,d):
        """Parameter d contains:
            * filename: The final filename (always present)
            * tmpfilename: The filename we're currently writing to
            * downloaded_bytes: Bytes on disk
            * total_bytes: Size of the whole file, None if unknown
            * total_bytes_estimate: Guess of the eventual file size,
                                    None if unavailable.
            * elapsed: The number of seconds since download started.
            * eta: The estimated time in seconds, None if unknown
            * speed: The download speed in bytes/second, None if
                    unknown
            * fragment_index: The counter of the currently
                                downloaded video fragment.
            * fragment_count: The number of fragments (= individual
                                files that will be merged)"""
        
        size = None
        try:
            if 'total_bytes' in d:
                size = d['total_bytes']
            else:
                if 'total_bytes_estimate' in d:
                    size = d['total_bytes_estimate']
            if size is not None:
                progress_interval = size/self.progress_messages
                #print("{} {} {:.1%}".format(d['downloaded_bytes'],self.progress*progress_interval,d['downloaded_bytes']/size))

                if self.progress == -1:
                    if 'downloaded_bytes' in d and d['downloaded_bytes'] is not None:
                        self.progress = int(d['downloaded_bytes']/progress_interval)
                        if self.progress > 0:
                            self.logger.info("Resuming download...")
                    else:
                        return

                if d['downloaded_bytes'] > self.progress*progress_interval:
                    self.progress += 1
                    if 'fragment_index' in d and 'fragment_count' in d and 'eta' in d and 'speed' in d and d['fragment_index'] is not None and d['fragment_count'] is not None and d['eta'] is not None and d['speed'] is not None:
                        self.logger.info("Download: {} of {} ({:.1%}) at {} ETA: {}. Fragement {} of {}".format(
                            sizeof_fmt(d['downloaded_bytes']),
                            sizeof_fmt(size),
                            d['downloaded_bytes']/size,                    
                            sizeof_fmt(d['speed'],'B/s'),
                            d['eta'],
                            d['fragment_index'],
                            d['fragment_count']
                            )
                        )
                    elif 'eta' in d and 'speed' in d and d['eta'] is not None and d['speed'] is not None:
                        self.logger.info("Download: {} of {} ({:.1%}) at {} ETA: {}.".format(
                            sizeof_fmt(d['downloaded_bytes']),
                            sizeof_fmt(size),
                            d['downloaded_bytes']/size,                    
                            sizeof_fmt(d['speed'],'B/s'),
                            d['eta']
                            )
                        )
                    elif 'fragment_index' in d and 'fragment_count' in d and d['fragment_index'] is not None and d['fragment_count'] is not None:
                        self.logger.info("Download: {} of {} ({:.1%}) Fragement {} of {}.".format(
                            sizeof_fmt(d['downloaded_bytes']),
                            sizeof_fmt(size),
                            d['downloaded_bytes']/size,
                            d['fragment_index'],
                            d['fragment_count']
                            )
                        )
                    else:
                        self.logger.info("Download: {} of {} ({:.1%}).".format(
                            sizeof_fmt(d['downloaded_bytes']),
                            sizeof_fmt(size),
                            d['downloaded_bytes']/size
                            )
                        )
        except Exception as e:
            import sys, traceback
            traceback.print_exc(file=sys.stderr)

    def progress_hook(self, d):
        """Main Progress Hook"""
        self.lastresult = d
        if(d is not None): 
            self.LogProgress(d)
            if d['status'] != 'downloading':
                self.lastresult = d
            if d['status'] == 'finished':
                self.logger.info('Done downloading, now converting...')

