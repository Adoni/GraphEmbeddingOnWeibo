import time
from utils import thread_load

if __name__=='__main__':
    d=thread_load('./embedding/user_embedding_using_neibors.data.json')
    for uid,v in d.items():
        print len(v)
    print len(d)
    print 'Done'
