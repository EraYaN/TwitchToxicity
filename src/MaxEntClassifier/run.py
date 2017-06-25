import pickle
import pprint
import re
import unicodedata as ud
import lzma as compressor
import nltk

from nltk.classify import maxent

"""
t = toxic, n = neutral
"""

"""
'e805988d-f713-45af-a236-6cb3b1bf4edb': yeah tymerl i did think the same
'4cc42e6e-b7a5-4601-9071-3c0ac03b20f0': lul
'f011b9cc-56bd-4b17-8e73-3f926fbcb652': can someone give me one skin pls
'f7d94456-ed19-4dac-b6c3-760c814bff17': sellout or nah
'37cf2c67-301b-4fe2-aebc-5fa3d4d55a1e': what is every1 matchmaking rank ? no lying
'f747f597-5998-4520-8795-6c5bd6211115': intel core i7 uses motherboard with am3 plastic hinges dansgame
'a6fb9ff1-146b-4ed4-ab96-6f0e2ecce2a2': this looks like a transformed ps4 lul
'7cb4d8f7-906f-486a-ad93-3072f477173b': @tymerl csgofast
'932d8069-3e6a-43e2-93eb-eebbeabd8a4c': @tymerl you can bet on hltv thanks me later :)
'222afdb6-e691-4a42-87f0-cb0e30ebccb8': start your esports career on esl play: http://esl.gg/eslplaycsgo
'f3ec2cb9-82b6-473e-a203-75fa0b90bf35': i'm here for the cute grill\
'5917a0dc-dd62-4269-bb54-715b1db90f10': who will win?
'28cb86ab-4d67-4f11-860d-34b29f847af9': guys and "girls"
'1f4af641-5957-4e70-b5ae-96c403e020f0': finally gamerino
'3543a1c1-e144-496f-ab5d-000316283b3e': cheifs
'd6990240-3a85-44fd-975a-90c609a79327': lol that pc have a 780
'9d845bee-2884-4d66-8390-25b260c67a16': athletico 90.0% winrate on mirage lol
'd36ddab5-1991-4636-b8ec-7f4302a64784': @msshadowfax, ur qt grill xd
'570bd09d-d2c9-424f-bdbd-79055e87b0bc': can someone give me one skin pls
'919c8119-6778-4bfc-84b5-785009cf840f': triggered
'301b2d8a-8c2b-416d-b3e3-89e830218e4b': ez for athletico. greizmann will get a hat trick boys. wait and see
'59458cb8-3f62-41c7-98b9-c41ee3cdbcc9': dis is racist dat dea r no maori teams
'93959f16-4066-47b9-8edb-b5c1bc09a20d': did chiefs choose train?
'507f7bf9-70d3-438a-b5d1-987bff4d5a5c': ez for athletico
'9f945498-718e-4eea-97d6-2483257ffe6c': @melkt dansgame
'0fa6b0f9-a5b1-4a74-9abb-8d49724bbb6c': 37.787971,-122.407776
'99a1bb75-7f9f-4fac-aae4-f2336d7cfa37': wik fr
'c6652e86-9e37-4989-8968-3bb40cda02e8': nou way
'3b33fe51-d6b5-4a3f-8590-16891f5c3ac2': live live live
'9871b520-fbda-4002-a353-b86a76b36faa': athletico winn
'5592cccb-f2b6-4c79-9e6d-51522fc7d5a4': i'd say ez chiefs we'll see
'0f429978-cc39-45f5-b2c1-01c07dc3d049': is it me or the stream is super quiet?
'f4ef578d-e83e-41ea-8668-253f7fa1534f': lol
'7b0ab110-25ba-4d17-ba64-8d9fd3dc5ee0': yah, some games involve coins some involve skins @tymerl
'd7c750cc-de6c-4688-8f6f-f9f8544a8e2a': :)
'edc2bd91-0c20-4b93-a778-f6b4827d01c8': who the *** is casting
'4fd47af0-de49-4d2a-9105-6427426ab1d2': oh
'4ebe6b08-4b27-48d6-965a-d6c98f78d433': who's the cameraman?
'4d0141f4-c305-4daf-936f-32ac40268adb': lets go chiefs
'a3da4645-ff5d-4c69-8080-0e56e508598d': can someone give me one skin pls
'5f179181-6fd1-451d-a23d-811faccd8319': harambe
'56e4e74a-1623-4052-a687-742496b0d582': omg omg only usp-s oion, guaranteed pistol round lost
'dd2df715-5ad2-4bf6-aa33-b41c3647bb94': lmao
'b7047702-ec32-4a00-8af8-6e3a7ad16e4c': wtf
'1767d326-04a7-4f61-9670-eed604663b36': wow
'c9b6c3ef-adad-4f66-b70d-cee91fa08fda': vac
'3dbf410e-079c-482e-a8c1-62fd406285b6': wow
'd3f33c8f-8c71-4212-b7bf-d5abe42b285a': lul
'd7183075-bed6-4301-b070-db1050f35b3e': vac
'77457124-a178-492e-8fb6-84ac84f3c493': ooooooooooooh!
'a90f5c5d-9370-4e49-9455-f081d3d3eaac': i told you guys gogoo chiefs
'fbccc4bb-512e-4c9d-9374-4533eaa6e28a': wow
'04e64640-2b52-47e3-ad3e-b608571ea82c': ez round
'da6ffddd-cbc5-4f4a-8c28-7749a903ca58': au cs
'cebf2875-17a0-413b-9fe7-595f48eb645b': ezzz
'd2df30f0-9a03-41de-aba4-f6ad04ca7fc7': ''\\=(_)=//'' new cases arrived at kinguin! check out the cs:go esl uk case! http://www.kinguin.net/7en/b91
'148bd89e-53a6-4854-a1d3-2af850ad84cc': cameraman?
'f178327f-c3e3-46cd-bad9-5df0e4e57fcb': ez
'0c934ffa-3d12-453c-b90b-d4f7827e4c25': why no sound notlikethis
'ee026b1a-bf79-475b-bb2f-b8100c394109': terrible camera
'370f49bc-7117-4d41-ba71-d193199d1f0c': luck
'059e73b4-6ded-4af8-b640-15143410b69e': where is athletico from?
'54021010-7e93-4098-8c3a-d4ac8dde717e': sound so low
'da87558c-4328-4014-9aae-ea3235ae174d': ez money
'6af80024-eb9e-4ae5-95cf-2abeaddd4dfa': anyones into foreskin betting here?
'9b045705-8cf9-4a37-b583-ae412dc1039f': sound so soft
'b1b20bef-dbea-47a4-8fdb-429b04f75a5b': na cameraman
'c61c5437-0767-4140-8f72-842f1c2f5cb0': camerman
'18c52336-9d71-433a-8f96-b086e4b57e70': @amazingza yep
'1b5eb424-1d01-409a-b72b-7d04ccc5a3d5': can someone give me one skin pls
'555e2403-6f14-4e31-ba68-bd09efc5c619': hp? and ammo?
'5e71f891-3328-491d-a53d-059d8b41c130': ez yolo?
'c4732e6d-c965-4b40-8896-82d296c0d61d': cameraman like heyguys
'3c616e38-8db5-413a-a0ab-cba858567c26': camera failfish
'5f2b69be-27aa-4d19-adaa-366391a82f4c': camera!
'b17ebf81-a8bd-44cc-bbab-9aad09a20988': cameraman plz..
'70801c2d-b289-4e5a-96c1-74fcec20825a': na~hate..
'058c9d12-f6bf-4a3d-9e78-431c36ae3f1f': lmao
'dda7d60e-2100-4986-8902-9ce460fd4293': athlete's foot stink dansgame
'f7d285b3-d749-4eb7-b86b-a854a9f6635a': @s1ckrep kill yourself. literally commit suicide.
'5ebc9ae2-777c-49f5-b2d0-e8490d2069bb': gg
'c1838450-4c24-4ef5-8ee6-fb7bda2d723f': camaraman intentionally dodging the kills
'f1ae1012-7e56-49d0-b54c-1afec045f89a': na cameraman?
'5cc63368-f20f-4602-bd6b-810f9a3771c4': praiseit praiseit praiseit camera
'953c87d3-b6a8-43b4-8c9e-dbf23a397526': they smell
'3ce2cb3b-fd10-4a79-bab5-7bf1b12ec147': cameraman, please lay off the amphetamines
'c6a68551-f553-4a76-b59f-0145a2a3cc99': yay we actually witness a frag for once in the round failfish
'14ecb422-a70a-48c4-954b-0496d194cee2': gg boys easy money
'e4e5f572-3f35-4a62-884d-3c3db05486dc': can someone give me one skin pls
'e028b997-686f-4c5f-a789-992056d2edb0': aimlock to check !!
'78e1001b-9639-4b99-86e4-4d1f21ac6e58': wixsanic
'e8408a3d-536b-4bd4-be8c-3bff8bc22e88': put the auto camera mode kappa
'c9bbe57e-0a1c-4b5b-b9d8-6c4df136437e': idd :d
'277678b9-b455-4d26-832e-bbb9cd43c5f4': where are drops???
'45b06a44-46a0-452d-90c3-8d32bebeafd2': do they have auto director on or something shesh
'f603845c-bbe3-472e-be8a-5f262ddd1532': @s1ckrep no one is going to give a silver a skin so stfu, and get on with killing yourself
'f9c1e06b-a080-4059-b942-aa24b64d5af4': na save
'a3e6f23d-bb1d-436b-aef8-637f67939e3e': pls 3rd person @cameraman
'84063287-ca88-4f1e-b995-0ec0afdf9352': no just na cameraman
'146144d3-11e3-4eb8-8074-3b67d0f239a4': 1 2
"""

