from django.shortcuts import render, redirect
from .models import Room, Booking
from .forms import BookingForm


def home(request):
    rooms = Room.objects.all()
    return render(request, "home.html", {"rooms": rooms})


def room_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    return render(request, "room_detail.html", {"room": room})


def create_booking(request, room_id):
    room = Room.objects.get(id=room_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.save()
            return redirect("home")
    else:
        form = BookingForm()

    return render(request, "booking_form.html", {"form": form, "room": room})
