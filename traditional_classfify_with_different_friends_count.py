from construct_train_data import *
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import json
from utils import thread_load
import numpy as np
from sklearn.cross_validation import train_test_split
import sys


def get_neibor_embedding(fname, index):
    data = thread_load(fname)
    embedding = dict()
    for uid, e in data.items():
        if len(e) < 6:
            continue
        embedding[uid] = list(e[2][index]) + list(e[3][index]) + list(e[4][index]) + list(e[5][index])
    return embedding

def simple_evaluate(labels, embedding):
    #simple_evaluate function uses default params without any params tuning
    from collections import Counter
    uids = list(set(embedding.keys()) & set(labels.keys()))
    X = map(lambda uid: embedding[uid], uids)
    Y = map(lambda uid: labels[uid], uids)
    print '\t', dict(Counter(Y))
    clf=LogisticRegression()
    score_names=['precision_weighted','recall_weighted','f1_weighted','f1_micro','f1_macro','roc_auc']
    for score_name in score_names:
        scores=cross_validation.cross_val_score(clf, X, Y, cv=2, scoring=score_name)
        print("%s:\t%0.2f (+/- %0.2f)" % (score_name, scores.mean(), scores.std() * 2))
    sys.stdout.flush()

def evaluate_our_method(iter_count=20):
    print '======Our; Iter Count: %d======' % iter_count
    counts=[5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300, 350, 390]
    for index in range(0,len(counts)):
        embedding = get_neibor_embedding(
        './embedding/user_embedding_using_neibors_%d.data.json' % iter_count
    )
        print index
        simple_evaluate(get_label(1, gender), embedding)
        #simple_evaluate(get_label(2, age_reg), embedding)
    #simple_evaluate(get_label(2, age_reg), embedding)


if __name__ == '__main__':
    #evaluate_baseline('./embedding/user_embedding_using_deepwalk.data.json')
    #evaluate_baseline('./embedding/user_embedding_using_line.data.json')
    #evaluate_our_method(iter_count=10)
    #evaluate_our_method(iter_count=15)
    evaluate_our_method(iter_count=20)
    print 'Done'
