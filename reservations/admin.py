from django.contrib import admin
from .models import RoomType, Room, Booking, UserProfile

admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(UserProfile)
