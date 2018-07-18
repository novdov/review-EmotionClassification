from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.utils import np_utils
from file_io import *

train_docs = load_pickle('../docs.pickle')
labels = load_pickle('../labels.pickle')

def data_to_sequences(train_docs, labels):
    MAX_SEQUENCE_LENGTH = max([len(row) for row in train_docs])

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(train_docs)
    sequences = tokenizer.texts_to_sequences(train_docs)

    x_train = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    y_train = np_utils.to_categorical(labels)

    save_pickle('../x_train_sequences.pickle', x_train)
    save_pickle('../y_train_sequences.pickle', labels)

if __name__=='__main__':
    data_to_sequences(train_docs, labels)
