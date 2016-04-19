from multiprocessing.dummy import Pool as ThreadPool
import urllib2
import json

with open('./graph_data/reversed_cleaned_second_graph.data.json') as data_file:
    graph = json.load(data_file)
for key in graph:
    graph[key] = set(graph[key])


def get_weights(uid):
    try:
        neibors = graph[uid]
    except:
        return []
    weights = []
    for n in neibors:
        try:
            weights.append((n, len(graph[n] & neibors)))
        except:
            weights.append((n, 0))
    return zip(*weights)


def dump_weight():
    uids = [
        line.strip().split(' ')[0]
        for line in open('./graph_data/cleaned_first_graph.data')
    ]
    weight_file = open('./graph_data/reversed_weights.data', 'a')
    GROUP = 100
    for i in range(0, GROUP):
        print i
        group_uids = uids[i * len(uids) / GROUP:(i + 1) * len(uids) / GROUP]
        pool = ThreadPool(10)
        weights = pool.map(get_weights, group_uids)
        pool.close()
        pool.join()
        #weights=[]
        #for uid in group_uids:
        #    weights.append(get_weights(uid))
        for uid, single_weight in zip(group_uids, weights):
            if single_weight == []:
                continue
            weight_file.write(str(uid))
            weight_file.write('\n')
            weight_file.write(' '.join(single_weight[0]))
            weight_file.write('\n')
            weight_file.write(' '.join(map(lambda x: str(x), single_weight[1])))
            weight_file.write('\n')


if __name__ == '__main__':
    dump_weight()
