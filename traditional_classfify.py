from construct_train_data import *
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import StandardScaler
import json
from utils import thread_load
import numpy as np

def get_simple_embedding(fname):
    return thread_load(fname)

def get_neibor_embedding(fname):
    data=thread_load(fname)
    embedding=dict()
    for uid,e in data.items():
        if len(e)<6:
            continue
        embedding[uid]=e[0]+e[1]+e[2]+e[3]
        #embedding[uid]=e[0]+e[1]
    return embedding

def evaluate(labels,embedding):
    #print '======='
    from collections import Counter
    uids=list(set(embedding.keys()) & set(labels.keys()))
    X=map(lambda uid:embedding[uid],uids)
    Y=map(lambda uid:labels[uid],uids)
    print '\t',dict(Counter(Y))
    #clf=LogisticRegression()
    #clf=SVC()
    #score_names=['precision_weighted','recall_weighted','f1_weighted','f1_micro','f1_macro','roc_auc']
    #for score_name in score_names:
    #    scores=cross_validation.cross_val_score(clf, X, Y, cv=2, scoring=score_name)
    #    print("F1 micro:\t%0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}, {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5,
                                   scoring='%s_weighted' % score)
    clf.fit(X_train, y_train)

def evaluate_baseline(fname):
    if 'deepwalk' in fname:
        print '======Deepwalk======'
    if 'line' in fname:
        print '======LINE======'
    embedding=get_simple_embedding(fname)
    evaluate(get_label(1,gender_reg),embedding)
    evaluate(get_label(2,age_reg),embedding)
    evaluate(get_label(3,location_reg),embedding)

def evaluate_our_method(iter_count=20):
    print '======Our; Iter Count: %d======'%iter_count
    embedding=get_neibor_embedding('./embedding/user_embedding_using_neibors_%d.data.json'%iter_count)
    evaluate(get_label(1,gender_reg),embedding)
    evaluate(get_label(2,age_reg),embedding)
    evaluate(get_label(3,location_reg),embedding)

if __name__=='__main__':
    evaluate_baseline('./embedding/user_embedding_using_deepwalk.data.json')
    evaluate_baseline('./embedding/user_embedding_using_line.data.json')
    evaluate_our_method(iter_count=10)
    evaluate_our_method(iter_count=15)
    evaluate_our_method(iter_count=20)
    evaluate_our_method(iter_count=50)
    print 'Done'
