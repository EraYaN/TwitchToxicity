import pickle
import os
import unicodedata as ud
import re
import lzma as compressor
from joblib import Parallel, delayed
import multiprocessing
from math import ceil
import time
COMPRESSOR_EXTENSION = 'xz'

common_words = []

CHUNK_SIZE=5000
USE_REGEX = False
NUM_CORES = multiprocessing.cpu_count()

big_regexes = []

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def make_regexes(words):
    regexes = []
    i = 1
    num_words = len(words)
    for chunk in chunks(common_words,CHUNK_SIZE):
        print('Adding regex {} out of {}...'.format(i,ceil(num_words/CHUNK_SIZE)))
        regexes.append(re.compile(r'\b{}\b'.format(r'\b|\b'.join(map(re.escape, chunk))),flags=re.IGNORECASE))
        print('Added regex {} out of {}'.format(i,ceil(num_words/CHUNK_SIZE)))
        i+=1
    return regexes


def replace_all(text, words):
    for word in words[15607:15689]:
        text = text.replace(word, '')
    return text

def replace_all_re(text,regexes):
    for regex in regexes:
        text = regex.sub("", text)
    return text

def strip_unicode(s, replace=r''):
    return re.sub(r'[^\x00-\x7f]', replace, ud.normalize('NFD', s))


def sub_filter(line,words):  
    message = line["attributes"]["message"] 
    if line["attributes"]['tags'].get('emotes'):
        if USE_REGEX:
            message = replace_all_re(message,words)
        else:
            message = replace_all(message,words)    

    line["attributes"]["message-filtered"] = strip_unicode(message).strip()
    if line["attributes"]["message-filtered"]:
        return line
    else: 
        return None

def filter_rechat(filename, parallel):
    with compressor.open(filename, "rb") as file:
        data = pickle.load(file)
        num = len(data)
        start_time = time.time()

        if USE_REGEX:
            #filtered_messages = [sub_filter(line,big_regexes) for line in data] 
            filtered_messages = parallel(delayed(sub_filter)(line,big_regexes) for line in data)  
        else:            
            #filtered_messages = [sub_filter(line,common_words) for line in data]     
            filtered_messages = parallel(delayed(sub_filter)(line,common_words) for line in data)  
        
        filtered_messages = [m for m in filtered_messages if m]
        
        end_time = time.time()

        print("Processed {:.1f} messages per second from {} messages".format(num/(end_time - start_time),num))
        return filtered_messages


if __name__ == "__main__":
    print('Loading words...')
    with open("./data/resources/TwitchEmotes.txt", "r") as Emotes:
        common_words = [line[:-1] for line in Emotes]

    if USE_REGEX:
        print("Compiling regexes...")
        big_regexes = make_regexes(common_words)
    print("Start the filtering...")
    data_folder = "./data/videos"
    #os.sched_setaffinity(0, range(NUM_CORES))
    with Parallel(n_jobs=NUM_CORES) as parallel:
    #    for root, dirs, files in os.walk(data_folder, topdown=False):
     #       for name in files:
     #           if name.endswith('rechat.pickle.{0}'.format(COMPRESSOR_EXTENSION)):
        root = "./data/videos/MLG/"
        name = "Luminosity Gaming vs Virtus Pro - Quarter Finals - MLG CSGO Major-v58219102.rechat.pickle.xz"
        print("Processing {}".format(strip_unicode(name)))
        filtered = filter_rechat(os.path.join(root, name),parallel)
        new_filename = name.replace('rechat.pickle.{0}'.format(COMPRESSOR_EXTENSION), 'rechat-filtered.pickle.{0}'.format(COMPRESSOR_EXTENSION))
        with compressor.open(os.path.join(root, new_filename), 'wb') as filtered_file:

            pickle.dump(filtered, filtered_file)