data = {
	'e805988d-f713-45af-a236-6cb3b1bf4edb': '',
	'4cc42e6e-b7a5-4601-9071-3c0ac03b20f0': '',
	'f011b9cc-56bd-4b17-8e73-3f926fbcb652': '',
	'f7d94456-ed19-4dac-b6c3-760c814bff17': '',
	'37cf2c67-301b-4fe2-aebc-5fa3d4d55a1e': '',
	'f747f597-5998-4520-8795-6c5bd6211115': '',
	'a6fb9ff1-146b-4ed4-ab96-6f0e2ecce2a2': '',
	'7cb4d8f7-906f-486a-ad93-3072f477173b': '',
	'932d8069-3e6a-43e2-93eb-eebbeabd8a4c': '',
	'222afdb6-e691-4a42-87f0-cb0e30ebccb8': '',
	'f3ec2cb9-82b6-473e-a203-75fa0b90bf35': '',
	'5917a0dc-dd62-4269-bb54-715b1db90f10': '',
	'28cb86ab-4d67-4f11-860d-34b29f847af9': '',
	'1f4af641-5957-4e70-b5ae-96c403e020f0': '',
	'3543a1c1-e144-496f-ab5d-000316283b3e': '',
	'd6990240-3a85-44fd-975a-90c609a79327': '',
	'9d845bee-2884-4d66-8390-25b260c67a16': '',
	'd36ddab5-1991-4636-b8ec-7f4302a64784': '',
	'570bd09d-d2c9-424f-bdbd-79055e87b0bc': '',
	'919c8119-6778-4bfc-84b5-785009cf840f': '',
	'301b2d8a-8c2b-416d-b3e3-89e830218e4b': '',
	'59458cb8-3f62-41c7-98b9-c41ee3cdbcc9': '',
	'93959f16-4066-47b9-8edb-b5c1bc09a20d': '',
	'507f7bf9-70d3-438a-b5d1-987bff4d5a5c': '',
	'9f945498-718e-4eea-97d6-2483257ffe6c': '',
	'0fa6b0f9-a5b1-4a74-9abb-8d49724bbb6c': '',
	'99a1bb75-7f9f-4fac-aae4-f2336d7cfa37': '',
	'c6652e86-9e37-4989-8968-3bb40cda02e8': '',
	'3b33fe51-d6b5-4a3f-8590-16891f5c3ac2': '',
	'9871b520-fbda-4002-a353-b86a76b36faa': '',
	'5592cccb-f2b6-4c79-9e6d-51522fc7d5a4': '',
	'0f429978-cc39-45f5-b2c1-01c07dc3d049': '',
	'f4ef578d-e83e-41ea-8668-253f7fa1534f': '',
	'7b0ab110-25ba-4d17-ba64-8d9fd3dc5ee0': '',
	'd7c750cc-de6c-4688-8f6f-f9f8544a8e2a': '',
	'edc2bd91-0c20-4b93-a778-f6b4827d01c8': '',
	'4fd47af0-de49-4d2a-9105-6427426ab1d2': '',
	'4ebe6b08-4b27-48d6-965a-d6c98f78d433': '',
	'4d0141f4-c305-4daf-936f-32ac40268adb': '',
	'a3da4645-ff5d-4c69-8080-0e56e508598d': '',
	'5f179181-6fd1-451d-a23d-811faccd8319': '',
	'56e4e74a-1623-4052-a687-742496b0d582': '',
	'dd2df715-5ad2-4bf6-aa33-b41c3647bb94': '',
	'b7047702-ec32-4a00-8af8-6e3a7ad16e4c': '',
	'1767d326-04a7-4f61-9670-eed604663b36': '',
	'c9b6c3ef-adad-4f66-b70d-cee91fa08fda': '',
	'3dbf410e-079c-482e-a8c1-62fd406285b6': '',
	'd3f33c8f-8c71-4212-b7bf-d5abe42b285a': '',
	'd7183075-bed6-4301-b070-db1050f35b3e': '',
	'77457124-a178-492e-8fb6-84ac84f3c493': '',
	'a90f5c5d-9370-4e49-9455-f081d3d3eaac': '',
	'fbccc4bb-512e-4c9d-9374-4533eaa6e28a': '',
	'04e64640-2b52-47e3-ad3e-b608571ea82c': '',
	'da6ffddd-cbc5-4f4a-8c28-7749a903ca58': '',
	'cebf2875-17a0-413b-9fe7-595f48eb645b': '',
	'd2df30f0-9a03-41de-aba4-f6ad04ca7fc7': '',
	'148bd89e-53a6-4854-a1d3-2af850ad84cc': '',
	'f178327f-c3e3-46cd-bad9-5df0e4e57fcb': '',
	'0c934ffa-3d12-453c-b90b-d4f7827e4c25': '',
	'ee026b1a-bf79-475b-bb2f-b8100c394109': '',
	'370f49bc-7117-4d41-ba71-d193199d1f0c': '',
	'059e73b4-6ded-4af8-b640-15143410b69e': '',
	'54021010-7e93-4098-8c3a-d4ac8dde717e': '',
	'da87558c-4328-4014-9aae-ea3235ae174d': '',
	'6af80024-eb9e-4ae5-95cf-2abeaddd4dfa': '',
	'9b045705-8cf9-4a37-b583-ae412dc1039f': '',
	'b1b20bef-dbea-47a4-8fdb-429b04f75a5b': '',
	'c61c5437-0767-4140-8f72-842f1c2f5cb0': '',
	'18c52336-9d71-433a-8f96-b086e4b57e70': '',
	'1b5eb424-1d01-409a-b72b-7d04ccc5a3d5': '',
	'555e2403-6f14-4e31-ba68-bd09efc5c619': '',
	'5e71f891-3328-491d-a53d-059d8b41c130': '',
	'c4732e6d-c965-4b40-8896-82d296c0d61d': '',
	'3c616e38-8db5-413a-a0ab-cba858567c26': '',
	'5f2b69be-27aa-4d19-adaa-366391a82f4c': '',
	'b17ebf81-a8bd-44cc-bbab-9aad09a20988': '',
	'70801c2d-b289-4e5a-96c1-74fcec20825a': '',
	'058c9d12-f6bf-4a3d-9e78-431c36ae3f1f': '',
	'dda7d60e-2100-4986-8902-9ce460fd4293': '',
	'f7d285b3-d749-4eb7-b86b-a854a9f6635a': '',
	'5ebc9ae2-777c-49f5-b2d0-e8490d2069bb': '',
	'c1838450-4c24-4ef5-8ee6-fb7bda2d723f': '',
	'f1ae1012-7e56-49d0-b54c-1afec045f89a': '',
	'5cc63368-f20f-4602-bd6b-810f9a3771c4': '',
	'953c87d3-b6a8-43b4-8c9e-dbf23a397526': '',
	'3ce2cb3b-fd10-4a79-bab5-7bf1b12ec147': '',
	'c6a68551-f553-4a76-b59f-0145a2a3cc99': '',
	'14ecb422-a70a-48c4-954b-0496d194cee2': '',
	'e4e5f572-3f35-4a62-884d-3c3db05486dc': '',
	'e028b997-686f-4c5f-a789-992056d2edb0': '',
	'78e1001b-9639-4b99-86e4-4d1f21ac6e58': '',
	'e8408a3d-536b-4bd4-be8c-3bff8bc22e88': '',
	'c9bbe57e-0a1c-4b5b-b9d8-6c4df136437e': '',
	'277678b9-b455-4d26-832e-bbb9cd43c5f4': '',
	'45b06a44-46a0-452d-90c3-8d32bebeafd2': '',
	'f603845c-bbe3-472e-be8a-5f262ddd1532': '',
	'f9c1e06b-a080-4059-b942-aa24b64d5af4': '',
	'a3e6f23d-bb1d-436b-aef8-637f67939e3e': '',
	'84063287-ca88-4f1e-b995-0ec0afdf9352': '',
	'146144d3-11e3-4eb8-8074-3b67d0f239a4': '',
	'a3387050-bf96-487e-93f3-24d484e81af9': ''
}

