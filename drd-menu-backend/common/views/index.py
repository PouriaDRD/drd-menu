from django.http import HttpResponse, HttpRequest
from config.app_config import config

APP_NAME = config.app.app_name


def index(request: HttpRequest):
    return HttpResponse(
        f"<h1>Welcome to {APP_NAME}!</h1><p>This is the index page of the application.</p>"
    )
