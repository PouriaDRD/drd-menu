from django.http import HttpRequest, HttpResponse

from core.app_config import config

APP_NAME = config.app.app_name


def index(request: HttpRequest):
    return HttpResponse(f"Welcome to {APP_NAME}!")
