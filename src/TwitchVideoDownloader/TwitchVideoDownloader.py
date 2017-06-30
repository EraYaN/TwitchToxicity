import subprocess
import os
import pickle
try:
    import ujson as json
except:
    import json
import TwitchTools.YouTubeDLWrapper as yt
import TwitchTools.RechatScraper as rs
from datetime import datetime
import lzma as compressor
COMPRESSOR_EXTENSION = 'xz'
import logging
import logging.handlers
import multiprocessing as mp
import argparse as ap
import sys
import colorama
import signal
import time

CID = 'df1trcokk8t1si5eloxe1lg1e0040f'

global_results=[]

def listener_configurer():
    root = logging.getLogger()
    root.handlers = []
    h = logging.StreamHandler()
    f = logging.Formatter('%(asctime)s - %(name)10s - %(levelname)7s - %(message)s')
    h.setFormatter(f)
    root.addHandler(h)

def listener_process(queue, configurer):
    configurer()
    while True:
        try:
            record = queue.get()
            if record is None: # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record) # No level or filter logic applied - just do it!
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            import sys, traceback
            sys.stderr.write('Whoops! Problem:')
            traceback.print_exc(file=sys.stderr)
            sys.stderr.write('\n')

def worker_configurer(queue):
    h = logging.handlers.QueueHandler(queue) # Just the one handler needed
    root = logging.getLogger()    
    root.handlers = []
    root.addHandler(h)
    root.setLevel(logging.INFO) # send all messages, for demo; no other level or filter logic applied.

def ProcessVideo(queue, configurer, video_info, root, skip_video): 
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    configurer(queue)
    
    threadlogger = logging.getLogger(video_info['id'])    

    threadlogger.info("Initializing YouTubeDLWrapper....")
    ydlw = yt.YouTubeDLWrapper(video_info['id'],root)
    threadlogger.info("Downloading video....")

    ydlw.download_video(video_info)

    if(ydlw.lastresult is not None):

        download_result = (ydlw.lastresult['status'] == 'finished')

        base = os.path.splitext(ydlw.lastresult['filename'])[0]
        api_info_file = base + '.apiinfo.pickle.{0}'.format(COMPRESSOR_EXTENSION)
        threadlogger.info("Saving Twitch API video info....")
        with compressor.open(api_info_file,'wb') as f:
            info = pickle.dump(video_info,f)

        info_file = base + '.info.json'

        #threadlogger.info("Reading YouTube-DL info....")
        #with open(info_file,'r') as f:
        #    info = json.load(f)    
        threadlogger.info("Downloading chat....")
        rechat_result = rs.download_rechat(CID, video_info, base + '.rechat.pickle.{0}'.format(COMPRESSOR_EXTENSION))
    else:
        rechat_result = False
        download_result = False

    return (video_info['id'],download_result, rechat_result)

def log_result(result):
    global_results.append(result)    

def log_error(error):
    import sys, traceback
    sys.stderr.write("Got error: {}\n".format(error))
    traceback.print_exc(file=sys.stderr)


if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='Twitch Video Downloader',description='Twitch Video Downloader')    
    parser.add_argument('inputfile', action="store",nargs='?', help='The input file, generated using TwitchVideoIDCollector. Relative to root.',default='data/video-ids/top100-videos-per-user.pickle')
    parser.add_argument('--root', action="store", help='The output root folder. Default is current directory.',default=os.getcwd())
    parser.add_argument('--result-file', action="store", help='The results file. Relative to root.',default='data/results.txt')
    parser.add_argument('--threads', action="store", type=int, help='The size of the thread pool.',default='8')
    parser.add_argument('--skip-stream', action="store", help='Skip stream download.')

    pool = None
    listener = None

    try:
        # create basic logger config
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)10s - %(levelname)7s - %(message)s')
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        opts = parser.parse_args(sys.argv[1:])
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        if opts.threads == 0:
            pool = mp.Pool()
        else:
            pool = mp.Pool(opts.threads)
        signal.signal(signal.SIGINT, original_sigint_handler)
        
        if not os.access(opts.root, os.W_OK):
            logger.critical("The root direcotry {} should be writable by the process.".format(os.path.realpath(opts.root)))
            exit(1)

        if not os.access(os.path.join(opts.root,opts.inputfile), os.R_OK):
            logger.critical("Input file {} should be readable by the process.".format(os.path.realpath(os.path.join(opts.root,opts.inputfile))))
            exit(1)

        if not os.access(os.path.join(opts.root,opts.result_file), os.W_OK) and not os.access(os.path.dirname(os.path.join(opts.root,opts.result_file)), os.W_OK):
            logger.critical("Result file {} or the directory {} should be writable by the process.".format(os.path.realpath(os.path.join(opts.root,opts.result_file)),os.path.realpath(os.path.dirname(os.path.join(opts.root,opts.result_file)))))
            exit(1)
        
        m = mp.Manager()
        queue = m.Queue(-1)
        listener = mp.Process(target=listener_process, args=(queue, listener_configurer))
        listener.start()               

        logger.info("Loading data....")
        with open(os.path.realpath(os.path.join(opts.root,opts.inputfile)),'rb') as top100file:
            top100_videos = pickle.load(top100file,encoding='utf-8',fix_imports=True)

        skipped = 0
        added = 0
        for user in top100_videos:
            logger.info('Checking user {} for test video.'.format(user))
            for v in top100_videos[user]['videos']:   
                if v['duplicate']:
                    logger.debug('Passed duplicate video {} from {} with length {} from {}.'.format(v['id'],user,v['length'],v['recorded_at'] ))
                    skipped += 1
                    continue
                added += 1
                pool.apply_async(ProcessVideo, args = (queue, worker_configurer, v, opts.root, opts.skip_stream), callback = log_result, error_callback = log_error)
                logger.debug('Found video {} from {} with length {} from {}.'.format(v['id'],user,v['length'],v['recorded_at'] ))
        logger.info('Added {} videos to queue and skipped {} videos.'.format(added,skipped))
        pool.close()
        logger.info('Waiting for all workers to exit.')
        pool.join()
        logger.info('Waiting for listener process to exit.')
        queue.put_nowait(None)
        listener.join()

        with open(os.path.realpath(os.path.join(opts.root,opts.result_file)),'w') as f:
            for res in global_results:
                f.write("\"Result for\";{};{};{}\n".format(res[0],res[1],res[2]))

        #ProcessVideo(video_info)

        logger.info('Done.')
    except KeyboardInterrupt:
        if pool:
            logger.critical('Terminating pool...')
            pool.terminate()
            pool.join()
        if listener:
            logger.critical('Stopping listener...')
            queue.put_nowait(None)
            listener.join(5)
            if listener.is_alive():
                logger.critical('Terminating listener...')
                listener.terminate()
                listener.join()
    except SystemExit:
        print('Bad Arguments')
        if pool:
            logger.critical('Terminating pool...')
            pool.terminate()
            pool.join()
        if listener:
            logger.critical('Stopping listener...')
            queue.put_nowait(None)
            listener.join(5)
            if listener.is_alive():
                logger.critical('Terminating listener...')
                listener.terminate()
                listener.join()
