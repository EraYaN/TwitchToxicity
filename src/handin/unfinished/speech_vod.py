import os

import speech_recognition as sr
from pydub import AudioSegment
from pydub.audio_segment import StringIO



r = sr.Recognizer()


def decode_video(filename):
    print(filename)

    aac_version = AudioSegment.from_file(filename)
    sw = aac_version.sample_width
    fr = aac_version.frame_rate
    data = aac_version.raw_data

    start = (60*52) + 38
    end = (60*52) + 42
    ad = sr.AudioData(data[start*fr:end*fr], fr, sw)
    print("Recoginzin2iwjs")
    print("Sphinx thinks you said " + r.recognize_google(ad))

    #r.recognize_google(ad)
    #aac_version.export('file.wav', format='wav')

    #with sr.AudioFile('file.wav') as source:  # open the audio file for reading
    #    audio = r.record(source)
    #    print("Sphinx thinks you said " + r.recognize_sphinx(audio))

data_folder = "D:\\twitchtoxicity\\data"
for root, dirs, files in os.walk(data_folder, topdown=False):
    for name in files:
        if (name.endswith(".mp4")):
            pass
            #decode_video(os.path.join(root, name))
            # print("MP4 file sound %s %s" % (root, name))
            # for name in dirs:
            #    print(os.path.join(root, name))

decode_video("D:\\twitchtoxicity\\data\\videos\\LIRIK\\Untitled Broadcast-v125867497.mp4")