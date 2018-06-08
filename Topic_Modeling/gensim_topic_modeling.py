from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import os

import string
import numpy as np
import lda
import os
from sklearn.feature_extraction.text import CountVectorizer


stop_words = get_stop_words('english') #pulls in stop words from stop_words library
additional_stop_words = ['thanks', 'thank', 'you', 'un', 'agency', 'call', 'and', 'destiny', 'make']
translator = str.maketrans('', '', string.punctuation)
stop_words = stop_words + additional_stop_words
tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
   

# compile sample documents into a list
doc_set = []

transcript_path = './transcripts/UNHCR_Transcripts_CS50_Use/'
transcript_files = os.listdir(transcript_path)

# Create document list
for file in transcript_files:
	if file.endswith('.txt') and "Inbound" in file and "PrankCall" not in file and "HangUp" not in file:
		with open(transcript_path + file) as myfile:
			raw = myfile.read().replace('\n', '')
			raw = raw.lower().translate(translator) #remove punctutation
			raw_words = raw.split()
			result_words = [word.lower() for word in raw_words if word.lower() not in stop_words] #clean/filter text
			doc_set.append(' '.join(result_words)) #add text to corpus
			#entry.text = result_words #update text for specific entry

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:
    
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]
    
    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    
    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=6, id2word = dictionary, passes=20)
print(ldamodel.print_topics())

