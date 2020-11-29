import os
import collections
import nltk.classify
import nltk.metrics
from nltk.classify import NaiveBayesClassifier
import pandas as pd

def train_bayes_classifier(dict_path):
    """
    Take two files (one containing a dictionary of positive words and the other containing a
    dictionary of negative words) and train a naive bayes classifier based on them.

    Input:
    - Path containing the opinion-lexicon-English dictionaries by Liu et al.
      (See https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html for more details)
    
    Output:
    - Naive Bayes classifier.
    """
    # Read dictionary files.
    ENGLISH_OPINION_LEXICON_LOCATION = os.path.join(dict_path)
    POS_WORDS_FILE = os.path.join(ENGLISH_OPINION_LEXICON_LOCATION, 'positive-words.txt')
    NEG_WORDS_FILE = os.path.join(ENGLISH_OPINION_LEXICON_LOCATION, 'negative-words.txt')

    pos_words = []
    neg_words = []

    for pos_word in open(POS_WORDS_FILE, 'r').readlines()[35:]:
        pos_words.append(({pos_word.rstrip(): True}, 'positive'))

    for neg_word in open(NEG_WORDS_FILE, 'r').readlines()[35:]:
        neg_words.append(({neg_word.rstrip(): True}, 'negative'))

    # Train classifier.
    all_words_with_sentiment = pos_words + neg_words
    bayes_classifier = NaiveBayesClassifier.train(all_words_with_sentiment)
    return bayes_classifier
  
def to_dictionary(words):
    """
    Helper function to convert list of words into a dictionary.
    """
    return dict([(word, True) for word in words])

def predict_sentiment(text, classifier, expected_sentiment=None):
    """
    Predict the sentiment of a sentence using a given classifier.
    """
    text_to_classify = to_dictionary(text.split())
    result = classifier.classify(text_to_classify)
    return result

def run_sentiment_analysis_on_rt(review, classifier):
    """
    """
    actual_set = collections.defaultdict(set)
    words = review.split(".")
    intt = 0
    for i in range(len(words)-1):
        actual_sentiment = predict_sentiment(words[i], classifier)
        actual_set[actual_sentiment].add(intt)
        intt+=1
    score=(len(actual_set['positive'])-len(actual_set['negative']))*1.0
    return score

if __name__ == "__main__":
    # Train classifier.
    classifier = train_bayes_classifier('Data/opinion-lexicon-English')

    # Read review data.
    rvd_type = {'review_id': 'string', 'user_id': 'string', 'business_id': 'string',
                'stars': 'Int8',
                'Interact.useful': 'Int32', 'Interact.funny': 'Int32', 'Interact.cool': 'Int32',
                'content': 'string', 'date': 'string'
                }
    db_review = pd.read_csv(r"Data/dataset_review.tsv",
                    dtype=rvd_type,
                    sep='\t', na_values='None')
    db_review['date'] = pd.to_datetime(db_review['date'])

    # Apply classifier to review content.
    db_review['emo_score'] = db_review.apply(
            lambda row: run_sentiment_analysis_on_rt(row['content'], classifier), axis=1)
    
    # Write to output file.
    output_path = os.path.join(os.path.dirname(__file__), "Data/dataset_review_emo_bayes.tsv")
    db_review.to_csv(output_path, index=False, sep="\t")
