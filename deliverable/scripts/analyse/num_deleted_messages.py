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

for root, dirs, files in os.walk("./data/videos/AmasHZ", topdown=False):
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
                        results[room]['users'] = {}

                    try:
                        results[room]['users'][user]
                    except KeyError:
                        results[room]['users'][user] = {}
                        results[room]['users'][user]['ratio'] = 0
                        results[room]['users'][user]['total'] = 0
                        results[room]['users'][user]['vids'] = 0

                    try:
                        results[room][vid]
                    except KeyError:
                        results[room][vid] = {}

                    try:
                        results[room][vid][user]
                    except KeyError:
                        results[room][vid][user] = {}
                        results[room][vid][user]['total'] = 0
                        results[room][vid][user]['deleted'] = 0
                        results[room][vid][user]['ratio'] = 0
                        results[room]['users'][user]['vids'] += 1

                    results[room][vid][user]['total'] += 1
                    results[room]['users'][user]['total'] += 1
                    if line['attributes']['deleted']:
                        results[room][vid][user]['deleted'] += 1

                # Finished processing the message, calculate the ratio per vid
                for user in results[room][vid]:
                    results[room][vid][user]['ratio'] = \
                        results[room][vid][user]['deleted'] \
                        / results[room][vid][user]['total']

                    results[room]['users'][user]['ratio'] += results[room][vid][user]['ratio']

rated_results = {}

for room in results:
    rated_results[room] = {}

    for user in results[room]['users']:
        if results[room]['users'][user]['ratio'] > 0 and results[room]['users'][user]['total'] > 10:
            rated_results[room][user] = results[room]['users'][user]['ratio'] / results[room]['users'][user]['vids']

sorted_results = {}
for room in rated_results:
    ratio_count = rated_results[room]
    sorted_deleted_count = sorted(ratio_count.items(), key=itemgetter(1), reverse=True)
    sorted_results[room] = sorted_deleted_count

with open('deleted_per_room.json', 'w') as result_file:
    json.dump(sorted_results, result_file)

# sorted_results = {}
# for room in results:
#    deleted_count = results[room]
#    sorted_deleted_count = sorted(deleted_count.items(), key=itemgetter(1), reverse=True)
#    sorted_results[room] = sorted_deleted_count#
#
# with open('deleted_per_room.json', 'w') as result_file:
#    json.dump(sorted_results, result_file)
