from __future__ import division
import os
import collections
import nltk.classify
import nltk.metrics

def tokenize_file_and_apply_label(filename, label):
    words_label_tuple_list = []
    for line in open(filename, 'r').readlines():
        words = [word.lower() for word in line.split() if len(word) >= 3]
        words_label_tuple_list.append((list_to_dict(words), label))
    return words_label_tuple_list
    
def list_to_dict(words):
    return dict([(word, True) for word in words])
  
  
###

ENGLISH_OPINION_LEXICON_LOCATION = os.path.join('opinion-lexicon-English')
POS_WORDS_FILE = os.path.join(ENGLISH_OPINION_LEXICON_LOCATION, 'positive-words.txt')
NEG_WORDS_FILE = os.path.join(ENGLISH_OPINION_LEXICON_LOCATION, 'negative-words.txt')

# pos_words = [({'amazing': True}, 'positive'), ({'great': True}, 'positive')]
# neg_words = [({'pathetic': True}, 'negative')]

pos_words = []
neg_words = []

for pos_word in open(POS_WORDS_FILE, 'r').readlines()[35:]:
    pos_words.append(({pos_word.rstrip(): True}, 'positive'))

for neg_word in open(NEG_WORDS_FILE, 'r').readlines()[35:]:
    neg_words.append(({neg_word.rstrip(): True}, 'negative'))


print("Number of positive words %d" % len(pos_words))

print("Number of negative words %d" % len(neg_words))

all_words_with_sentiment = pos_words + neg_words

print("Total number of words %d" % len(all_words_with_sentiment))

from nltk.classify import NaiveBayesClassifier

classifier = NaiveBayesClassifier.train(all_words_with_sentiment)  
  
def to_dictionary(words):
    return dict([(word, True) for word in words])

test_data = []
def predict_sentiment(text, expected_sentiment=None):
    text_to_classify = to_dictionary(text.split())
    result = classifier.classify(text_to_classify)
    test_data.append([text_to_classify, expected_sentiment])
    return result




#pos_tokens = tokenize_file_and_apply_label(POSITIVE_REVIEWS_FILE, "positive")
#print(pos_tokens)

def run_sentiment_analysis_on_rt():
	REVIEWS_FILE = 'D:\class\EECS545\sentiment-analysis-python-master\sentiment-analysis-python-master\pp.txt'
	rt_reviewers = open(REVIEWS_FILE, 'r')

   # expected_pos_set = collections.defaultdict(set)
	
	score_review=[]
	for index,review in enumerate(rt_reviewers.readlines()):
       # expected_pos_set['positive'].add(index)
		actual_set = collections.defaultdict(set)
		words=review.split(".")
		intt=0
		print(words)
		for i in range(len(words)-1):
			actual_sentiment = predict_sentiment(words[i])
			actual_set[actual_sentiment].add(intt)
			intt+=1
			print(actual_sentiment)
		#print(actual_set)
		print(len(actual_set['negative'])+len(actual_set['positive']))
		print()
		score=(len(actual_set['positive'])-len(actual_set['negative']))*1.0
		score_review.append(score)
	print("score for the reviews are ", score_review)
        

    #print ('accuracy: %.2f' % nltk.classify.util.accuracy(classifier, test_data))
    #print 'pos precision: %.2f' % nltk.metrics.precision(expected_pos_set['positive'], actual_pos_set['positive'])
    #print 'pos recall: %.2f' % nltk.metrics.recall(expected_pos_set['positive'], actual_pos_set['positive'])
    #print 'neg precision: %.2f' % nltk.metrics.precision(expected_neg_set['negative'], actual_neg_set['negative'])
    #print 'neg recall: %.2f' % nltk.metrics.recall(expected_neg_set['negative'], actual_neg_set['negative'])


run_sentiment_analysis_on_rt()
