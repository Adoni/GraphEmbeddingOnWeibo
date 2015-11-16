import random
import numpy

def get_graph(file_name):
        graph_file=open(file_name)
        graph=dict()
        for line in graph_file:
            line=line.strip().split(' ')
            graph[line[0]]=line[1:]
        return graph

def get_a_random_path_from_graph(graph,length):
    from small_utils.progress_bar import progress_bar
    path=[]
    node=numpy.random.choice(graph.keys())
    path.append(node)
    bar=progress_bar(length-1)
    for i in range(length-1):
        try:
            neibor=numpy.random.choice(graph[node])
        except Exception as e:
            print e
            neibor=numpy.random.choice(graph.keys())
        if neibor not in graph:
            neibor=numpy.random.choice(graph.keys())
        node=neibor
        path.append(node)
        bar.draw(i)
    return path

def deep_walk(total_nodes_count):
    import random
    import os
    graph=get_graph('./cleaned_second_graph.data')
    print 'Get graph done'
    path=get_a_random_path_from_graph(graph, total_nodes_count)
    print len(set(path))
    raw_file_name='deep_walk_path.data'
    open(raw_file_name,'w').write(' '.join(path)+'\n')
    embedding_file_name='deep_walk_embedding.data'
    print '\nEmbedding...'
    command='~/word2vec/word2vec -train %s -output %s -cbow 0 -size 100 -window %d -negative 1 -hs 0 -sample 1e-3 \
    -min-count 1 -threads 10 -binary 0'%(raw_file_name, embedding_file_name,5)
    print command
    os.system(command)
    print '\nEmbedding Done'

if __name__=='__main__':
    deep_walk(10000)
