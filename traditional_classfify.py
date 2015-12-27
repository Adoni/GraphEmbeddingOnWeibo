from construct_train_data import *
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
from sklearn.svm import SVC
import json
from utils import thread_load

def get_simple_embedding(fname):
    return thread_load(fname)

def get_neibor_embedding(fname):
    data=thread_load(fname)
    embedding=dict()
    for uid,e in data.items():
        if len(e)<4:
            continue
        #embedding[uid]=e[0]+e[1]+e[2]+e[3]
        embedding[uid]=e[2]+e[3]
    return embedding

def evaluate(labels,embedding):
    print '======='
    from collections import Counter
    uids=list(set(embedding.keys()) & set(labels.keys()))
    X=map(lambda uid:embedding[uid],uids)
    Y=map(lambda uid:labels[uid],uids)
    print len(Y)
    print '\t',dict(Counter(Y))
    clf=LogisticRegression()
    scores=cross_validation.cross_val_score(clf, X, Y, cv=2, scoring='f1_weighted')
    print("F1 weighted:\t%0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    scores=cross_validation.cross_val_score(clf, X, Y, cv=2, scoring='f1_micro')
    print("F1 micro:\t%0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    scores=cross_validation.cross_val_score(clf, X, Y, cv=2, scoring='f1_macro')
    print("F1 macro:\t%0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    if len(set(labels.values()))==2:
        scores=cross_validation.cross_val_score(clf, X, Y, cv=5, scoring='roc_auc')
        print("ROC_AUC:\t%0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    print '==============='

def evaluate_baseline(fname):
    embedding=get_simple_embedding(fname)
    evaluate(get_label(1,gender_reg),embedding)
    evaluate(get_label(2,age_reg),embedding)
    evaluate(get_label(3,location_reg),embedding)

def evaluate_our_method():
    embedding=get_neibor_embedding('./embedding/user_embedding_using_neibors.data.json')
    evaluate(get_label(1,gender_reg),embedding)
    evaluate(get_label(2,age_reg),embedding)
    evaluate(get_label(3,location_reg),embedding)

if __name__=='__main__':
    #evaluate_baseline('./embedding/user_embedding_using_deepwalk.data.json')
    #evaluate_baseline('./embedding/user_embedding_using_line.data.json')
    evaluate_our_method()
    print 'Done'
