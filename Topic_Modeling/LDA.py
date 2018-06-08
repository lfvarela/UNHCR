from stop_words import get_stop_words
import string
import numpy as np
import lda
import os
from sklearn.feature_extraction.text import CountVectorizer

stop_words = get_stop_words('english') #pulls in stop words from stop_words library

translator = str.maketrans('', '', string.punctuation)
vocab = []
print(vocab)
corpus = []
doc_complete = [doc1, doc2, doc3, doc4, doc5]

transcript_path = './transcripts/KevinTranscripts/Transcripts1/'
transcript_files = os.listdir(transcript_path)

for file in transcript_files:
	if file.endswith('.txt'):
		with open(transcript_path + file) as myfile:
			raw = myfile.read().replace('\n', '')
			raw = raw.lower().translate(translator) #remove punctutation
			raw_words = raw.split()
			result_words = [word.lower() for word in raw_words if word.lower() not in stop_words] #clean/filter text
			#print(result_words)
			#corpus = corpus + [result_words
			vocab = vocab + result_words
			corpus.append(' '.join(result_words)) #add text to corpus
			#entry.text = result_words #update text for specific entry

vectorizer = CountVectorizer(min_df=1)
#print(corpus)
X = vectorizer.fit_transform(corpus) #count vectorizer for all words
X_names = vectorizer.get_feature_names() #names = different words in vectorizer

model = lda.LDA(n_topics=4, n_iter=1500, random_state=1).fit(X) #create LDA model with n_topics

# for entry in whole:
	# whole[entry.ID].topic = np.argmax(model.doc_topic_[entry.ID]) #assign specific topic to individual entry

topic_word = model.topic_word_  # model.components_ also works
n_top_words = 8
for i, topic_dist in enumerate(topic_word):
	topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
	print('Topic {}: {}'.format(i, ' '.join(topic_words)))



		

