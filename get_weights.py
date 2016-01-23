from multiprocessing.dummy import Pool as ThreadPool

with open('./graph_data/cleaned_first_graph.data.dump.json') as data_file:
    graph = json.load(data_file)
for key in graph:
    graph[key] = set(graph[key])


def get_weights(uid):
    neibors = graph()
    weights = []
    for n in neibors:
        weights.append((n, graph[n] & neibors))
    return zip(*weights)


def dump_weight():
    uids = [
        line.strip().split(' ')[0]
        for line in open('./graph_data/cleaned_first_graph.data')
    ]
    weight_file = open('./graph_data/weight.data.dump.json', 'a')
    GROUP = 1000
    for i in range(0, 10):
        print i
        group_uids = uids[i * len(uids) / GROUP:(i + 1) * len(uids) / GROUP]
        pool = ThreadPool(10)
        weights = pool.map(get_weights, group_uids)
        pool.close()
        pool.join()
        for uid, single_weight in zip(group_uids, weights):
            weight_file.write(str(uid))
            weight_file.write('\n')
            weight_file.write(' '.join(single_weight[0]))
            weight_file.write('\n')
            weight_file.write(' '.join(map(lambda x: str(x), single_weight[1])))
            weight_file.write('\n')


if __name__ == '__main__':
    dump_weight()
