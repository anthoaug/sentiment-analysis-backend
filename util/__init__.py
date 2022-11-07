from util.youtube import CommentData, get_youtube_comments
from util.model import MultinomialBayes, ComplementBayes


def _init_model():
    import json

    with open("../static/model/model.json") as model_file:
        model_config = json.load(model_file)
        return MultinomialBayes(**model_config)


model_instance: MultinomialBayes = _init_model()


def predict_sentiment(text: str) -> str:
    return model_instance.predict(text)


__all__ = [MultinomialBayes, CommentData, model_instance, get_youtube_comments, predict_sentiment]
