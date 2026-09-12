from django.urls import path

from . import views


app_name = "org"

urlpatterns = [
    path("", views.home, name="home"),
    path("announcements/<slug:slug>/", views.announcement_detail, name="announcement_detail"),

    path("admin/announcements/", views.admin_announcement_list, name="admin_announcement_list"),
    path("admin/announcements/create/", views.admin_announcement_create, name="admin_announcement_create"),
    path("admin/announcements/<int:pk>/edit/", views.admin_announcement_edit, name="admin_announcement_edit"),
    path("admin/announcements/<int:pk>/delete/", views.admin_announcement_delete, name="admin_announcement_delete"),
]