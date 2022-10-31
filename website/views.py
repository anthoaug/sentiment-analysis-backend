import datetime

import pandas
import math

from util import CommentData, get_youtube_comments, predict_sentiment
from django.http import HttpResponse, JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the website index.")


def youtube(request, video_id: str):
    comments_dict: dict[str, CommentData] = get_youtube_comments(video_id)

    data = []
    for _, comment_data in comments_dict.items():
        sentiment = predict_sentiment(comment_data.text)

        data.append((
            comment_data.timestamp,
            1 if sentiment == "positive" else 0,
            1 if sentiment == "negative" else 0,
            1 if sentiment == "neutral" else 0
        ))

    df: pandas.DataFrame = pandas.DataFrame(data, columns=["date", "positive", "negative", "neutral"])

    df = df.sort_values(by="date")
    df = df.rolling(pandas.to_timedelta(3, 'D'), on="date").sum()

    data_columns = ["positive", "negative", "neutral"]
    df[data_columns] = df[data_columns].div(df[data_columns].sum(axis=1), axis=0)

    return JsonResponse(df.to_dict('list'))
