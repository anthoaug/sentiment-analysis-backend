import django.contrib.auth as auth

from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.http import require_GET
from django.contrib.auth.models import User
from django.shortcuts import render


def index(request):
    return render(request, "build/index.html")


def account(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("You're not currently logged in.")

    return HttpResponse(f"You're logged in with the username {request.user.username}.")


@require_GET
def signup(request: HttpRequest):
    # data = json.loads(request.GET)
    #
    # username = data["username"]
    # password = data["password"]

    username = request.GET.get("username")
    password = request.GET.get("password")

    if username is None or password is None:
        return HttpResponseBadRequest("Please supply both a username and password.")

    if User.objects.filter(username=username).exists():
        return HttpResponseBadRequest(f"Username {username} already exists.")

    user = User.objects.create_user(username=username, password=password)

    if user is None:
        return HttpResponseBadRequest(f"Unable to create user with username {username}.")

    return HttpResponse(f"Successfully created user with username {username}.")


@require_GET
def login(request: HttpRequest):
    # data = json.loads(request.body)
    #
    # username = data["username"]
    # password = data["password"]

    username = request.GET.get("username")
    password = request.GET.get("password")

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
