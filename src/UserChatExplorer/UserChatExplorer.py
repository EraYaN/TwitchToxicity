import pickle
import os
from collections import OrderedDict
import unicodedata as ud
import re 
def strip_unicode(s,replace=r''):
    return re.sub(r'[^\x00-\x7f]',replace,ud.normalize('NFD',s))

users = {}

for root, dirs, files in os.walk("./data/videos", topdown=False):
    for name in files:
        if name.endswith('rechat.pickle'):
            print('Processing {}\{}'.format(strip_unicode(root),strip_unicode(name)));
            with open(os.path.join(root, name),'rb') as file:
                data = pickle.load(file)
                for line in data:
                    room = line['attributes']['room']
                    user = line['attributes']['from']
                    if user not in users:
                        users[user] = {}

                    if room not in users[user]:
                        users[user][room] = 1
                    else:
                        users[user][room] += 1
  
users_list = []
for user in users:
    users_list.append({"user":user,"channels":users[user], "count": len(users[user])})

print('Sorting...')

users_sorted = OrderedDict(sorted(users_list, key=lambda x: x["count"]))
print('Saving...')
with open('user-char-explorer-result.pickle','wb') as f:
    pickle.dump(users_sorted,f)