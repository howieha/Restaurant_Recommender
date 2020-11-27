import pandas as pd
from datetime import datetime
from ast import literal_eval

def read_emo_words(emo_words_file):
    emo_words_set = set()
    f = open(emo_words_file, "r")
    for line in f:
        words = line.split()
        # Ignore header
        if len(words) == 1 and words[0][0] != ';':
            emo_words_set.add(words[0].strip().lower())
    return emo_words_set

def calc_emo_score(review_content, pos_words, neg_words):
    emo_score = 0
    review_words = review_content.split()
    word_count = len(review_words)
    for word in review_words:
        word = word.strip(" ,./:!?|[]()&%$#@*'")
        if word == "":
            word_count -= 1
        if word in pos_words:
            emo_score += 1
        elif word in neg_words:
            emo_score -= 1
    return emo_score / word_count

def process_emo_score(review_df, pos_words_file, neg_words_file):
    pos_words_set = read_emo_words(pos_words_file)
    neg_words_set = read_emo_words(neg_words_file)
    review_df['emo_score'] = review_df.apply(lambda row: calc_emo_score(row['content'], 
        pos_words_set, neg_words_set), axis=1)
    return review_df

if __name__ == "__main__":
    # READ REVIEW DATABASE
    rvd_type = {'review_id': 'string', 'user_id': 'string', 'business_id': 'string',
                'stars': 'Int8',
                'Interact.useful': 'Int32', 'Interact.funny': 'Int32', 'Interact.cool': 'Int32',
                'content': 'string', 'date': 'string'
                }
    db_review = pd.read_csv(r"Data/dataset_review.tsv",
                        dtype=rvd_type,
                        sep='\t', na_values='None')
    db_review['date'] = pd.to_datetime(db_review['date'])
    review_df = process_emo_score(db_review, 
        "Data/opinion-lexicon-English/positive-words.txt", 
        "Data/opinion-lexicon-English/negative-words.txt")
    review_df.to_csv("Data/dataset_review_emo.tsv", index=False, sep="\t")
