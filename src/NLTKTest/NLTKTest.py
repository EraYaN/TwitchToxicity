import nltk
from nltk.tokenize import TweetTokenizer

chat_nontoxic = [
    ('<Cthon98> hey, if you type in your pw, it will show as stars','nontoxic'),
    ('<Cthon98> ********* see!','nontoxic'),
    ('<AzureDiamond> hunter2','nontoxic'),
    ('<AzureDiamond> doesnt look like stars to me','nontoxic'),
    ('<Cthon98> <AzureDiamond> *******','nontoxic'),
    ('<Cthon98> thats what I see','nontoxic'),
    ('<AzureDiamond> oh, really?','nontoxic'),
    ('<Cthon98> Absolutely','nontoxic'),
    ('<AzureDiamond> you can go hunter2 my hunter2-ing hunter2','nontoxic'),
    ('<AzureDiamond> haha, does that look funny to you?','nontoxic'),
    ('<Cthon98> lol, yes. See, when YOU type hunter2, it shows to us as *******','nontoxic'),
    ('<AzureDiamond> thats neat, I didnt know IRC did that','nontoxic'),
    ('<Cthon98> yep, no matter how many times you type hunter2, it will show to us as *******','nontoxic'),
    ('<AzureDiamond> awesome!','nontoxic'),
    ('<AzureDiamond> wait, how do you know my pw?','nontoxic'),
    ('<Cthon98> er, I just copy pasted YOUR ******\'s and it appears to YOU as hunter2 cause its your pw','nontoxic'),
    ('<AzureDiamond> oh, ok.','nontoxic')
]

chat_toxic = [
    ('<t0rbad> so there i was in this hallway right','toxic'),
    ('<BlackAdder> i believe i speak for all of us when i say...','toxic'),
    ('<BlackAdder> WRONG BTICH','toxic'),
    ('<BlackAdder> IM SICK OF YOU','toxic'),
    ('<BlackAdder> AND YOUR LAME STORIES','toxic'),
    ('<BlackAdder> NOBODY  HERE THINKS YOURE FUNNY','toxic'),
    ('<BlackAdder> NOBODY HERE WANTS TO HEAR YOUR STORIES','toxic'),
    ('<BlackAdder> IN FACT','toxic'),
    ('<BlackAdder> IF YOU DIED RIGHT NOW','toxic'),
    ('<BlackAdder> I  DON"T THINK NOBODY WOULD CARE','toxic'),
    ('<BlackAdder> SO WHAT DO YOU SAY TO THAT FAG','toxic'),
    ('*** t0rbad sets mode: +b BlackAdder*!*@*.*','toxic'),
    ('*** BlackAdder has been kicked my t0rbad ( )','toxic'),
    ('<t0rbad> so there i was in this hallway right','toxic'),
    ('<CRCError> right','toxic'),
    ('<heartless> Right.','toxic'),
    ('<r3v> right','toxic')
]

test_chat = [
    (['feel', 'happy', 'this', 'morning'], 'positive'),
    (['larry', 'friend'], 'positive'),
    (['not', 'like', 'that', 'man'], 'negative'),
    (['house', 'not', 'great'], 'negative'),
    (['your', 'song', 'annoying'], 'negative')
]

tknzr = TweetTokenizer(preserve_case=False, reduce_len=False, strip_handles=False)

chats = []

chat_training_set = chat_nontoxic + chat_toxic

for (words, sentiment) in chat_training_set:
	words_filtered = [e.lower() for e in tknzr.tokenize(words) if len(e) >= 3]
	chats.append((words_filtered, sentiment))
    
def get_words_in_chats(chats_data):
    all_words = []
    for (words, sentiment) in chats_data:
	    all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

word_features = get_word_features(get_words_in_chats(chats))

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

training_set = nltk.classify.apply_features(extract_features, chats)
classifier = nltk.NaiveBayesClassifier.train(training_set)

chat = 'Test: "<Somegal> Just type your password."'
print(chat)
print('Verdict: {}'.format(classifier.classify(extract_features(tknzr.tokenize(chat)))))
chat = 'Test: "<Someguy> Your STORY IS SUPER LAME YOU BITCH."'
print(chat)
print('Verdict: {}'.format(classifier.classify(extract_features(tknzr.tokenize(chat)))))
