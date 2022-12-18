import django.contrib.auth as auth
import json
import re

from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from util import get_channel_id, get_videos
from website.models import FollowedUsers
from django.shortcuts import render


@ensure_csrf_cookie
def index(request):
    return render(request, "index.html")


def session(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("You're not currently logged in.")

    return HttpResponse(f"You're logged in with the username {request.user.username}.")


@require_POST
def register(request: HttpRequest):
    data = json.loads(request.body)

    username: str = data["username"]
    password: str = data["password"]

    if username is None or password is None:
        return HttpResponseBadRequest("Please supply both a username and password.")

    if not re.fullmatch(r"\w+", username):
        return HttpResponseBadRequest(f"Invalid username '{username}'. Use only letters, numbers and underscores.")

    if User.objects.filter(username=username).exists():
        return HttpResponseBadRequest(f"Username '{username}' already exists.")

    user = User.objects.create_user(username=username, password=password)

    if user is None:
        return HttpResponseBadRequest(f"Unable to create user with username '{username}'.")

    followed_users = FollowedUsers(user=user)
    followed_users.save()

    auth.login(request, user)

    return HttpResponse(f"Successfully created and signed in user with username '{username}'.")


@require_POST
def login(request: HttpRequest):
    data = json.loads(request.body)

    username = data["username"]
    password = data["password"]

    if username is None or password is None:
        return HttpResponseBadRequest("Please supply both a username and password.")

    user = auth.authenticate(username=username, password=password)

    if user is None:
        return HttpResponseBadRequest("Invalid username or password.")

    auth.login(request, user)

    return HttpResponse("Succesfully logged in.")


def logout(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("You're not currently logged in.")

    auth.logout(request)

    return HttpResponse("Successfully logged out.")


@require_POST
def add_follower(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("You're not currently logged in.")

    data = json.loads(request.body)

    username: str = data["username"]

    if username is None:
        return HttpResponseBadRequest("Please supply a username to follow.")

    followed = request.user.followed_users.followed
    # if username in followed:
    #     return HttpResponseBadRequest(f"You already follow '{username}'.")

    channel_id: str = get_channel_id(username)
    if channel_id is None:
        return HttpResponseBadRequest("Invalid username.")

    followed[username] = channel_id

    request.user.followed_users.save()

    print(request.user.followed_users.followed)

    return HttpResponse("Success!")


def get_feed(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("You're not currently logged in.")

    followed = request.user.followed_users.followed

    for username, channel_id in followed.items():
        print(username, channel_id)
        get_videos(channel_id)

    return HttpResponse("Test.")
