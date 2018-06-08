import os, csv, re, glob, nltk
import argparse, textwrap
import numpy as np
import pandas as pd
import sklearn.feature_extraction.text as text
from sklearn import decomposition
from nltk import word_tokenize
from nltk.corpus import stopwords

# Import Custom User Stopwords (If Any)
from custom_stopword_tokens import custom_stopwords

# Original Working Directory
owd = os.getcwd()

# ----------------------------------------------#
# SUPPORT FUNCTIONS
# ----------------------------------------------#

def start_csv(file_name):
    with open(file_name, 'w') as f:
        writer = csv.writer(f)


def tokenize_nltk(text):
	"""
	Note: 	This function imports a list of custom stopwords from the user
			If the user does not modify custom stopwords (default=[]),
			there is no substantive update to the stopwords.
	"""
	tokens = word_tokenize(text)
	text = nltk.Text(tokens)
	stop_words = set(stopwords.words('english'))
	stop_words.update(custom_stopwords)
	words = [w.lower() for w in text if w.isalpha() and w.lower() not in stop_words]
	return words


def select_files(text_or_tweet, file_path="."):

	#Set Data Directory
	os.chdir(file_path)

	try:
		if text_or_tweet == "text":
			filenames = glob.glob("*.txt")
		elif text_or_tweet == "tweet":
			rawcsv = glob.glob("*.csv")[0]
			twitter_data = pd.read_table(rawcsv, sep=",")
			filenames = twitter_data['TWEET']
		else:
			print("please specify 'text' or 'tweet' for your input type...")

		print("Selecting {} files from {}...".format(len(filenames), file_path))
		return filenames

	except:
		print("please check your file path specification...")


def select_vectorizer(vectorizer_type, req_ngram_range=[1,2]):

	"""
	Select the desired vectorizer for either text or tweet
	@ text_tfidf_std
	@ text_tfidf_custom
	@ text_count_std

	@ tweet_tfidf_std
	@ tweet_tfidf_custom
	"""

	# SPECIFY VECTORIZER ALGORITHM
	#---------------------------------#

	ngram_lengths = req_ngram_range

	if vectorizer_type == "text_tfidf_std":
		# Standard TFIDF Vectorizer (Text)
		vectorizer = text.TfidfVectorizer(input='filename', analyzer='word', ngram_range=(ngram_lengths), stop_words='english', min_df=2)
		return vectorizer
	elif vectorizer_type == "text_tfidf_custom":
		# TFIDF Vectorizer with NLTK Tokenizer (Text)
		vectorizer = text.TfidfVectorizer(input='filename', analyzer='word', ngram_range=(ngram_lengths), stop_words='english', min_df=2, tokenizer=tokenize_nltk)
		print("User specified custom stopwords: {} ...".format(str(custom_stopwords)[1:-1]))
		return vectorizer
	elif vectorizer_type == "text_count_std":
		vectorizer = text.CountVectorizer(input='filename', analyzer='word', ngram_range=(ngram_lengths), stop_words='english', min_df=2)
		return vectorizer
	elif vectorizer_type == "tweet_tfidf_std":
		# Standard TFIDF Vectorizer (Content)
		vectorizer = text.TfidfVectorizer(input='content', analyzer='word', ngram_range=(ngram_lengths), stop_words='english', min_df=2)
		return vectorizer
	elif vectorizer_type == "tweet_tfidf_custom":
		# Standard TFIDF Vectorizer (Content)
		vectorizer = text.TfidfVectorizer(input='content', analyzer='word', ngram_range=(ngram_lengths), stop_words='english', min_df=2, tokenizer=tokenize_nltk)
		print("User specified custom stopwords: {} ...".format(str(custom_stopwords)[1:-1]))
		return vectorizer
	else:
		print("error in vectorizer specification...")
		pass


# ----------------------------------------------#
# MAIN TOPIC MODEL FUNCTION
# ----------------------------------------------#

