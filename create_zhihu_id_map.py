def create_id_map():
    all_ids = set()
    for line in open('./cleaned_zhihu_graph.data'):
        line = line.strip().split(' ')
        all_ids.update(line)
    fout1 = open('zhihu_id2int.data', 'w')
    fout2 = open('zhihu_int2id.data', 'w')
    for i, id in enumerate(all_ids):
        fout1.write('%s %d\n' % (id, i))
        fout2.write('%d %s\n' % (i, id))


def map_zhihu_graph_id2int():
    id_map = dict(
        [
            line.strip().split(' ') for line in open(
                './zhihu_id2int.data'
            )
        ]
    )
    fout = open('./remaped_cleaned_zhihu_graph.data', 'w')
    for line in open('./cleaned_zhihu_graph.data'):
        line = line.strip().split(' ')
        line = map(lambda id: id_map[id], line)
        fout.write(' '.join(line) + '\n')


def map_zhihu_embedding_int2id(embedding_file):
    id_map = dict(
        [
            line.strip().split(' ') for line in open(
                './zhihu_int2id.data'
            )
        ]
    )
    fin = open(embedding_file)
    fout = open(embedding_file + 'maped', 'w')
    fout.write(fin.readline())
    for line in fin:
        loc = line.find(' ')
        try:
            zhihu_id = id_map[line[0:loc]]
        except Exception as e:
            print e
            continue
        fout.write(id_map[line[0:loc]] + line[loc:])


if __name__ == '__main__':
    #create_id_map()
    #map_zhihu_graph()
    map_zhihu_embedding_int2id('./embedding/zhihu_deepwalk_embedding.data')
    print 'Done'
