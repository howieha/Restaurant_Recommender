import numpy as np
import os
import pandas as pd
import pickle
from statistics import mean
import matplotlib.pyplot as plt
from sklearn import metrics
from collections import defaultdict

DIRNAME = os.path.dirname(__file__)


def count_total_restaurant(file_name= './data/db_business.tsv'):

    file_name = os.path.join(DIRNAME, file_name)
    business_df = pd.read_csv(file_name, sep='\t')
    n_resturant = len(business_df)
    del business_df
    return n_resturant

def read_pickle(file_name='./data/collaborative_filtered_recommendation_0.1.pickle'):
    """
    :param file_name: RELATIVE path to the folder of this python file
    :return: data
    """
    file_name = os.path.join(DIRNAME, file_name)
    with open(file_name, 'rb') as data_file:
        data = pickle.load(data_file)
    return data

def rcmd_stats(data):
    """
    :param data: a dict containing recommendation data {user_id1: [rest1: score1, rest2: score2 ...], user_id2: ... }

    :return: None
    """

    key_list = list(data.keys())
    lengths = [len(data[key]) for key in key_list]

    minimum = min(lengths)
    maximum = max(lengths)
    avg = mean(lengths)
    print('min: ', minimum, 'max: ', maximum, 'mean: ', avg)
    plt.text(20, 0.3, 'min: %d' % minimum, fontsize=12)
    plt.text(20, 0.275, 'max: %d' % maximum, fontsize=12)
    plt.text(20, 0.25, 'avg: %f' % avg, fontsize=12)


    _, _, _ = plt.hist(lengths, bins=list(range(minimum, maximum+1)), density=True, color='#0504aa', alpha=0.7, rwidth=0.85)
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.xlim(0, 30)
    plt.show()

def dict_to_df(pred_data):
    """
    :param pred_data:  a dict containing recommendation data {user_id1: [rest1: score1, rest2: score2 ...], user_id2: ... }
    :return:
    """

    # first sort the dict by descending pred score, and generate a dict {'user_id1': [rest1, rest2 ...], 'user_id2', [rest1...]...}
    pred_data = {user: [rest for rest, score in sorted(pred_data[user].items(), key=lambda item: item[1], reverse=True)] for user in pred_data}

    user_ids = list(pred_data.keys())
    rec_rest_ids = [pred_data[user_id] for user_id in user_ids]

    pred_df = pd.DataFrame({'user_id': user_ids, 'pred_rcmd': rec_rest_ids})
    return pred_df


def reorder_pred_df(pred_data, ground_data):
    """
    Reorder the pred_data user_id to have the same order as ground_data
    :return: reordered pred_data
    """
    pred_data = pred_data.set_index('user_id')
    pred_data = pred_data.reindex(list(ground_data['user_id']))
    pred_data = pred_data.reset_index()
    return pred_data

def top_k(rcmd_list, k):
    if len(rcmd_list) > k:
        rcmd_list = rcmd_list[:k]
    return rcmd_list


def confusion_matrix(pred_rcmd, rcmd, N_rest, k=5):
    """
    :param pred_rcmd: Pandas Series pred_rcmd
    :param rcmd_true: Pandas Series rcmd (ground truth)
    :param N_rest: Total number of restaurant
    :param k: number of item to be recommended to the user
    :return: confusion matrix
    """
    # change the list to set for further calculations
    pred_rcmd = pred_rcmd.apply(lambda x: top_k(x, k))
    confusion_df = pd.DataFrame({'pred_rcmd': pred_rcmd.apply(set), 'rcmd': rcmd.apply(set)})
    confusion_df['true_pos'] = confusion_df.apply(lambda x: len(x['pred_rcmd'].intersection(x['rcmd'])), axis=1)
    confusion_df['false_pos'] = confusion_df.apply(lambda x: len(x['pred_rcmd'] - x['rcmd']), axis=1)
    confusion_df['false_neg'] = confusion_df.apply(lambda x: len(x['rcmd'] - x['pred_rcmd']), axis=1)
    confusion_df['true_neg'] = confusion_df.apply(lambda x: N_rest - x['true_pos'] - x['false_pos'] - x['false_neg'], axis=1)

    return confusion_df


def precision(confusion_df):
    prec = confusion_df.apply(lambda x: x['true_pos']/(x['true_pos'] + x['false_pos']) if (x['true_pos'] + x['false_pos']) > 0 else float('nan'), axis=1)
    prec = prec.mean(skipna=True)
    return prec

def recall(confusion_df):
    rec = confusion_df.apply(
        lambda x: x['true_pos'] / (x['true_pos'] + x['false_neg']) if (x['true_pos'] + x['false_neg']) > 0 else float(
            'nan'), axis=1)
    rec = rec.mean(skipna=True)
    return rec

def fallout(confusion_df):
    fo = confusion_df.apply(
        lambda x: x['false_pos'] / (x['false_pos'] + x['true_neg']) if (x['false_pos'] + x['true_neg']) > 0 else float(
            'nan'), axis=1)
    fo = fo.mean(skipna=True)
    return fo

