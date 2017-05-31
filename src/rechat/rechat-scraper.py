from __future__ import print_function

import requests
import sys
import calendar
import time
import math
import json


def scrape_vod(vod_id, filename):
    CHUNK_ATTEMPTS = 6
    CHUNK_ATTEMPT_SLEEP = 10

    messages = []

    cid = "isaxc3wjcarzh4vgvz11cslcthw0gw"
    vod_info = requests.get("https://api.twitch.tv/kraken/videos/v" + vod_id, headers={"Client-ID": cid}).json()

    file_name = "rechat-" + vod_id + ".json"
    if len(sys.argv) == 3:
        file_name = sys.argv[2]

    if "error" in vod_info:
        sys.exit("got an error in vod info response: " + str(vod_info))

    start_timestamp = calendar.timegm(time.strptime(vod_info["recorded_at"], "%Y-%m-%dT%H:%M:%SZ"))
    video_len = int(vod_info["length"])
    last_timestamp = start_timestamp + int(math.ceil(video_len / 30.0) * 30)

    vod_info['start_timestamp'] = start_timestamp
    messages.append(vod_info)  # we store the vod metadata in the first element of the message array

    for chat_timestamp in range(start_timestamp, last_timestamp + 1, 30):
        chunk_number = int((chat_timestamp - start_timestamp) / 30) + 1
        chunks = int((last_timestamp - start_timestamp) / 30) + 1

        print("\rdownloading chunk " + str(chunk_number) + " / " + str(chunks), end="")

        chat_json = None

        for i in range(0, CHUNK_ATTEMPTS):
            error = None
            try:
                chat_json = requests.get(
                    "http://rechat.twitch.tv/rechat-messages?start=" + str(chat_timestamp) + "&video_id=v" + vod_id,
                    headers={"Client-ID": cid}).json()
            except requests.exceptions.ConnectionError as e:
                error = str(e)
            else:
                if "errors" in chat_json or not "data" in chat_json:
                    error = "error received in chat message response: " + str(chat_json)

            if error == None:
                messages += chat_json["data"]
                break
            else:
                print("\nerror while downloading chunk #" + str(chunk_number) + ": " + error)

                if i < CHUNK_ATTEMPTS - 1:
                    print("retrying in " + str(CHUNK_ATTEMPT_SLEEP) + " seconds ", end="")
                print("(attempt " + str(i + 1) + "/" + str(CHUNK_ATTEMPTS) + ")")

                if i < CHUNK_ATTEMPTS - 1:
                    time.sleep(CHUNK_ATTEMPT_SLEEP)

        if error != None:
            sys.exit("max retries exceeded.")

    print()
    print("saving to " + file_name)

    # TODO: use json-info

    f = open("rechats/" + file_name, "w")
    f.write(json.dumps(messages))
    f.close()

    print("done!")


scrape_vod("148361448")
