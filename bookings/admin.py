from django.contrib import admin
from .models import Location, Resource, Booking


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "address",
        "interval_duration_minutes",
        "opening_hour",
        "closing_hour",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "address")


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
        "resource_type",
        "capacity",
        "is_active",
    )
    list_filter = ("location", "resource_type", "is_active")
    search_fields = ("name", "location__name")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "resource",
        "user",
        "booking_date",
        "start_time",
        "end_time",
        "status",
        "created_at",
    )
    list_filter = ("status", "booking_date", "resource__location")
    search_fields = (
        "resource__name",
        "user__username",
        "user__email",
    )