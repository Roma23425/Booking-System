from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class RoomType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Room(models.Model):
    room_type = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name="rooms"
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError(
                "Дата завершення повинна бути пізніше за дату початку."
            )

        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
            status="confirmed",
        ).exclude(pk=self.pk)

        if overlapping_bookings.exists():
            raise ValidationError("Кімната вже заброньована на цей період.")

    def __str__(self):
        return f"{self.user.username} - {self.room.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username
