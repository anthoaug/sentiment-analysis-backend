from abc import abstractmethod, ABC

import collections
import pandas
import string
import numpy
import math
import nltk
import sys


class NaiveBayesModel(ABC):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    tokenizer = nltk.tokenize.casual.TweetTokenizer(preserve_case=False, reduce_len=True)
    lemmatizer = nltk.WordNetLemmatizer()

    def __init__(self, features: dict[str, dict[str, float]] = None, prior_positive: float = 0,
                 prior_negative: float = 0, prior_neutral: float = 0, smooth_positive: float = 0,
                 smooth_negative: float = 0, smooth_neutral: float = 0) -> None:
        if features is None:
            self.features: dict[str, dict[str, float]] = {"positive": {}, "negative": {}, "neutral": {}}
        else:
            self.features: dict[str, dict[str, float]] = features

        self.prior_positive: float = prior_positive
        self.prior_negative: float = prior_negative
        self.prior_neutral: float = prior_neutral

        self.smooth_positive: float = smooth_positive
        self.smooth_negative: float = smooth_negative
        self.smooth_neutral: float = smooth_neutral

    @staticmethod
    def tokenize(text: str) -> list[str]:
        return [
            NaiveBayesModel.lemmatizer.lemmatize(word)
            for word
            in NaiveBayesModel.tokenizer.tokenize(text)
            if word not in NaiveBayesModel.stop_words and word not in string.punctuation
        ]

    @staticmethod
    def default_classifier(sentiment_id, positive, negative, neutral):
        if sentiment_id == 0:
            return neutral
        elif sentiment_id == 1:
            return negative
        elif sentiment_id == 2:
            return positive

        return None

    @staticmethod
    def count(data: pandas.DataFrame, text_label="text", sentiment_label="sentiment", classifier=default_classifier):
        counter_positive = collections.Counter()
        counter_negative = collections.Counter()
        counter_neutral = collections.Counter()

        text: str
        for index, text, sentiment in data[[text_label, sentiment_label]].itertuples():
            words: list[str] = NaiveBayesModel.tokenize(text)
            if len(words) == 0:
                continue

            counter = classifier(sentiment, counter_positive, counter_negative, counter_neutral)
            if counter is None:
                print(f"Invalid sentiment {sentiment} at index {index}.", file=sys.stderr)
                continue

            for word in words:
                counter[word] += 1

        return counter_positive, counter_negative, counter_neutral

    @abstractmethod
    def train(self, data: pandas.DataFrame, text_label="text", sentiment_label="sentiment",
              classifier=default_classifier) -> None:
        pass

    @abstractmethod
    def predict(self, text: str) -> str:
        pass


class MultinomialBayes(NaiveBayesModel):
    def train(self, data: pandas.DataFrame, text_label="text", sentiment_label="sentiment",
              classifier=NaiveBayesModel.default_classifier) -> None:

        counter_positive, counter_negative, counter_neutral = self.count(data, text_label, sentiment_label, classifier)

        total_positive = counter_positive.total()
        total_negative = counter_negative.total()
        total_neutral = counter_neutral.total()
        total_documents = total_positive + total_negative + total_neutral

        self.prior_positive = math.log(total_positive / total_documents)
        self.prior_negative = math.log(total_negative / total_documents)
        self.prior_neutral = math.log(total_neutral / total_documents)

        self.smooth_positive = -math.log(total_documents + 3)
        for word, count in counter_positive.items():
            self.features["positive"][word] = math.log(count + 1) + self.smooth_positive

        self.smooth_negative = -math.log(total_documents + 3)
        for word, count in counter_negative.items():
            self.features["negative"][word] = math.log(count + 1) + self.smooth_negative

        self.smooth_neutral = -math.log(total_documents + 3)
        for word, count in counter_neutral.items():
            self.features["neutral"][word] = math.log(count + 1) + self.smooth_neutral

    def predict(self, text: str) -> str:
        words = self.tokenize(text)

        prob_positive = self.prior_positive
        prob_negative = self.prior_negative
        prob_neutral = self.prior_neutral
        for word in words:
            positive = word in self.features["positive"]
            negative = word in self.features["negative"]
            neutral = word in self.features["neutral"]

            if positive:
                prob_positive += self.features["positive"][word]
            elif negative or neutral:
                prob_positive += self.smooth_positive

            if negative:
                prob_negative += self.features["negative"][word]
            elif positive or neutral:
                prob_negative += self.smooth_negative

            if neutral:
                prob_neutral += self.features["neutral"][word]
            elif positive or negative:
                prob_neutral += self.smooth_neutral

        return ["positive", "negative", "neutral"][numpy.argmax([prob_positive, prob_negative, prob_neutral])]


# TODO: Fix. Accuracy is extremely low compared to multinomial, so likely there's a significant mistake impacting accuracy.
class ComplementBayes(NaiveBayesModel):
    def train(self, data: pandas.DataFrame, text_label="text", sentiment_label="sentiment",
              classifier=NaiveBayesModel.default_classifier) -> None:
        counter_positive, counter_negative, counter_neutral = self.count(data, text_label, sentiment_label, classifier)

        total_positive = counter_positive.total()
        total_negative = counter_negative.total()
        total_neutral = counter_neutral.total()
        total_documents = total_positive + total_negative + total_neutral

        self.prior_positive = math.log(total_positive / total_documents)
        self.prior_negative = math.log(total_negative / total_documents)
        self.prior_neutral = math.log(total_neutral / total_documents)

        self.smooth_positive = math.log(total_negative + total_neutral + 3)
        for word, count in counter_positive.items():
            self.features["positive"][word] = self.smooth_positive - math.log(
                counter_negative[word] + counter_neutral[word] + 1)

        self.smooth_negative = math.log(total_positive + total_neutral + 3)
        for word, count in counter_negative.items():
            self.features["negative"][word] = self.smooth_negative - math.log(
                counter_positive[word] + counter_neutral[word] + 1)

        self.smooth_neutral = math.log(total_positive + total_negative + 3)
        for word, count in counter_neutral.items():
            self.features["neutral"][word] = self.smooth_neutral - math.log(
                counter_positive[word] + counter_negative[word] + 1)

    def predict(self, text: str) -> str:
        words = self.tokenize(text)

        prob_positive = self.prior_positive
        prob_negative = self.prior_negative
        prob_neutral = self.prior_neutral
        for word in words:
            positive = word in self.features["positive"]
            negative = word in self.features["negative"]
            neutral = word in self.features["neutral"]

            if positive:
                prob_positive += self.features["positive"][word]
            elif negative or neutral:
                prob_positive += self.smooth_positive

            if negative:
                prob_negative += self.features["negative"][word]
            elif positive or neutral:
                prob_negative += self.smooth_negative

            if neutral:
                prob_neutral += self.features["neutral"][word]
            elif positive or negative:
                prob_neutral += self.smooth_neutral

        return ["positive", "negative", "neutral"][numpy.argmin([prob_positive, prob_negative, prob_neutral])]
