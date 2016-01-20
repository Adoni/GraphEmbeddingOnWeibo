def get_id_map():
    ids = []
    for line in open('./id_map.txt'):
        line = line.strip().split(' ')
        line.reverse()
        ids.append(line)
    return dict(ids)


def remap():
    id_map = get_id_map()
    print 'Start remap'
    fout = open('remap_weibo_graph.data', 'w')
    false = 0
    for line in open('./weibo_socialgraph.txt'):
        line = line.strip().split()
        new_line = line[0:1] + line[2:]
        try:
            new_line = map(lambda uid: id_map[uid], new_line)
        except:
            false += 1
            print false
            continue
        fout.write(' '.join(new_line) + '\n')


if __name__ == '__main__':
    remap()
    print 'Done'
