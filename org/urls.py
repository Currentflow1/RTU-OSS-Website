from django.urls import path

from . import views


app_name = "org"

urlpatterns = [
    path("", views.home, name="home"),
    path("announcements/<slug:slug>/", views.announcement_detail, name="announcement_detail"),
]