import time
from utils import thread_load
from traditional_classfify import get_simple_embedding
from construct_train_data import get_label
import json
import numpy

def dump(labels,embedding,fname):
    uids=list(set(embedding.keys()) & set(labels.keys()))
    X=map(lambda uid:embedding[uid],uids)
    Y=map(lambda uid:labels[uid],uids)
    numpy.save(fname+'_X.data',X)
    numpy.save(fname+'_Y.data',Y)

if __name__=='__main__':
    fname='./embedding/user_embedding_using_line.data.json'
    embedding=get_simple_embedding(fname)
    dump(get_label(1,gender_reg),embedding,'./training_data/line_gender')