def classify(pos, neg, swr, sentence):
	features = {'p': 0, 'n': 0, 't': 0}
	tokens = nltk.word_tokenize(sentence)

	for token in tokens:
		if token in pos:
			features['p'] += 1
		elif token in neg:
			features['n'] += 1
		elif token in swr:
			features['t'] += 1
	return features

def parseWordList(filename):
	wordList = []
	with open(filename) as f:
		for line in f:
			if line != "" and line[0] != ';':
				wordList.append(line.strip())
	return wordList

def strip_unicode(s,replace=r''):
    return re.sub(r'[^\x00-\x7f]',replace,ud.normalize('NFD',s))

def load_compressed_pickle(filename):
    with compressor.open(filename, 'rb') as f:
        loaded_object = pickle.load(f)
        return loaded_object

pos = parseWordList('positive.txt')
neg = parseWordList('negative.txt')
swr = parseWordList('swear.txt')

train = []
messages = load_compressed_pickle('data.pickle.xz')
count = 0

for message in messages:
	msg = strip_unicode(message['attributes']['message']).lower()
	if msg != "" and msg[0] != '!':
		features = classify(pos, neg, swr, msg)
		idx = message['attributes']['tags']['id']
		print("'{}': {}".format(idx, msg))

		# pprint.pprint(message)
		# pprint.pprint(message['attributes']['tags']['id'])
		# print("{} {}".format(str(verdict), msg))
		# train.append((verdict, 'n'))

		count += 1
		if count > 100:
			break

exit()


## Example training and classification
train = [
    ({'a': 1, 'b': 1, 'c': 1}, 'y'),
    ({'a': 5, 'b': 5, 'c': 5}, 'x'),
    ({'a': 5.5, 'b': 5.4, 'c': 5.3}, 'x'),
    ({'a': 0.9, 'b': 0.9, 'c': 0.9}, 'y'),
    ({'a': 0.8, 'b': 1.2, 'c': 1}, 'y'),
    ({'a': 5.1, 'b': 4.9, 'c': 5.2}, 'x')
]
test = [
    {'a': 1, 'b': 0.8, 'c': 1.2},
    {'a': 5.2, 'b': 5.1, 'c': 5}
]

encoding = maxent.TypedMaxentFeatureEncoding.train(train, count_cutoff=3, alwayson_features=True)
classifier = maxent.MaxentClassifier.train(train, bernoulli=False, encoding=encoding, trace=0)

print(classifier.classify_many(test))
