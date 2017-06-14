import requests
import sys
import calendar
import time
import math
import pickle
import os
import logging
import lzma as compressor
COMPRESSOR_EXTENSION = 'xz'

try:
    import ujson as json
except:
    import json

def download_rechat(cid, vod_info, filename, force=False):
    logger = logging.getLogger(vod_info['id'])   
    CHUNK_ATTEMPTS = 6
    CHUNK_ATTEMPT_SLEEP = 10
    if os.path.exists(filename) and not force:
        logger.info("Rechat already downloaded to {}".format(filename))
        return True
    messages = []

    logger.info("Saving to {}".format(filename))

    start_timestamp = calendar.timegm(time.strptime(vod_info["recorded_at"], "%Y-%m-%dT%H:%M:%SZ"))
    video_len = int(vod_info["length"])
    last_timestamp = start_timestamp + int(math.ceil(video_len / 30.0) * 30)    
   
    for chat_timestamp in range(start_timestamp, last_timestamp + 1, 30):
        chunk_number = int((chat_timestamp - start_timestamp) / 30) + 1
        chunks = int((last_timestamp - start_timestamp) / 30) + 1

        if chunk_number % 10 == 0:
            logger.info("Downloading chunk {} of {}".format(chunk_number,chunks))
        else:
            logger.debug("Downloading chunk {} of {}".format(chunk_number,chunks))

        chat_json = None

        for i in range(0, CHUNK_ATTEMPTS):
            error = None
            exit = False
            try:
                chat_json = requests.get(
                    "http://rechat.twitch.tv/rechat-messages?start={}&video_id={}".format(chat_timestamp,vod_info['id']),
                    headers={"Client-ID": cid}).json()
            except requests.exceptions.ConnectionError as e:
                error = str(e)
            else:
                if "errors" in chat_json or not "data" in chat_json:
                    error = ''
                    for error_obj in chat_json['errors']:
                        if error_obj['status'] == 404:
                            exit = True
                        error += "ERROR[{status}] {detail}. ".format(**error_obj)

            if error is None:
                messages += chat_json["data"]
                break
            else:
                logger.error("ERROR while downloading chunk #{}: {}".format(chunk_number,error))

                if exit:
                    return False

                if i < CHUNK_ATTEMPTS - 1:
                    logger.info("Retrying in {} seconds.".format(CHUNK_ATTEMPT_SLEEP))
                logger.info("(Attempt {}/{})".format(i + 1,CHUNK_ATTEMPTS))

                if i < CHUNK_ATTEMPTS - 1:
                    time.sleep(CHUNK_ATTEMPT_SLEEP)

        if error is not None:
            logger.error("Max retries exceeded.")
            return False

    logger.debug("Saving...")


    with compressor.open(filename, "wb") as f:
        pickle.dump(messages,f)

    logger.info("Saved Rechat!")
    return True


    



