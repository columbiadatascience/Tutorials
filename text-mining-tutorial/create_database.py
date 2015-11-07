import pandas as pd
import sqlite3
from StringIO import StringIO
import urllib2
import zipfile

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