def missRate(confusion_df):
    mr = confusion_df.apply(
        lambda x: x['false_neg'] / (x['true_pos'] + x['false_neg']) if (x['true_pos'] + x['false_neg']) > 0 else float(
            'nan'), axis=1)
    mr = mr.mean(skipna=True)
    return mr

def invPrecision(confusion_df):
    ip = confusion_df.apply(
        lambda x: x['true_neg'] / (x['true_neg'] + x['false_neg']) if (x['true_neg'] + x['false_neg']) > 0 else float(
            'nan'), axis=1)
    ip = ip.mean(skipna=True)
    return ip

def invRecall(fallout):
    return 1 - fallout

def f1(precision, recall):
    return 2 * precision * recall / (precision + recall)

def markedness(precision, invPrecision):
    return precision + invPrecision - 1

def informedness(recall, invRecall):
    return recall + invRecall - 1

def matt_corr(markness, informedness):
    if markness < 0:
        return - ((markness * informedness) ** (1/2))
    else:
        return (markness * informedness) ** (1/2)

def AUC_ROC(fpr, tpr):
    return metrics.auc(fpr, tpr)

def preprocess_ground(ground_data_path):
    """
    :param ground_data_path: Relative path for ground truth file
    :return: preprocessed ground_data
    """
    # pandas df in ['user_id', 'average_stars', 'rcmd_true', 'rcmd_false']
    ground_data = read_pickle(ground_data_path)
    # append a new column that contains only recommended ids (without score)
    ground_data['rcmd'] = ground_data['rcmd_true'].apply(lambda d: list(d.keys()))

    # rcmd_stats(dict(zip(ground_data['user_id'], ground_data['rcmd_true'])))

    return ground_data

def preprocess_pred(pred_data_path, ground_data):
    """
    :param pred_data_path: Relative path for prediction file
    :param ground_data_path: preprocessed ground-truth data
    :return: preprocessed pred_data
    """
    # dict
    pred_data = read_pickle(pred_data_path)

    # rcmd_stats(pred_data)

    # convert predict_data to pandas df of ['user_id', 'pred_rcmd']
    pred_df = dict_to_df(pred_data)

    # set pred_df to have the same user_id ordering as ground_data's
    pred_df = reorder_pred_df(pred_df, ground_data)

    return pred_df



def evaluation(pred_data, ground_data):
    """
    :param pred_data: preprocessed  pred_data in Pandas DF
    :param ground_data: preprocessed ground_data in Pandas DF
    :return: evaluation scores in a Pandas DF: {'metric1':[score1, ..., score10], 'metric2': [score 1,..., score10] ....}
    :return: auc-roc score
    """
    n_resturant = count_total_restaurant()

    metrics_funcs = [precision, recall, fallout, missRate, invPrecision]

    eval_scores = defaultdict(list)

    fpr = []
    tpr = []
    for k in range(10):
        eval_scores['k'].append(k+1)
        conf_matrix = confusion_matrix(pred_data['pred_rcmd'], ground_data['rcmd'], n_resturant, k=k+1)
        for metric in metrics_funcs:
            temp_score = metric(conf_matrix)
            eval_scores[metric.__name__].append(temp_score)
            if metric.__name__ == 'recall':
                tpr.append(temp_score)
            elif metric.__name__ == 'fallout':
                fpr.append(temp_score)
        eval_scores['invRecall'].append(invRecall(eval_scores['fallout'][k]))
        eval_scores['f1'].append(f1(eval_scores['precision'][k], eval_scores['recall'][k]))
        eval_scores['markedness'].append(markedness(eval_scores['precision'][k], eval_scores['invPrecision'][k]))
        eval_scores['informedness'].append(informedness(eval_scores['recall'][k], eval_scores['invRecall'][k]))
        eval_scores['matt_corr'].append(matt_corr(eval_scores['markedness'][k], eval_scores['informedness'][k]))
        print("k = %d finished" % (k+1))


    eval_scores = pd.DataFrame(eval_scores)
    print(eval_scores)
    auc_roc = metrics.auc(fpr, tpr)
    print(auc_roc)

    return (eval_scores, auc_roc)






if __name__ == "__main__":

    file_suffix = [str(i+1) for i in range(7)]
    ground_data_path = './data/user_recommend.p'

    ground_data = preprocess_ground(ground_data_path)
    auc_roc = []
    for i in file_suffix:
        print('-------collaborative_filtered_recommendation_0.%s starts!!!-------' % i)

        pred_data_path = './data/collaborative_filtered_recommendation_0.%s.pickle' % i

        pred_data = preprocess_pred(pred_data_path, ground_data)
        eval_scores, temp_auc_roc = evaluation(pred_data, ground_data)
        eval_scores.to_csv('%s/eval_score/eval_0.%s.csv' % (DIRNAME, i), index=False)
        auc_roc.append(temp_auc_roc)
        print('-------collaborative_filtered_recommendation_0.%s finished!!!-------' % i)
        print('--------------------------------------------------------------------')

    auc_df = pd.DataFrame({'i': file_suffix, 'auc_roc': auc_roc})
    auc_df.to_csv('%s/eval_score/auc.csv' % DIRNAME, index=False)








