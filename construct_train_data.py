#coding:utf8
import json
from multiprocessing.dummy import Pool as ThreadPool
import numpy
import random


def get_location_labels():
    labels = dict()
    with open('./location.label') as f_l:
        for line in f_l:
            line = line.strip().split(' ')
            key = line[0]
            key = key.replace('省', '')
            key = key.replace('省', '')
            key = key.replace('市', '')
            key = key.replace('维吾尔族自治区', '')
            key = key.replace('回族自治区', '')
            key = key.replace('壮族自治区', '')
            key = key.replace('特别行政区', '')
            labels[key] = int(line[1])
    return labels


location_labels = get_location_labels()


def gender_reg(v):
    if v == '男' or v == 'm' or v == 'male':
        return 0
    elif v == '女' or v == 'f' or v == 'female':
        return 1
    else:
        return None


def age_reg(v, split_point=25):
    try:
        age = 2015 - int(v)
        if 5 <= age <= 100:
            if age <= split_point:
                return 0
            else:
                return 1
            return age
        else:
            return None
    except:
        return None


def location_reg(v):
    v = v.strip().split(' ')[0]
    try:
        return location_labels[v]
    except:
        return None


def get_label(website, label_index, label_reg):
    labels = dict()
    for line in open('./%s_user_attributes.data' % website):
        line = line.strip().split('||')
        uid = line[0]
        label = label_reg(line[label_index])
        if label == None:
            continue
        labels[uid] = label
    #print len(labels)
    return labels


def thread_load(file_name):
    print 'loading from %s' % file_name
    with open(file_name) as data_file:
        data = json.load(data_file)
    print 'loading done'
    return data


def load(file_names):
    pool = ThreadPool(len(file_names))
    results = pool.map(thread_load, file_names)
    pool.close()
    pool.join()
    return tuple(results)


def get_user_embedding_on_simple_embedding(website, embedding_method):
    uids = [
        line.strip().split('||')[0]
        for line in open('./%s_user_attributes.data' % website)
    ]
    embedding_file = './embedding/%s_%s_embedding.data.json' % (
        website, embedding_method
    )
    out_filename = './embedding/%s_user_embedding_using_%s.data.json' % (
        website, embedding_method
    )
    embedding = thread_load(embedding_file)
    user_embedding = dict()
    for uid in uids:
        try:
            user_embedding[uid] = embedding[uid]
        except:
            continue
    with open(out_filename, 'w') as outfile:
        json.dump(user_embedding, outfile)
    print 'Get simple user embedding done'


def get_weights():
    f = open('./graph_data/weights.data')
    weights = dict()
    while 1:
        uid = f.readline().strip()
        if uid == '':
            break
        neibors = f.readline().strip().split(' ')
        weight = map(lambda x: int(x), f.readline().strip().split(' '))
        weights[uid] = dict(zip(neibors, weight))
    return weights


def construct_friends_embedding_with_certain_count(friend_embeddings):
    #counts=[1,2,3,4,5,6,7,8,9,10]+range(20,310,10)
    counts = []
    result = []
    for count in counts:
        if count <= len(friend_embeddings):
            tmp_embedding = random.sample(friend_embeddings, count)
            result.append(list(numpy.mean(tmp_embedding, axis=0)))
        else:
            result.append([])
    if friend_embeddings == []:
        result.append([])
    else:
        result.append(list(numpy.mean(friend_embeddings, axis=0)))
    return result


def get_user_embedding_with_friends(website, iter_count):
    uids = [
        line.strip().split('||')[0]
        for line in open('./%s_user_attributes.data' % website)
    ]
    weights = get_weights()
    embedding_file = './embedding/%s_neibor_embedding_1_%d.data.json' % (
        website, iter_count
    )
    re_embedding_file = './embedding/%s_neibor_embedding_2_%d.data.json' % (
        website, iter_count
    )
    graph_file = './graph_data/cleaned_%s_graph.data.small.json' % website
    re_graph_file = './graph_data/reversed_cleaned_%s_graph.data.small.json' % website
    graph, re_graph, embedding, re_embedding = load(
        [graph_file, re_graph_file, embedding_file, re_embedding_file]
    )
    #graph,re_graph=load([graph_file,re_graph_file])
    user_embedding = dict()
    print 'Start'
    for index, uid in enumerate(uids):
        if uid not in graph:
            print 'H1', uid
            continue
        if uid not in re_graph:
            print 'H2', uid
            continue
        if uid not in embedding:
            print 'H3', uid
            continue
        if uid not in re_embedding:
            print 'H4', uid
            continue

        user_embedding[uid] = []

        #1. append user's embedding
        user_embedding[uid].append(embedding[uid])
        #2. append user's reversed embedding
        user_embedding[uid].append(re_embedding[uid])
        #3. append user's embedding from who he or her follows
        e1 = []
        e2 = []
        for friend in graph[uid]:
            try:
                e1.append(re_embedding[friend])
                e2.append(embedding[friend])
            except:
                continue
        if e1 == [] or e2 == []:
            continue
        #user_embedding[uid].append(list(numpy.mean(e1, axis=0)))
        user_embedding[uid].append(
            construct_friends_embedding_with_certain_count(e1)
        )
        #user_embedding[uid].append(list(numpy.mean(e2, axis=0)))
        user_embedding[uid].append(
            construct_friends_embedding_with_certain_count(e2)
        )
        #4. append user's embedding from who he or her follows
        e1 = []
        e2 = []
        for friend in re_graph[uid]:
            try:
                e1.append(embedding[friend])
                e2.append(re_embedding[friend])
            except:
                continue
        if e1 == [] or e2 == []:
            continue
        #user_embedding[uid].append(list(numpy.mean(e1, axis=0)))
        user_embedding[uid].append(
            construct_friends_embedding_with_certain_count(e1)
        )
        #user_embedding[uid].append(list(numpy.mean(e2, axis=0)))
        user_embedding[uid].append(
            construct_friends_embedding_with_certain_count(e2)
        )

    with open(
        './embedding/%s_user_embedding_using_neibors_%d.data.json' %
        (website, iter_count), 'w'
    ) as outfile:
        json.dump(user_embedding, outfile)
    print 'Get user embedding with friend done'


def main():
    #get_label(3,location_reg)
    #get_user_embedding()
    #get_user_embedding_with_friends(10)
    #get_user_embedding_with_friends(15)
    #get_user_embedding_with_friends('zhihu',10)
    #get_user_embedding_with_friends('zhihu',20)
    #get_user_embedding_with_friends('zhihu',30)
    #get_user_embedding_with_friends('zhihu',40)
    #get_user_embedding_with_friends('zhihu',50)
    get_user_embedding_with_friends('zhihu', 60)
    get_user_embedding_with_friends('zhihu', 70)
    #get_user_embedding_with_friends(25)
    #get_user_embedding_with_friends(30)
    #get_user_embedding_with_friends(50)
    #get_user_embedding_on_simple_embedding('zhihu','deepwalk')
    #get_user_embedding_on_simple_embedding('zhihu','line')
    pass


if __name__ == '__main__':
    main()
    #get_weights()
    print 'Done'
