from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from bookings.models import Booking, Location, Resource


def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    today = timezone.localdate()

    total_locations = Location.objects.filter(is_active=True).count()
    total_resources = Resource.objects.filter(is_active=True).count()
    my_active_bookings = Booking.objects.filter(
        user=request.user,
        status="active",
        booking_date__gte=today
    ).count()

    recent_bookings = Booking.objects.filter(
        user=request.user
    ).select_related(
        "resource",
        "resource__location"
    ).order_by("-created_at")[:5]

    context = {
        "total_locations": total_locations,
        "total_resources": total_resources,
        "my_active_bookings": my_active_bookings,
        "recent_bookings": recent_bookings,
    }

    return render(request, "dashboard.html", context)