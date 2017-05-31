import requests
import sys
import calendar
import time
import math
import pickle
try:
    import ujson as json
except:
    import json

def download_rechat(cid, vod_info, filename):
    CHUNK_ATTEMPTS = 6
    CHUNK_ATTEMPT_SLEEP = 10

    messages = []

    print("\nSaving to {}".format(filename))

    start_timestamp = calendar.timegm(time.strptime(vod_info["recorded_at"], "%Y-%m-%dT%H:%M:%SZ"))
    video_len = int(vod_info["length"])
    last_timestamp = start_timestamp + int(math.ceil(video_len / 30.0) * 30)    
   
    for chat_timestamp in range(start_timestamp, last_timestamp + 1, 30):
        chunk_number = int((chat_timestamp - start_timestamp) / 30) + 1
        chunks = int((last_timestamp - start_timestamp) / 30) + 1

        print("\rDownloading chunk {} of {}".format(chunk_number,chunks), end="")

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
                        error += "ERROR[{status}] {detail}.\n".format(**error_obj)

            if error == None:
                messages += chat_json["data"]
                break
            else:
                print("\nERROR while downloading chunk #{}: {}".format(chunk_number,error))

                if exit:
                    return False

                if i < CHUNK_ATTEMPTS - 1:
                    print("Retrying in {} seconds.".format(CHUNK_ATTEMPT_SLEEP), end="")
                print("(Attempt {}/{})".format(i + 1,CHUNK_ATTEMPTS))

                if i < CHUNK_ATTEMPTS - 1:
                    time.sleep(CHUNK_ATTEMPT_SLEEP)

        if error != None:
            sys.exit("Max retries exceeded.")

    print("\nSaving...")


    with open(filename, "wb") as f:
        pickle.dump(messages,f)

    print("Saved Rechat!")
    return True


    



