import re
from konlpy.tag import Twitter
twitter = Twitter()


def tokenize(doc):
    """
    Tokenize document with tokens/POS tags pairs.
    :param doc: Document to tokenize
    :return: token/POS tags paired document
    For iterable documents, they should be in iteration.
    """
    return ['/'.join(t) for t in twitter.pos(doc, norm=True, stem=True)]


def remove_pos(docs):
    """
    Remove POS tagging from token/POS.
    :param docs: Document to remove POS tags
    :return: Document with removed POS. Same result as tokenizing.
    """
    p = '/([a-zA-Z]+)[+]*([a-zA-Z]*)'
    pos_removed = []
    for s in docs:
        result = re.sub(p, '', s)
        pos_removed.append(result)
    return pos_removed


def remove_stopwords(doc, stopwords):
    """
    Remove stopwords from doc.
    :param doc: Document to remove stopwords
    :param stopwords: stopwords corpus
    :return: documents with removed stopwords
    """
    stopwords_removed = []
    for token in doc:
        if token not in stopwords:
            stopwords_removed.append(token)


def get_similar_words(docs):
    li_new = []
    for word in docs:
        try:
            token = model.wv.most_similar(tokenize(word)[0], topn=8)
            if token not in li_new:
                li_new.append(token)
        except KeyError:
            pass

    return li_new


def get_labels(train_docs,
               joy_list, anger_list, disgust_list, sadness_list, fear_list):

    train_docs_labeled = []

    for row in train_docs:
        joy_score = 0
        anger_score = 0
        disgust_score = 0
        sadness_score = 0
        fear_score = 0

        all_scores = {
            '기쁘다': joy_score,
            '화나다': anger_score,
            '역겹다': disgust_score,
            '슬프다': sadness_score,
            '무섭다': fear_score
        }

        for _, token in enumerate(row):

            if token in joy_list:
                joy_score += 1
            elif token in anger_list:
                anger_score += 1
            elif token in disgust_list:
                disgust_score += 1
            elif token in sadness_list:
                sadness_score += 1
            elif token in fear_list:
                fear_score += 1

            all_scores['기쁘다'] += joy_score
            all_scores['화나다'] += anger_score
            all_scores['역겹다'] += disgust_score
            all_scores['슬프다'] += sadness_score
            all_scores['무섭다'] += fear_score

            label = max(all_scores, key=lambda key: all_scores[key])

        if all_scores[label] == 0:
            label = '중립'
            train_docs_labeled.append((row, label))
        elif all_scores['기쁘다'] == all_scores['화나다'] == all_scores['역겹다'] == all_scores['슬프다'] == all_scores['무섭다']:
            label = '중립'
            train_docs_labeled.append((row, label))
        else:
            train_docs_labeled.append((row, label))

    return train_docs_labeled
