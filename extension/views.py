from util import CommentData, get_youtube_comments, youtube_model, twitter_model
from django.http import HttpResponse, HttpRequest, JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the extension index.")


def youtube(request: HttpRequest, video_id: str):
    comments_dict: dict[str, CommentData] = get_youtube_comments(video_id)

    counts: dict[str, int] = {"positive": 0, "negative": 0, "neutral": 0}
    sentiments: dict[str, str] = {}
    for comment_id, data in comments_dict.items():
        sentiment = youtube_model.predict(data.text)

        sentiments[comment_id] = sentiment
        counts[sentiment] += 1

    return JsonResponse({"sentiments": sentiments, "counts": counts})


def twitter(request: HttpRequest, reply_text: str):
    return HttpResponse(twitter_model.predict(reply_text))
