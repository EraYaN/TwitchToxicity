import pickle
import os
import unicodedata as ud
import re
import gzip

common_words = None

with open("./data/TwitchEmotes.txt", "r") as Emotes:
    common_words = [line[:-1] for line in Emotes]

big_regex = re.compile(r'\b{}\b'.format(r'\b|\b'.join(map(re.escape, common_words))))


def strip_unicode(s, replace=r''):
    return re.sub(r'[^\x00-\x7f]', replace, ud.normalize('NFD', s))


def filter_rechat(filename):
    with open(filename, "rb") as file:
        data = pickle.load(file)
        filtered_message = []
        for line in data:
            message = line["attributes"]["message"]
            message = big_regex.sub("", message)
            message = strip_unicode(message).strip()
            line["attributes"]["message-filtered"] = message
            if message:
                filtered_message.append(line)
        return filtered_message

if __name__ == "__main__":
    data_folder = "./data/videos"
    for root, dirs, files in os.walk(data_folder, topdown=False):
        for name in files:
            if name.endswith("rechat.pickle"):
                print("Processing %s " % name)
                filtered = filter_rechat(os.path.join(root, name))
                new_filename = name.replace("rechat.pickle", "rechat-filtered.pickle")
                with open(os.path.join(root, new_filename), 'wb') as filtered_file:
                    pickle.dump(filtered, filtered_file)
