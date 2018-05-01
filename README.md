# Emotion Classification of Movie Reviews 

## Contents

### 1. Overview

- **Data Sources**
  - [Naver movie rating](https://movie.naver.com/movie/point/af/list.nhn) (for corpus and train/test set)

### 2. Corpus Construction

- Total 252,847 reviews from Naver movie rating
- 5 labels (기쁘다, 화나다, 역겹다, 슬프다, 무섭다)
- Corpus construction
  - Tokenizing/Pos tagging -  Twitter (KoNLPy)

  - Word Embedding (300 dimension)  - Word2Vec

  - Get similar words from Word2Vec model → Make corpus for each label

    ```python
    model.wv.most_similar('기쁘다/Noun', topn=100) ...
    ```

  - Tagging label to reviews/Removing mislabeled and neutral items

<img src="https://i.imgur.com/sRYPYXz.jpg">

### 3. Modeling

- Doc2Vec/Logistic Regression
- Tf-Idf/Multinomial Naive Bayes

### 4. Results

|                                            | Accuracy | Recall |
| ------------------------------------------ | -------- | ------ |
| Doc2Vec/Logistic Regression                | 0.57     |        |
| Tf-Idf/Multinomial NB (without tokenizing) | 0.64     | 0.65   |

### 5. Lessons











