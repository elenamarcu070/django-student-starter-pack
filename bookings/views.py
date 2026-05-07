from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Booking, Location, Resource


def generate_time_slots(opening_hour, closing_hour, duration_minutes):
    slots = []

    current = datetime.strptime(f"{opening_hour}:00", "%H:%M")
    end = datetime.strptime(f"{closing_hour}:00", "%H:%M")

    while current < end:
        slot_start = current.time()
        current += timedelta(minutes=duration_minutes)
        slot_end = current.time()

        if current <= end:
            slots.append((slot_start, slot_end))

    return slots


@login_required
def resource_list(request):
    query = request.GET.get("q", "")
    location_id = request.GET.get("location", "")
    resource_type = request.GET.get("type", "")

    resources = Resource.objects.filter(is_active=True).select_related("location")

    if query:
        resources = resources.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(location__name__icontains=query)
        )

    if location_id:
        resources = resources.filter(location_id=location_id)

    if resource_type:
        resources = resources.filter(resource_type=resource_type)

    locations = Location.objects.filter(is_active=True)

    user_bookings = Booking.objects.filter(
        user=request.user,
        status="active",
        booking_date__gte=timezone.localdate()
    ).select_related("resource", "resource__location")

    context = {
        "resources": resources,
        "locations": locations,
        "user_bookings": user_bookings,
        "query": query,
        "selected_location": location_id,
        "selected_type": resource_type,
        "resource_types": Resource.RESOURCE_TYPES,
    }

    return render(request, "bookings/resource_list.html", context)


@login_required
def resource_detail(request, resource_id):
    resource = get_object_or_404(
        Resource.objects.select_related("location"),
        id=resource_id,
        is_active=True
    )

    selected_date_raw = request.GET.get("date")

    if selected_date_raw:
        selected_date = datetime.strptime(selected_date_raw, "%Y-%m-%d").date()
    else:
        selected_date = timezone.localdate()

    slots = generate_time_slots(
        opening_hour=resource.location.opening_hour,
        closing_hour=resource.location.closing_hour,
        duration_minutes=resource.location.interval_duration_minutes
    )

    existing_bookings = Booking.objects.filter(
        resource=resource,
        booking_date=selected_date,
        status="active"
    ).select_related("user")

    booked_slots = {
        (booking.start_time, booking.end_time): booking
        for booking in existing_bookings
    }

    now = timezone.localtime()
    slot_data = []

    for start_time, end_time in slots:
        booking = booked_slots.get((start_time, end_time))

        slot_end_datetime = timezone.make_aware(
            datetime.combine(selected_date, end_time)
        )

        slot_data.append({
            "start_time": start_time,
            "end_time": end_time,
            "booking": booking,
            "is_booked": booking is not None,
            "is_past": slot_end_datetime < now,
            "is_mine": booking.user == request.user if booking else False,
        })

    context = {
        "resource": resource,
        "selected_date": selected_date,
        "slot_data": slot_data,
    }

    return render(request, "bookings/resource_detail.html", context)


@login_required
def create_booking(request, resource_id):
    if request.method != "POST":
        return redirect("bookings:resource_detail", resource_id=resource_id)

    resource = get_object_or_404(Resource, id=resource_id, is_active=True)

    booking_date = request.POST.get("booking_date")
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")
    notes = request.POST.get("notes", "")

    if not booking_date or not start_time or not end_time:
        messages.error(request, "Invalid booking data.")
        return redirect("bookings:resource_detail", resource_id=resource.id)

    booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
    start_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
    end_time_obj = datetime.strptime(end_time, "%H:%M:%S").time()

    slot_end_datetime = timezone.make_aware(
        datetime.combine(booking_date_obj, end_time_obj)
    )

    if slot_end_datetime < timezone.now():
        messages.error(request, "You cannot book a past time slot.")
        return redirect(f"/bookings/resource/{resource.id}/?date={booking_date}")

    already_booked = Booking.objects.filter(
        resource=resource,
        booking_date=booking_date_obj,
        start_time=start_time_obj,
        end_time=end_time_obj,
        status="active"
    ).exists()

    if already_booked:
        messages.error(request, "This time slot is already booked.")
        return redirect(f"/bookings/resource/{resource.id}/?date={booking_date}")

    Booking.objects.create(
        user=request.user,
        resource=resource,
        booking_date=booking_date_obj,
        start_time=start_time_obj,
        end_time=end_time_obj,
        status="active",
        notes=notes
    )

    messages.success(request, "Booking created successfully.")
    return redirect("bookings:resource_list")


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        status="active"
    )

    booking.status = "cancelled"
    booking.save()

    messages.success(request, "Booking cancelled successfully.")
    return redirect("bookings:resource_list")