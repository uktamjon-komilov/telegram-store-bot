from django.urls import path
from . import views

urlpatterns = [
    path("bot/", views.main),
    path("", views.stats),
    path("data/", views.pivot_data, name="pivot_data"),
]