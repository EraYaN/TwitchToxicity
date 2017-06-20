import os
import pickle

from nltk import NaiveBayesClassifier, pprint
from nltk.corpus import subjectivity, twitter_samples

from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import mark_negation, extract_unigram_feats

subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')]
obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')]

training_docs = subj_docs[0:80] + obj_docs[0:80]

sentim_analyzer = SentimentAnalyzer()
all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])
unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
pprint(training_docs)
training_set = sentim_analyzer.apply_features(training_docs)
pprint(training_set)
trainer = NaiveBayesClassifier.train
classifier = sentim_analyzer.train(trainer, training_set)

# We apply features to obtain a feature-value representation of our datasets:


test_pickle = "D:\\twitchtoxicity\\data\\videos\\A_Seagull\\[PTR] new hero and new zen-v78024279.rechat-filtered.pickle"
result_pickle = "D:\\twitchtoxicity\\data\\videos\\A_Seagull\\[PTR] new hero and new zen-v78024279.rechat-result.pickle"

with open(test_pickle, 'rb') as test_file:
    with open(result_pickle, 'wb') as result_file:
        test_pickle = pickle.load(test_file)
        test_messages = []
        for line in test_pickle:
            test_messages.append(line["attributes"]["message-filtered"])
        test_set = sentim_analyzer.apply_features(test_messages)
        #sentim_analyzer.evaluate(test_set, classifier=classifier)
        #for key, value in sorted(sentim_analyzer.evaluate(test_set).items()):
        #    print('{0}: {1}'.format(key, value))

# import pprint
#
# with open(result_pickle, 'rb') as result:
#    test_result = pickle.load(result)
#    pprint.pprint(test_result[0])
# print test results pickle
