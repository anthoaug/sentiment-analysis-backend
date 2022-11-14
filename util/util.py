import dataclasses
import pandas

from util.model import MultinomialBayes


@dataclasses.dataclass
class CommentData:
    text: str
    likes: int
    timestamp: pandas.Timestamp


def _init_model(config: str):
    import json

    with open(config) as model_file:
        model_config = json.load(model_file)
        return MultinomialBayes(**model_config)


youtube_model: MultinomialBayes = _init_model("static/model/youtube_model.json")
twitter_model: MultinomialBayes = _init_model("static/model/twitter_model.json")
