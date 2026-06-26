from django.urls import path
from . import views

app_name = "voiceai"

urlpatterns = [
    path("",        views.index,   name="index"),
    path("chat/",   views.chat,    name="chat"),
    path("history/",views.history, name="history"),
]
