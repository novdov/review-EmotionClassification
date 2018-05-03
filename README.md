# Emotion Classification of Movie Reviews 

## Contents

### 1. Overview

- Why emotion classification of movie reviews?
  - Get many information from emotions of reviews rather than ratings
  - Main concern: Check how good classification can be done

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
- Tf-Idf/Multinomial Naive Bayes (with/without tokenizing)
- CNN-LSTM
  - Conv - Pooling - LSTM (256-4-128)
  - epochs: 10, batch size: 150
  - activation function: relu
  - train/validation/test - 80865/53911/14976

### 4. Results

- Result Summary

|                                            | D. Data | N. Data | Accuracy | Recall | F1-Score |
| ------------------------------------------ | :-----: | :-----: | :------: | :----: | :------: |
| Doc2Vec/Logistic Regression                |  04/30  | 152,479 |   0.57   |        |          |
| Tf-Idf/Multinomial NB (without tokenizing) |  04/30  | 152,479 |   0.64   |  0.65  |   0.63   |
| CNN-LSTM                                   |  05/02  | 149,752 |   0.93   |        |          |
| Tf-Idf/Multinomial NB                      |  05/03  | 148,861 |   0.77   |  0.77  |   0.77   |
| Tf-Idf/Multinomial NB (oversampling)       |  05/03  | 148,861 |   0.86   |  0.86  |   0.86   |

- Tf-Idf/Multinomial NB
  - 05/01
    - Row recall at 역겹다/슬프다/무섭다 - 0.44/0.35/0.30 (Accuracy: 0.75/0.73/0.77)
    - Accuracy and recall of 기쁘다/화나다 imporved after tokenizing. (0.68/0/85, 0.61/0.61 → 0.69/0.91, 0.61/0/67)
    - Misclassifying other emotions as 기쁘다 (even more 기쁘다 at 무섭다/슬프다) - Main problem! 
  - 05/03
    - After removing mislabeled items (152,479 → 149,752 mainly in 기쁘다), recall of 화나다/역겹다/무섭다/슬프다 imporved. (0.67/0.44/0.35/0.30 → 0.78/0.64/0.62/0.55)
  - 05/03
    - Data filtered (mainly 기쁘다)
    - Oversampling → precision/recall improved, especially 역겹다/슬프다/무섭다 (recall 0.65/0.62/0.56 → 0.89/0.87/0.94)

- CNN-LSTM

  - 05/02

    - Failed to use word2vec embedding. (`model.wv.get_keras_embedding`) - Vocabulary size of word2vec embedding (9829) does not match keras tokenizing. (`tokenizer.fit_ont_texts`, 48495): Failed to handle
    - 1 epoch -  0.95, but test loss increased at follwing epochs.

    <img src="https://i.imgur.com/ow3SeFb.png">

### 5. Lessons