def topic_modeler(vectorizer_type, topic_clf, n_topics, n_top_terms, req_ngram_range=[1,2], file_path="."):

	"""
    Topic Modeling Function: See Argparse Documentation for Details
	"""

	# Determine Text of Tweet
	text_or_tweet = str(vectorizer_type).split('_')[0]

	# Select Files or Text to Analyze
	filenames = select_files(text_or_tweet, file_path)

	# Specify Number of Topics, Ngram Structure, and Terms per Topic
	num_topics = n_topics
	num_top_words = n_top_terms
	ngram_lengths = req_ngram_range


	# SPECIFY VECTORIZER ALGORITHM
	vectorizer = select_vectorizer(vectorizer_type, ngram_lengths)


	# Vectorizer Results
	dtm = vectorizer.fit_transform(filenames).toarray()
	vocab = np.array(vectorizer.get_feature_names())
	print("Evaluating vocabulary...")
	print("Found {} terms in {} files...".format(dtm.shape[1], dtm.shape[0]))


	# DEFINE and BUILD MODEL
	#---------------------------------#

	if topic_clf == "lda":

		#Define Topic Model: LatentDirichletAllocation (LDA)
		clf = decomposition.LatentDirichletAllocation(n_topics=num_topics+1, random_state=3)

	elif topic_clf == "nmf":

		#Define Topic Model: Non-Negative Matrix Factorization (NMF)
		clf = decomposition.NMF(n_components=num_topics+1, random_state=3)

	elif topic_clf == "pca":

		#Define Topic Model: Principal Components Analysis (PCA)
		clf = decomposition.PCA(n_components=num_topics+1)

	else:
		pass

	print("Fitting Topic Model...")

	#Fit Topic Model
	doctopic = clf.fit_transform(dtm)
	topic_words = []
	num_comp = len(clf.components_)
	count = 0
	for topic in clf.components_:
		count += 1
		word_idx = np.argsort(topic)[::-1][0:num_top_words]
		topic_words.append([vocab[i] for i in word_idx])
		if count % 100 == 0:
			print("%d files analyzed..." % (count))


	print("Results complete:")
	# Show the Top Topics
	if not os.path.exists("results"):
		os.makedirs("results")
	os.chdir("results")
	results_file = "clf_results_{}_model.csv".format(topic_clf)
	start_csv(results_file)
	print("writing topic model results in {}...".format(file_path+"/results/"+results_file))
	for t in range(len(topic_words)):
		print("Topic {}: {}".format(t, ', '.join(topic_words[t][:])))
		with open(results_file, 'a') as f:
			writer = csv.writer(f)
			writer.writerow(["Topic {}, {}".format(t, ', '.join(topic_words[t][:]))])

	# Return to Original Directory
	os.chdir(owd)




# ----------------------------------------------#
# EXAMPLES RUNNING THE FUNCTION WITHOUT ARGPARSE
# ----------------------------------------------#

#topic_modeler("text_tfidf_custom", "nmf", 15, 10, [2,4], "data/president")
#topic_modeler("text_tfidf_custom", "lda", 15, 10, [2,4], "data/president")
#topic_modeler("text_tfidf_custom", "pca", 15, 10, [2,4], "data/president")
#topic_modeler("tweet_tfidf_std", "lda", 15, 10, [1,4], "data/twitter")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Prepare input file',
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('vectorizer_type', type=str,
        help=textwrap.dedent("""\
        	Select the desired vectorizer for either text or tweet
        	@ text_tfidf_std       | TFIDF Vectorizer (for text)
        	@ text_tfidf_custom    | TFIDF Vectorizer with Custom Tokenizer (for text)
        	@ text_count_std       | Count Vectorizer

        	@ tweet_tfidf_std      | TFIDF Vectorizer (for tweets)
        	@ tweet_tfidf_custom   | TFIDF Vectorizer with Custom Tokenizer (for tweets)

            """
            ))
    parser.add_argument('topic_clf', type=str,
        help=textwrap.dedent("""\
        	Select the desired topic model classifier (clf)
        	@ lda     | Topic Model: LatentDirichletAllocation (LDA)
        	@ nmf     | Topic Model: Non-Negative Matrix Factorization (NMF)
        	@ pca     | Topic Model: Principal Components Analysis (PCA)

            """
            ))
    parser.add_argument('n_topics', type=int,
        help=textwrap.dedent("""\
            Select the number of topics to return (as integer)
            Note: requires n >= number of text files or tweets

            Consider the following examples:

            @ 10     | Example: Returns 5 topics
            @ 15     | Example: Returns 10 topics

            """
            ))
    parser.add_argument('n_top_terms', type=int,
        help=textwrap.dedent("""\
            Select the number of top terms to return for each topic (as integer)
            Consider the following examples:

            @ 10     | Example: Returns 10 terms for each topic
            @ 15     | Example: Returns 15 terms for each topic

            """
            ))
    parser.add_argument('req_ngram_range', nargs='+', type=int,
        help=textwrap.dedent("""\
            Select the requested 'ngram' or number of words per term
            @ NG-1:  | ngram of length 1, e.g. "pay"
            @ NG-2:  | ngram of length 2, e.g. "fair share"
            @ NG-3:  | ngram of length 3, e.g. "pay fair share"

            Consider the following ngram range examples:

            @ [1, 2] | Return ngrams of lengths 1 and 2
            @ [2, 5] | Return ngrams of lengths 2 through 5

            """
            ))
    parser.add_argument('file_path', type=str,
        help=textwrap.dedent("""\
            Select the desired file path for the data

            Consider the following ngram range examples:

            @ data/twitter      | Uses data in the data/twitter subdirectory
            @ data/president    | Uses data in the data/president subdirectory
            @ .                 | Uses data in the current directory

            """
            ))

    args = parser.parse_args()
    topic_modeler(args.vectorizer_type, args.topic_clf, args.n_topics, args.n_top_terms, args.req_ngram_range, args.file_path)
