import pickle
import os
import re

common_words = None

with open("TwitchEmotes.txt", "r") as Emotes:
    common_words = [line[:-1] for line in Emotes]

with open("data/videos/Doublelift/D-v102365143.rechat.pickle", "rb") as file:
    data = pickle.load(file)

    data2 = []

    for line in data:
        #print(line)
        message = line["attributes"]["message"]
        print(message)

        big_regex = re.compile(r'\b{}\b'.format(r'\b|\b'.join(map(re.escape, common_words))))
        message = big_regex.sub("", message)
        print(message)

        # title = "When to use Python for web applications"
       # words = set(message.lower().split())
     #   keywords = words.difference(common_words)
      #  print(keywords)


