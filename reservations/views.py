from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Room, Booking
from .forms import BookingForm


def home(request):
    rooms = Room.objects.all()
    return render(request, "home.html", {"rooms": rooms})


def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, "room_detail.html", {"room": room})


@login_required
def create_booking(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user

            overlap = Booking.objects.filter(
                room=room,
                start_time__lt=booking.end_time,
                end_time__gt=booking.start_time,
                status="confirmed",
            )

            if overlap.exists():
                messages.error(request, "Ця кімната вже заброньована на вибраний час.")
            else:
                booking.save()
                messages.success(request, "Бронювання успішно створено.")
                return redirect("home")

    else:
        form = BookingForm()

    return render(request, "booking_form.html", {"form": form, "room": room})


def search_rooms(request):
    rooms = Room.objects.all()

    name = request.GET.get("name")
    capacity = request.GET.get("capacity")
    price = request.GET.get("price")

    if name:
        rooms = rooms.filter(name__icontains=name)

    if capacity:
        rooms = rooms.filter(capacity__gte=capacity)

    if price:
        rooms = rooms.filter(price__lte=price)

    return render(request, "search.html", {"rooms": rooms})


@login_required
def dashboard(request):

    bookings = Booking.objects.filter(user=request.user).order_by("-start_time")

    return render(request, "dashboard.html", {"bookings": bookings})
