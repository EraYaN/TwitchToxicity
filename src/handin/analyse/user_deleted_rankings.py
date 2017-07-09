import json
import pickle
import os
import lzma as compressor
from operator import itemgetter

COMPRESSOR_EXTENSION = 'xz'
import unicodedata as ud
import re


def strip_unicode(s, replace=r''):
    return re.sub(r'[^\x00-\x7f]', replace, ud.normalize('NFD', s))


results = {}
sorted_results = {}

for root, dirs, files in os.walk("./data/videos/AmazHS", topdown=False):
    for name in files:
        if name.endswith('rechat.pickle.{0}'.format(COMPRESSOR_EXTENSION)):
            #print('Processing {}\{}'.format(strip_unicode(root), strip_unicode(name)))
            with compressor.open(os.path.join(root, name), 'rb') as file:

                vid = "v" + name.split('-v')[1].split(".")[0]
                room = None
                data = pickle.load(file)
                for line in data:

                    room = line['attributes']['room']
                    user = line['attributes']['from']

                    try:
                        results[room]
                    except KeyError:
                        results[room] = {}

                    try:
                        results[room][vid]
                    except KeyError:
                        results[room][vid] = {}
                        results[room]['users'] = {}

                    try:
                        results[room][vid][user]
                    except KeyError:
                        results[room][vid][user] = {}
                        results[room][vid][user]['total'] = 0
                        results[room][vid][user]['deleted'] = 0
                        results[room][vid][user]['ratio'] = 0

                    results[room][vid][user]['total'] += 1
                    if line['attributes']['deleted']:
                        results[room][vid][user]['deleted'] += 1

                # Finished processing the message, calculate the ratio per vid
                for user in results[room][vid]:
                    results[room][vid][user]['ratio'] = \
                        results[room][vid][user]['deleted'] \
                        / results[room][vid][user]['total']

                # Sort
                sorted_results[room] = {}
                sorted_results[room][vid] = {}

                for user in results[room][vid]:
                    if results[room][vid][user]['ratio'] > 0 and results[room][vid][user]['total'] > 10:
                        sorted_results[room][vid][user] = results[room][vid][user]['ratio']

                if room is not '' and vid is not '':
                    ratio_count = sorted_results[room][vid]
                    sorted_deleted_count = sorted(ratio_count.items(), key=itemgetter(1), reverse=True)
                    sorted_results[room][vid] = sorted_deleted_count
                    print(sorted_deleted_count)
