# Emotion Classification of Movie Reviews 

### 1. Introduction

- **Objective**
  - Main concern: How to find movies fit me?
  - Get information of moives from context of reviews, not rating itself.
  - Classify reviews as 5 emotions.
- **Data Sources**
  - [Naver sentiment movie corpus v1.0](https://github.com/e9t/nsmc)
  - [Naver 영화 네티즌 평점](https://movie.naver.com/movie/point/af/list.nhn) (from crawling)
- **Tools**
  - [`KoNLPy`](http://konlpy-ko.readthedocs.io/ko/v0.4.3/)
  - [`gensim`](https://radimrehurek.com/gensim/)
  - [`scikit-learn`](http://scikit-learn.org/stable/)
  - [`keras`](https://keras.io/)

### 2. Preprocessing

- Total 252,847 reviews at initial point.
- 5 labels (기쁘다, 화나다, 역겹다, 슬프다, 무섭다)
- Tagging labels
  - Tokenizing/Pos tagging -  Twitter (KoNLPy)
  - Word Embedding (300 dimension)  - Word2Vec
  - Get similar words from Word2Vec model → Make corpus for each label
  - Tagging label to reviews using constructed corpus
  - Removing mislabeled and neutral items (manually)
  - 165,810 labeled reviews after preprocessing

<img src="https://i.imgur.com/sRYPYXz.jpg">

### 3. Modeling

- Doc2Vec/Logistic Regression
- Tf-Idf/Multinomial Naive Bayes (with/without tokenizing, oversampling)
- CNN-LSTM
  - Conv1D - Pooling - LSTM
  - epochs: 10, batch size: 150
  - activation function: relu

### 4. Results

- Metrics of each model

|                                      | Accuracy | Recall | F1-Score |
| ------------------------------------ | :------: | :----: | :------: |
| Doc2Vec/Logistic Regression          |   0.55   |  0.56  |   0.52   |
| Tf-Idf/Multinomial NB                |   0.64   |  0.65  |   0.63   |
| Tf-Idf/Multinomial NB (tokenizing)   |   0.77   |  0.78  |   0.77   |
| Tf-Idf/Multinomial NB (oversampling) |   0.85   |  0.86  |   0.85   |
| CNN-LSTM                             |   0.93   |        |          |

- Tf-Idf/Multinomial NB
  - Row recall at 역겹다/슬프다/무섭다 - 0.44/0.35/0.30 (Accuracy: 0.75/0.73/0.77)
  - Accuracy and recall of 기쁘다/화나다 imporved after tokenizing. (0.68/0/85, 0.61/0.61 → 0.69/0.91, 0.61/0/67)

  - Oversampling → precision/recall improved, especially 역겹다/슬프다/무섭다 (recall 0.65/0.62/0.56 → 0.89/0.87/0.94)

- CNN-LSTM


### 5. Limitations

- Failed to use word2vec embedding due to lack of data for word embeddings. Did not consider data for embedding at first.

