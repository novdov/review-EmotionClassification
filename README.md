# Emotion Classification in Movie Reviews 

## 1. Introduction

- **Objective**
  - Main concern: How to find movies fit me?
  - Get information of moives from context of reviews, not rating itself.
  - Classify reviews as 5 emotions.
- **Data Sources**
  - [Naver sentiment movie corpus v1.0](https://github.com/e9t/nsmc)
  - [Naver 영화 네티즌 평점](https://movie.naver.com/movie/point/af/list.nhn) (from crawling)
- **Tools**
  - [KoNLPy](http://konlpy-ko.readthedocs.io/ko/v0.4.3/)
  - [Word2Vec/Doc2Vec](https://radimrehurek.com/gensim/)
  - [scikit-learn](http://scikit-learn.org/stable/)
  - [keras](https://keras.io/)
  - [Flask](http://flask.pocoo.org/)
  - [Bootstrap](https://getbootstrap.com/)
  - [soynlp](https://github.com/lovit/soynlp)
  - [soyspacing](https://github.com/lovit/soyspacing)

## 2. Preprocessing

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
  <img src="https://github.com/novdov/review-EmotionClassification/blob/master/img/emotion-clf.001.png?raw=true" width="700">
</p>

## 3. Modeling

- Doc2Vec/Logistic Regression
- Tf-Idf/Multinomial Naive Bayes (w/o tokenizing, oversampling)
- CNN-LSTM
  - Conv1D - Pooling - LSTM
  - epochs: 10, batch size: 200
  - activation function: relu



## 4. Results

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
    - 0.67/0.44/0.35/0.30 → 0.78/0.66/0.61/0.57
  - Oversampling → precision/recall improved, especially 역겹다/슬프다/무섭다
    - Recall 0.66/0.61/0.57 → 0.89/0.87/0.95
- CNN-LSTM
  - Overfitted
- Best performance: MNB (without tokenizing) towards real data.



### Analysis of Wrong Predictions

- Image of normalized confusion matrix

<img src="https://i.imgur.com/RNLGrN6.png" width="500">

- Most of wrong predictions are classified as joy.

- Below table contains reivews classified as joy which are selected every 10 turn in first 100 predictions.

- | Reason        | 'sadness' reviews classified as joy                          |
  | ------------- | ------------------------------------------------------------ |
  | Noise         | 오랜만에 맘에 드는 애니네요 제발 업 좀 빨리 해주세요 ㅜㅜ    |
  | Multi-Emo     | 김지영감독님 수고 많으셨습니다.마지막 로이킴 봄봄봄 노래가 이렇게 슬픈줄..잘 보았습니다. 꼭 보세요 강추 |
  | Noise         | 마미를 보고 봐서 조금 아쉬웠지만 데뷔작이라고 하기엔 정말 좋았다. 자비에돌란의 감성은 놀랍다. |
  | Noise         | 극장에서 보이 못한게 아쉽네요. 좋은영화입니다.               |
  | Noise         | 아..다시보고싶네요ㅜㅜ리메이크안되나요?제인생최고의드라마!그대와함께! |
  | Fale Negative | ㅠㅠ 진실은 밝혀져야합니다                                   |
  | Noise         | 마음을 찡하게 하는 장군이와 천둥이와의 아름다운 우정이...임수정씨의 열연과 함께 감동적인 작품입니다~인간성이 상실되어 가는 지금 마음 따뜻해지게 하는 그런 작품인 것 같네요^^ |
  | Noise         | 드라마를 이렇게까지 집중해서 본건 처음인것 같습니다 연출력도 연출력이지만 배우들 연기와 스토리가 너무 좋았습니다ㅠㅠ 본방으로 못본게 너무 아쉬울정도! |
  | Noise         | 개봉하자마자 본 보람이 있네여ㅠㅠㅠ 꾸르잼!                  |
  | Noise         | 으웩우우에에에에ㅜ우우웅                                     |

  Small samples, but noisy data cause wrong predictions









## 5. Web Application

- http://dovvvv.tk
- Flask / Bootstrap

<p align="center">
  <img src="https://i.imgur.com/1YgjESJ.png">
</p>

## 6. Limitations

- Failed to use word2vec embedding due to lack of data for word embeddings; Did not consider large data for embedding at first.
  - Used words are limited to movie related expressions.
- More tags are needed. (예) 당황스럽다, 놀라다, 미안하다 등)
  - There are sentences which are hard to be classified as 5 labels including neutral state.
  - More reviews should have been included in 5 emotions. (87,037 reviews are not included)
  - More well-prepared data without noises.
- Low tokenizing/POS tagging performance (More sopisticated preprocessing is required.)
  - Vulnerable to mis-spell, typing errors, and spacing. (Improper to web texts)
  - Alternatives: [soynlp](https://github.com/lovit/soynlp), [soyspacing](https://github.com/lovit/soyspacing)… (at preprocessing stage)

## 7. Follow-Up

- Using `soynlp`, `soyspacing`
  - Low performance than original model (tried: `soynlp`/`soyspacing`→`twitter`)
  - Spacing correction need more train data, I think. (used data: [sample data of `soyspacing`](https://raw.githubusercontent.com/lovit/soyspacing/master/demo_model/134963_norm.txt))
  - Spacing correction did not work well when using news texts.
  
## 8. Lessons

- Obviously, data is important. (Proper reflection of real data outside model.)
- Preprocessing is very important. (Especially in Korean texts.)
- Define problems well.
  - In this project, 5 labels were too simple to capture other emotions like disappointment, embarrassment, surprise and other subtle emotions.

##  9. How to improve?

- Well-prepared data
  - Well-defined labels to capture most of emotions
- Proper preprocessing for short web texts
  - Spacing correction
  - Better tokenizing (not KoNLPy) e.g.) cohesion probablity
- Other embeddings
  - Fasttext based on consonant-vowel unit
