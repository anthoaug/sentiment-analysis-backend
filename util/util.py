import dataclasses
import pandas

from util.model import MultinomialBayes


@dataclasses.dataclass
class CommentData:
    text: str
    likes: int
    timestamp: pandas.Timestamp


def _init_model():
    import json

    with open("static/model/model.json") as model_file:
        model_config = json.load(model_file)
        return MultinomialBayes(**model_config)


model_instance: MultinomialBayes = _init_model()


def predict_sentiment(text: str) -> str:
    return model_instance.predict(text)
