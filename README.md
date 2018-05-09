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
  - [KoNLPy](http://konlpy-ko.readthedocs.io/ko/v0.4.3/)
  - [gensim](https://radimrehurek.com/gensim/)
  - [scikit-learn](http://scikit-learn.org/stable/)
  - [keras](https://keras.io/)
  - [Flask](http://flask.pocoo.org/)
  - [Bootstrap](https://getbootstrap.com/)

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

<p align="center">
  <img src="https://i.imgur.com/sRYPYXz.jpg" width="700">
</p>

### 3. Modeling

- Doc2Vec/Logistic Regression
- Tf-Idf/Multinomial Naive Bayes (with/without tokenizing, oversampling)
- CNN-LSTM
  - Conv1D - Pooling - LSTM
  - epochs: 10, batch size: 200
  - activation function: relu

### 4. Results

- Metrics of each model

|                                      | Precision | Recall | F1-Score |
| ------------------------------------ | :-------: | :----: | :------: |
| Doc2Vec/Logistic Regression          |   0.55    |  0.56  |   0.52   |
| Tf-Idf/Multinomial NB                |   0.64    |  0.65  |   0.63   |
| Tf-Idf/Multinomial NB (tokenizing)   |   0.77    |  0.78  |   0.77   |
| Tf-Idf/Multinomial NB (oversampling) |   0.85    |  0.86  |   0.85   |
| CNN-LSTM                             |   0.93    |  0.93  |   0.93   |

- Tf-Idf/Multinomial NB
  - Row recall at 역겹다/슬프다/무섭다 - 0.44/0.35/0.30 (Precision 0.75/0.73/0.77)
  - Recall of 화나다/역겹다/슬프다/무섭다 imporved after tokenizing. 
    - 0.67/0.44/0.35/0.30 → 0.78/0.64/0.62/0.55
  - Oversampling → precision/recall improved, especially 역겹다/슬프다/무섭다
    - Recall 0.66/0.61/0.57 → 0.89/0.87/0.95
- CNN-LSTM
  - Overfitted
- Best performance: MNB (without tokenizing) towards outside data.

<p align="center">

<img src="https://i.imgur.com/hwdAysw.png" width="700">

</p>



### 5. Web Application

- Flask / Bootstrap

<p align="center">
  <img src="https://i.imgur.com/df8YErl.png" width="600">
</p>

### 6. Limitations

- Failed to use word2vec embedding due to lack of data for word embeddings; Did not consider large data for embedding at first.
  - Used words are limited to movie related expressions.
- More tags are needed. (예) 당황스럽다, 놀라다, 미안하다 등)
  - There are sentences which are hard to be classified as 5 labels including neutral state.
- Low tokenizing/POS tagging performance (More sopisticated preprocessing is required.)
  - Vulnerable to mis-spell, typing errors, and spacing. (Improper to web texts)
  - Alternatives: [soynlp](https://github.com/lovit/soynlp), [soyspacing](https://github.com/lovit/soyspacing)… (at preprocessing stage)

