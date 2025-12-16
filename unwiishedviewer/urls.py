from django.contrib import admin
from django.urls import include, path, re_path
from .views import *
urlpatterns = [
    re_path(r'stage/(?P<pk>[\d]+)', StageDetailView.as_view(), name="stageviewer"),
    path('stages/',StageListView.as_view(), name="stagelist"),

]