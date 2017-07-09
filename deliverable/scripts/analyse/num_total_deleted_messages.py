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

for root, dirs, files in os.walk("./data/videos", topdown=False):
    for name in files:
        if name.endswith('rechat.pickle.{0}'.format(COMPRESSOR_EXTENSION)):
            print('Processing {}\{}'.format(strip_unicode(root), strip_unicode(name)))
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
                        results[room]['total'] = 0
                        results[room]['deleted'] = 0

                    results[room]['total'] += 1
                    if line['attributes']['deleted']:
                        results[room]['deleted'] += 1

for room in results:
    data = results[room]
    ratio = data['deleted'] / data['total']
    results[room]['ratio'] = ratio

print(results)


with open('ratio_per_room.json', 'w') as result_file:
    json.dump(results, result_file)
