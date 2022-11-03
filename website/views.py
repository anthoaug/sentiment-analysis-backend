import pandas

from util import CommentData, get_youtube_comments, predict_sentiment
from django.http import HttpResponse, JsonResponse

WEEK_INTERVAL = pandas.to_timedelta(arg=7, unit='D')
MONTH_INTERVAL = pandas.to_timedelta(arg=30, unit='D')
YEAR_INTERVAL = pandas.to_timedelta(arg=365, unit='D')


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

    df_all: pandas.DataFrame = df[["positive", "negative", "neutral"]].expanding().sum()
    df_week: pandas.DataFrame = df.rolling(WEEK_INTERVAL, on="date").sum()[["positive", "negative", "neutral"]]
    df_month: pandas.DataFrame = df.rolling(MONTH_INTERVAL, on="date").sum()[["positive", "negative", "neutral"]]
    df_year: pandas.DataFrame = df.rolling(YEAR_INTERVAL, on="date").sum()[["positive", "negative", "neutral"]]

    return JsonResponse({
        "absolute": {
            "all": df_all.to_dict('list'),
            "week": df_week.to_dict('list'),
            "month": df_month.to_dict('list'),
            "year": df_year.to_dict('list')
        },
        "relative": {
            "all": df_all.div(df_all.sum(axis=1), axis=0).to_dict('list'),
            "week": df_week.div(df_week.sum(axis=1), axis=0).to_dict('list'),
            "month": df_month.div(df_month.sum(axis=1), axis=0).to_dict('list'),
            "year": df_year.div(df_year.sum(axis=1), axis=0).to_dict('list'),
        },
        "timestamps": df["date"].tolist()
    })
