from __future__ import unicode_literals

import subprocess


def get_chat(url):
    proc = subprocess.Popen(
        [
            'youtube-dl',
            '--config-location', 'youtube-dl.conf',
            '-f', 'bestaudio',
            url
        ]
        , shell=True)
    proc.communicate()


get_chat('https://www.twitch.tv/videos/148361448')
