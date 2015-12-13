from construct_train_data import *
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
from sklearn.svm import SVC

def get_embedding(uids,fname):
    uids=set(uids)
    embedding=dict()
    f=open(fname)
    line=f.readline()
    embedding_size=int(line.strip().split(' ')[1])
    for line in f:
        line=line.strip().split(' ')
        if line[0] in uids:
            if len(line)==embedding_size+1:
                embedding[line[0]]=map(lambda v:float(v),line[1:])
    return embedding

def get_combined_embedding(uids,fname1,fname2):
    embedding1=get_embedding(uids,fname1)
    embedding2=get_embedding(uids,fname2)
    embedding=dict()
    for uid in embedding1:
        try:
            embedding[uid]=embedding1[uid]+embedding2[uid]
        except:
            continue
    return embedding

def evaluate(labels,embedding_fname,embedding_fname2=None):
    print '======='
    from collections import Counter
    if embedding_fname2==None:
        embedding=get_embedding(labels.keys(),embedding_fname)
    else:
        embedding=get_combined_embedding(labels.keys(),embedding_fname,embedding_fname2)
    uids=list(set(embedding.keys()) & set(labels.keys()))
    X=map(lambda uid:embedding[uid],uids)
    Y=map(lambda uid:labels[uid],uids)
    print len(Y)
    print '\t',dict(Counter(Y))
    clf=LogisticRegression()
    scores=cross_validation.cross_val_score(clf, X, Y, cv=5, scoring='f1_weighted')
    print("F1 weighted:\t%0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    scores=cross_validation.cross_val_score(clf, X, Y, cv=5, scoring='f1_micro')
    print("F1 micro:\t%0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    scores=cross_validation.cross_val_score(clf, X, Y, cv=5, scoring='f1_macro')
    print("F1 macro:\t%0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    if len(set(labels.values()))==2:
        scores=cross_validation.cross_val_score(clf, X, Y, cv=5, scoring='roc_auc')
        print("ROC_AUC:\t%0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    print '==============='

def evaluate_baseline(fname):
    evaluate(get_label(1,gender_reg),fname1)
    evaluate(get_label(2,age_reg),fname1)
    evaluate(get_label(3,location_reg),fname1)

def evaluate_our_method():
    fname1='./embedding/neibor_embedding_1_50.data'
    fname2='./embedding/neibor_embedding_2_50.data'

    evaluate(get_label(1,gender_reg),fname1,fname2)
    evaluate(get_label(2,age_reg),fname1,fname2)
    evaluate(get_label(3,location_reg),fname1,fname2)

if __name__=='__main__':
    #evaluate_baseline('./embedding/deepwalk_embedding.data')
    #evaluate_baseline('./embedding/line_embedding.data')
    evaluate_our_method()
