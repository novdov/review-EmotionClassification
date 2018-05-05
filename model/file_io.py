import pickle


def read_data_tab(filename):
    with open(filename, 'r') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]
    return data


def read_data(filename):
    with open(filename, 'r') as f:
        data = [[line] for line in f.read().splitlines()]
        data = data[1:]
    return data


def read_data_comma(filename):
    with open(filename, 'r') as f:
        data = [line.split(',') for line in f.read().splitlines()]
        data = data[1:]
    return data


def save_pickle(file_name, obj):
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)


def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        obj = pickle.load(f)
    return obj
