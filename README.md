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

- Metrics of each model (test data)

|                                      | Precision | Recall | F1-Score |
| ------------------------------------ | :-------: | :----: | :------: |
| Tf-Idf/Multinomial NB (tokenizing)   |   0.77    |  0.77  |   0.77   |
| Tf-Idf/Multinomial NB (oversampling) |   0.74    |  0.73  |   0.73   |

- Tf-Idf/Multinomial NB
  - Recall of 역겹다/슬프다/무섭다 are is lower than recall of 기쁘다/화나다
    - 역겹다/슬프다/무섭다: 0.64/0.60/0.59
    - 기쁘다/화나다: 0.88/0.78
  - After oversampling, recall of 역겹다/슬프다/무섭다 improved and recall of 기쁘다/화나다 decreased.
    - 역겹다/슬프다/무섭다: 0.64/0.60/0.59 → 0.68/0.67/0.66
    - 기쁘다/화나다: 0.88/0.78 → 0.77/0.73
- Best performance: MNB (without tokenizing) towards real data.



### Analysis of Wrong Predictions

- Image of normalized confusion matrix

<img src="https://i.imgur.com/RNLGrN6.png" width="350">

- Most of wrong predictions are classified as joy.
- Below table contains reivews classified as joy which are selected every 10 turn in first 100 predictions.
- Small samples, but noisy data cause wrong predictions

| Reason  | 'Sad' reviews classified as joy |
|:---|:---|
| FN | 가만있다 정말 이유 없이 불현듯 떠오른 '가을동화'. 보고싶어졌습니다. 전편을 이틀만에 봤습니다. 크헉크헉 울면서... 다시 봐도 명작입니다. 영상미, 배경들 미치도록 아름답네요. 두고두고 가슴에 남을 거예요. 아... 아리고 아린 드라마. 가을동화 |
| Noise [Joy] | 임권택감독의 삶에대한 관조가 고스란히 묻어있는 역작임. 정말 많은 생각을 하게 해주는영화 |
| Noise [Multi] | 보다말았어요 ㅠ 너무 지루했어요 ㅠ근데 배경은 이뻤어요.. |
| Noise [Joy] | 마음 울리는 영화연기 내용 비주얼 하나 빠짐없이 완벽함 |
| Noise [Joy] | 아무 생각없이 봤는데 기대 이상, 강한 여운이 남는다 |
| Noise [Joy] | 트와일라잇부터 다시 달렸는데.. 뭔가 함께 세월을 보낸 느낌이다. 뱀파이어물은 갑이다. 너무 멋있다 ㅠ ㅠ... 재미있었습니다. |
| Noise [Multi] | 이때정전된 일본이야기가 서바이벌 패밀리입니다. 인류가 얼마나 고통을 당하게 되엇을지. 정말 생각머리없는 악당패거리들! 지금의 환경오염 속도를 생각하면 그 에이아이가 현재에 얼마나 좋을까 상상하게 되는 영화. 지구는 지금도 인간에 의해 망해 가는 중. |
| Noise [Joy] | 코끝찡하고 아릅답고 희망적이었다 |
| Noise [Disappoint] | 전성기가 아닌 성장기.. 아쉬운 영화네요.. 긴 시간 몰입도 부족.. |
| Noise [Joy] | 심장이 나대지마 공포중 최고였던거같습니다 |


## 5. Web Application

- http://dovvvv.tk
- Flask / Bootstrap

<p align="center">
  <img src="https://i.imgur.com/1YgjESJ.png">
</p>

## 6. Limitations

- **Because of stemming, when eomi(어미) changes, model doesn't predict emotion.**
  - Left: '슬프다', Right: '슬퍼요'

<img src="https://i.imgur.com/ZdflZIg.png" width="400"> <img src="https://i.imgur.com/8vG0FNL.png" width="400">

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
  - Low performance than original model (tried: `soynlp`/`soyspacing`)
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
- Better preprocessing
  - Spacing correction
  - Better tokenizing (e.g.) cohesion probablity, etc.)
    - Not stemming
- Other embeddings
  - Fasttext based on consonant-vowel unit
