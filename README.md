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
  - [gensim(Word2Vec/Doc2Vec)](https://radimrehurek.com/gensim/)
  - [scikit-learn](http://scikit-learn.org/stable/)
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
| Noise [Joy] | 이 시대에 사람의 마음을 한편의 그림으로 표현하는게 정말 아름다웠고 대단했다. |
| Noise | 이모 죽을때 5초도 안슬퍼하네 |
| Noise | 삶의소중함을 만화를 보고 깨닫다니... |
| Noise [Disappoint] | 재미는 분명히 있지만 좀 더 치밀하지 못한 스토리 라인이 아쉽다. |
| Noise [Joy] | 미국인들은 이 영화를 보면서 무슨 생각을 할지 궁금.. 많은 생각을 하게 해주는 영화. 연기, 연출, 촬영, 메세지, 시나리오, 음악, 절제된 액션, 서정적인 라스트씬까지.. 거의 완벽에 가까운 웰메이드 서부 역사극. |
| Noise [Disappoint] | 암울한 히어로물... 시기가 일렀나 |
| Noise | 내삶은 지금 몇회일까? |
| Noise | 이 영화는 단 '1'만큼도 감정적인부분이없이 그저 팩트, 팩트, 팩트로 이어집니다.대한민국 국민이라면 꼭 봐야하는 영화라고 생각하며, 해외 영화제마다 다 나가서 전세계적으로 알려야한다고 생각합니다. |
| Noise [Joy] | 어릴 때 엄마랑 봤던 기억을 더듬어 재발견 한 주옥같은 영화. 10번 이상은 돌려봤을 정도로 볼 때마다 유쾌한 영화!! 요즘 사람들한테 잘 알려지진 않았지만 90년대 영화 중엔 이런 숨겨진 옥구슬들이 꽤 있다! 90년대 특유의 유쾌하고 가벼운 감성 |
| Noise [Joy] | 어린시절 너무 재밌게 봤어요.. |


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
