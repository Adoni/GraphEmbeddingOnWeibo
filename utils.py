import json


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
