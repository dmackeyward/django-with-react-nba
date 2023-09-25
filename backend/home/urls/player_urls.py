from django.urls import path
from home.views import player_views as views

urlpatterns = [
    path("<str:pk>", views.getPlayerByName, name="player"),
]