import pickle
import unicodedata as ud
import time
import re
try:
    import ujson as json
except:
    import json
import subprocess
import os
import lzma as compressor
COMPRESSOR_EXTENSION = 'xz'
import multiprocessing

BIN_PATH = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../Preprocessor.NET/bin/x64/Release/Preprocessor.NET.exe'))
NUM_CORES = multiprocessing.cpu_count()

def strip_unicode(s, replace=r''):
    return re.sub(r'[^\x00-\x7f]', replace, ud.normalize('NFD', s))

def ProcessFile(filename):
    num = 0
    test_pickle = filename
    test_pickle_filtered = test_pickle.replace('rechat.pickle.{}'.format(COMPRESSOR_EXTENSION),'rechat-filtered.pickle.{}'.format(COMPRESSOR_EXTENSION))
    test_json_out = test_pickle.replace('rechat.pickle.{}'.format(COMPRESSOR_EXTENSION),'rechat.json'.format(COMPRESSOR_EXTENSION))
    test_json_filtered = test_json_out.replace('rechat.json','rechat-filtered.json')
    with compressor.open(test_pickle, 'rb') as compressed_file:
        with open(test_json_out, 'w') as uncompressed_file:
            data=pickle.load(compressed_file)
            for line in data:
                messageObject = {
                    'message':line['attributes']['message'],
                    'has-emotes': (line["attributes"]['tags'].get('emotes') is not None),
                    'from':line['attributes']['from'],
                    'room':line['attributes']['room'],
                    'timestamp':line['attributes']['timestamp'],
                    'video-offset':line['attributes']['video-offset']
                       }
                json.dump(messageObject,uncompressed_file)
                uncompressed_file.write('\n')   
            del data
    
    with subprocess.Popen([BIN_PATH,os.path.abspath(test_json_out),os.path.abspath(test_json_filtered)],stderr=subprocess.PIPE) as proc:
        pass

    with compressor.open(test_pickle_filtered, 'wb') as compressed_file:
        with open(test_json_filtered, 'r') as uncompressed_file:
            data = json.load(uncompressed_file)
            num = len(data)
            pickle.dump(data,compressed_file)
            del data
    os.remove(test_json_out)
    os.remove(test_json_filtered)
    return num

def ProcessFileTimingWrapper(rootname):    
    try:
        root = rootname[0]
        name = rootname[1]
        shortname = (name[:66] + '...') if len(name) > 66 else name
        #print("Processing {}".format(strip_unicode(name)))
        start_time = time.time()
        num = ProcessFile(os.path.join(root, name))
        end_time = time.time()
        


        print("#{:02d}: Processed {:70} containing {:6} messages with {:8.1f} messages per second".format(int(multiprocessing.current_process().name[16:]),strip_unicode(shortname),num,num/(end_time - start_time)))
    except Exception:
        print("#{:02d}: Exception for {:70}".format(int(multiprocessing.current_process().name[16:]),strip_unicode(shortname)))
        import sys, traceback
        traceback.print_exc(file=sys.stderr)

if __name__ == "__main__":
    data_folder = './data/videos'
    if os.path.exists(BIN_PATH):
        print("External Filter executable found.");
        print("Starting pool...");
        p = multiprocessing.Pool(NUM_CORES)         
        
        print("Listing files...");
        filenames = []
        for root, dirs, files in os.walk(data_folder, topdown=False):
            for name in files:
                if name.endswith('rechat.pickle.{0}'.format(COMPRESSOR_EXTENSION)):
                    filenames.append((root, name))

        #filenames = [("./data/videos/MLG","Luminosity Gaming vs Virtus Pro - Quarter Finals - MLG CSGO Major-v58219102.rechat.pickle.xz")]
        print("Listing files done. Got {} files.".format(len(filenames)));
        print("Mapping to pool...");
        p.map(ProcessFileTimingWrapper, filenames)        
        print("All files were processed. Done.");
    else:
         print("Could not find external filter executable. Did you build it?");
    

