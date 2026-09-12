from django.urls import path
from . import views

app_name = "easter"

urlpatterns = [
  path("", views.game, name="game"),
]