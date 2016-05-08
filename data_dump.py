#coding:utf8
import json
from small_utils.vector_reader import read_vectors
from multiprocessing import Process
import time


def dump_vector(in_file_name):
    #将embedding数据存储为json格式
    print 'Dump file %s' % in_file_name
    out_file_name = in_file_name + '.json'
    vector = read_vectors(in_file_name, as_dict=True, as_list=True)
    with open(out_file_name, 'w') as outfile:
        json.dump(vector, outfile)


def dump_small_graph(in_file_name):
    #small_graph中存储了first graph中所有的uid的所有朋友，这些朋友可能是first graph中的也可能是second graph中的
    #本函数将small graph读入成字典形式并存储为json格式
    print 'Dump file %s' % in_file_name
    if 'zhihu' in in_file_name:
        website = 'zhihu'
    if 'weibo' in in_file_name:
        website = 'weibo'
    if 'dblp' in in_file_name:
        website = 'dblp'
    if 'outputacm' in in_file_name:
        website = 'outputacm'
    t = time.time()
    graph = dict()
    uids = set(
        [
            line.strip().split('||')[0]
            #for line in open('./graph_data/cleaned_first_graph.data')
            for line in open('./%s_user_attributes.data' % website)
        ]
    )
    with open(in_file_name) as fin:
        for line in fin:
            pos = line.find(' ')
            if pos == -1:
                continue
            uid = line[0:pos]
            if uid not in uids:
                continue
            line = line.strip().split(' ')
            graph[uid] = line[1:]
    out_file_name = in_file_name + '.small.json'
    with open(out_file_name, 'w') as outfile:
        json.dump(graph, outfile)
    print time.time() - t


def dump_graph(in_file_name):
    #本函数将graph读入成字典形式并存储为json格式
    print 'Dump file %s' % in_file_name
    t = time.time()
    graph = dict()
    with open(in_file_name) as fin:
        for line in fin:
            line = line.strip().split(' ')
            graph[line[0]] = line[1:]
    out_file_name = in_file_name + '.json'
    with open(out_file_name, 'w') as outfile:
        json.dump(graph, outfile)
    print time.time() - t


def dump(f, in_file_name):
    #多线程序列化,传入函数名和该函数的参数
    p = Process(target=f, args=[in_file_name, ])
    p.start()


if __name__ == '__main__':
    #dump_small_graph('./graph_data/dblp_graph.data')
    #dump_small_graph('./graph_data/reversed_dblp_graph.data')
    #dump(dump_vector,'./embedding/dblp_line_embedding.data')
    for i in [25690]:
        print(i)
        dump(dump_vector, './embedding/zhihu_neibor_embedding_1_%d.data'%i)
        dump(dump_vector, './embedding/zhihu_neibor_embedding_2_%d.data'%i)
    print 'Done'
