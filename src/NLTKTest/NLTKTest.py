print('Starting...')
import nltk
import requests
try:
    import ujson as json
except:
    import json
from nltk.tokenize import TweetTokenizer

post_data = {
    'd':'classifications',
    'count': 6000,
    'offset': 0,
    'minratings': 2,
    'apikey': 'jnWJc23aMvFfhoGtwHxFwRQMnhzRTKpUa04h'
    }

def get_words_in_chats(chats_data):
    all_words = []
    for (words, sentiment) in chats_data:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

if __name__ == "__main__":
    print('Setting up tokenizer...')
    tknzr = TweetTokenizer(preserve_case=False, reduce_len=False, strip_handles=False)

    chats = []
    print('Getting data from API...')
    resp = requests.post('https://labs.erayan.com/twitchtoxicity/api.php', data=post_data)

    chat_training_set = []
    chat_training_set_pre = json.loads(resp.text)
    print('Got {} data lines from API.'.format(len(chat_training_set_pre['data'])))
    for cts in chat_training_set_pre['data']:
        #print("Processing message with ID: {}".format(cts))
        chat_training_set.append((chat_training_set_pre['data'][cts]['message_data']['message-filtered'],chat_training_set_pre['data'][cts]['compound_classifications']))

    print('Filtering and tokenizing messages...')
    for (words, sentiment) in chat_training_set:
        words_filtered = [e.lower() for e in tknzr.tokenize(words) if len(e) >= 3]
        chats.append((words_filtered, sentiment))

    print('Getting features...')
    word_features = get_word_features(get_words_in_chats(chats))

    print('Creating training set...')
    training_set = nltk.classify.apply_features(extract_features, chats)
    print('Training classifier...')
    classifier = nltk.MaxentClassifier.train(training_set, bernoulli=False, trace=0)
    #classifier = nltk.NaiveBayesClassifier.train(training_set)

    print('Test classifications...')
    chat = 'Fucking americans'
    print("Message: {}".format(chat))
    print('Verdict: {}'.format(classifier.classify(extract_features(tknzr.tokenize(chat)))))
    chat = 'Your STORY IS SUPER LAME YOU BITCH'
    print("Message: {}".format(chat))
    print('Verdict: {}'.format(classifier.classify(extract_features(tknzr.tokenize(chat)))))
