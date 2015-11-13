import pandas as pd
import sqlite3
from StringIO import StringIO
import urllib2
import zipfile
import nltk
from nltk import tokenize

#Read document collection
f = open('sms_spam_collection.txt')
lines = [line for line in f.read().split('\n') if len(line) != 0]
f.close()

#Extract classes and documents
classes = [line.split()[0] for line in lines]
documents = [' '.join(line.split()[1:]) for line in lines]

#Make data frame
df = pd.DataFrame({'class' : classes, 'document' : documents})

#Write to a SQLite database
connection = sqlite3.connect('sms_spam_collection.sqlite')
connection.text_factory = str
df.to_sql(con = connection, name = 'sms', if_exists = 'replace')
connection.close()

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'

#Get data from database
connection = sqlite3.connect('sms_spam_collection.sqlite')
cur = connection.cursor()
cur.execute('SELECT * FROM sms;')
data = cur.fetchall()
connection.close()

sentences = []
#goes through each row from data in database
for row in data:
	#row[2] is the message from the sms
	text = row[2]
	#splits the message into sentences
	#not perfect but good enough
	current_sentences = tokenize.sent_tokenize(text)
	sentences += current_sentences

unigrams = {}
bigrams = {}
trigrams = {}


for sentence in sentences:
	#ideal to have spaces between words and punctuation
	sentence = sentence.replace(".", " . ").replace(","," , ").replace("  ", " ")
	if sentence[-1] == " ":
		sentence = sentence[:-1]
	#split sentence into array
	sentence_array = sentence.split(' ')
	sentence_array.insert(0,START_SYMBOL)
	sentence_array.insert(0,START_SYMBOL)
	sentence_array.append(STOP_SYMBOL)

	#count unigrams
	for word in sentence_array:
	    if word == START_SYMBOL:
	        continue
	    if (word,) in unigrams:
	        unigrams[(word,)] += 1
	    else:
	        unigrams[(word,)] = 1

	#count bigrams
	for bigram_tuple in list(nltk.bigrams(sentence_array)):
		if bigram_tuple[0]==START_SYMBOL and bigram_tuple[1]==START_SYMBOL:
			continue
		if bigram_tuple in bigrams:
		    bigrams[bigram_tuple] += 1
		else:
		    bigrams[bigram_tuple] = 1

	#count trigrams
	for trigram_tuple in list(nltk.trigrams(sentence_array)):
	    if trigram_tuple in trigrams:
	        trigrams[trigram_tuple] += 1
	    else:
	        trigrams[trigram_tuple] = 1