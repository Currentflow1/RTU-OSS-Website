from django.urls import path

from org import views as org_views
from . import views

app_name = "research"

urlpatterns = [
  path("", views.home, name="home"),
  path("admin/", views.admin_dashboard, name="admin_dashboard"),

  path("fields/", views.field_list, name="field_list"),
  path("fields/<slug:slug>/", views.field_detail, name="field_detail"),
  path("research/<slug:slug>/", views.research_detail, name="research_detail"),
  path("papers/<int:pk>/", views.paper_detail, name="paper_detail"),
  path("papers/<int:pk>/file/", views.paper_file, name="paper_file"),
  path("search/", views.search, name="search"),

  path("submit/", views.research_submit, name="research_submit"),
  path("submit/success/", views.submission_success, name="submission_success"),

  path("admin/submissions/", views.admin_submission_list, name="admin_submission_list"),
  path("admin/submissions/<int:pk>/", views.admin_submission_detail, name="admin_submission_detail"),
  path("admin/submissions/<int:pk>/approve/", views.admin_submission_approve, name="admin_submission_approve"),
  path("admin/submissions/<int:pk>/reject/", views.admin_submission_reject, name="admin_submission_reject"),

  path("admin/announcements/", org_views.admin_announcement_list, name="admin_announcement_list"),
  path("admin/announcements/create/", org_views.admin_announcement_create, name="admin_announcement_create"),
  path("admin/announcements/<int:pk>/edit/", org_views.admin_announcement_edit, name="admin_announcement_edit"),
  path("admin/announcements/<int:pk>/delete/", org_views.admin_announcement_delete, name="admin_announcement_delete"),
]
