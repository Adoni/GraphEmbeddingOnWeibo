import random
import numpy
from small_utils.progress_bar import progress_bar
from multiprocessing.dummy import Pool as ThreadPool

global graph


def get_graph(file_name):
    graph_file = open(file_name)
    graph = dict()
    for line in graph_file:
        line = line.strip().split(' ')
        graph[line[0]] = line[1:]
    return graph


def get_a_random_path_from_graph(index):
    global graph
    global chain_count
    path = []
    node = numpy.random.choice(graph.keys())
    path.append(node)
    for i in range(chain_count - 1):
        try:
            neibor = numpy.random.choice(graph[node])
        except Exception as e:
            print e
            neibor = numpy.random.choice(graph.keys())
        if neibor not in graph:
            neibor = numpy.random.choice(graph.keys())
        node = neibor
        path.append(node)
    return path


def deep_walk(total_nodes_count=None):
    import random
    import os
    global chain_count
    global graph
    graph = get_graph('./cleaned_second_graph.data')
    if total_nodes_count == None:
        total_nodes_count = len(graph.keys()) * 10
    print 'Get graph done'
    chain_count = 1000
    bar = progress_bar(total_nodes_count / chain_count)
    #pool = ThreadPool(psutil.cpu_count())
    #pathes=pool.map(get_a_random_path_from_graph,xrange(total_nodes_count/chain_count))
    #pool.close()
    #pool.join()
    raw_file_name = 'deep_walk_path.data'
    fout = open(raw_file_name, 'a')
    embedding_file_name = 'deep_walk_embedding.data'
    for i in xrange(total_nodes_count / chain_count):
        path = get_a_random_path_from_graph(i)
        fout.write(' '.join(path) + '\n')
        bar.draw(i + 1)
    print '\nEmbedding...'
    command = '~/word2vec/word2vec -train %s -output %s -cbow 0 -size 100 -window %d -negative 1 -hs 0 -sample 1e-3 \
    -min-count 0 -threads 10 -binary 0' % (raw_file_name, embedding_file_name,
                                           5)
    print command
    os.system(command)
    print '\nEmbedding Done'


if __name__ == '__main__':
    deep_walk()
