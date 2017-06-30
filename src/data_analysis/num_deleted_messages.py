import json
import pickle
import os
import lzma as compressor

COMPRESSOR_EXTENSION = 'xz'
import unicodedata as ud
import re


def strip_unicode(s, replace=r''):
    return re.sub(r'[^\x00-\x7f]', replace, ud.normalize('NFD', s))

results = {}

for root, dirs, files in os.walk("./data/videos", topdown=False):
    for name in files:
        if name.endswith('rechat.pickle.{0}'.format(COMPRESSOR_EXTENSION)):
            print('Processing {}\{}'.format(strip_unicode(root), strip_unicode(name)));
            with compressor.open(os.path.join(root, name), 'rb') as file:
                data = pickle.load(file)
                for line in data:

                    room = line['attributes']['room']
                    user = line['attributes']['from']

                    try:
                        results[room]
                    except KeyError:
                        results[room] = {}

                    try:
                        results[room][user]
                    except KeyError:
                        results[room][user] = 0

                    deleted = line['attributes']['deleted']
                    if deleted:
                        results[room][user] += 1


with open('deleted_per_room.json', 'w') as result_file:
    json.dump(results, result_file)
