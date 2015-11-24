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

def main(labels,embedding_fname):
    print '======='
    from collections import Counter
    print Counter(labels.values())
    embedding=get_embedding(labels.keys(),embedding_fname)
    uids=list(set(embedding.keys()) & set(labels.keys()))
    X=map(lambda uid:embedding[uid],uids)
    Y=map(lambda uid:labels[uid],uids)
    clf=LogisticRegression()
    scores=cross_validation.cross_val_score(clf, X, Y, cv=5, scoring='f1_weighted')
    print("F1 weighted: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    scores=cross_validation.cross_val_score(clf, X, Y, cv=5, scoring='f1_micro')
    print("F1 micro: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    scores=cross_validation.cross_val_score(clf, X, Y, cv=5, scoring='f1_macro')
    print("F1 macro: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    if len(set(labels.values()))==2:
        scores=cross_validation.cross_val_score(clf, X, Y, cv=5, scoring='roc_auc')
        print("ROC_AUC: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    #clf=SVC(kernel='linear', C=1)
    #scores=cross_validation.cross_val_score(clf, X, Y, cv=5, scoring='f1_weighted')
    #print("F1: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    print '==============='

if __name__=='__main__':
    fname='./line_embedding.data'
    main(get_label(1,gender_reg),fname)
    main(get_label(2,age_reg),fname)
    main(get_label(3,location_reg),fname)
