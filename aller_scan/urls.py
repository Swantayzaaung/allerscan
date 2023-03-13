from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("scan", views.scan, name="scan"),
    path("about", views.about, name="about")
]