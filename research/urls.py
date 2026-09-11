from django.urls import path

from . import views

app_name = "research"

urlpatterns = [
    path("", views.home, name="home"),
    path('search/', views.search, name='search'),

    path("fields/", views.field_list, name="field_list"),
    path("fields/<slug:slug>/", views.field_detail, name="field_detail"),
    path("research/<slug:slug>/", views.research_detail, name="research_detail"),
    path("papers/<int:pk>/", views.paper_detail, name="paper_detail"),
]