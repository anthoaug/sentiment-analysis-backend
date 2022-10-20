from util import get_youtube_comments
import random

from django.http import HttpResponse, HttpRequest, JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the extension index.")


def youtube(request: HttpRequest, video_id: str):
    comments_dict: dict[str, tuple[str, int]] = get_youtube_comments(video_id)

    sentiments: dict[str, str] = {}
    for comment_id, _ in comments_dict.items():
        sentiments[comment_id] = random.choice(["positive", "negative", "neutral"])

    return JsonResponse(sentiments)
