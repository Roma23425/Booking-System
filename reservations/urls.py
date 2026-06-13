from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("room/<int:room_id>/", views.room_detail, name="room_detail"),
    path("book/<int:room_id>/", views.create_booking, name="create_booking"),
]
