from django.conf import settings
from django.db import models
from django.utils import timezone


class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    interval_duration_minutes = models.PositiveIntegerField(default=60)
    opening_hour = models.PositiveIntegerField(default=8)
    closing_hour = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Resource(models.Model):
    RESOURCE_TYPES = [
        ("room", "Room"),
        ("lab", "Laboratory"),
        ("equipment", "Equipment"),
        ("desk", "Desk"),
        ("other", "Other"),
    ]

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="resources"
    )
    name = models.CharField(max_length=100)
    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPES,
        default="room"
    )
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="resources/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["location__name", "name"]

    def __str__(self):
        return f"{self.name} - {self.location.name}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["booking_date", "start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["resource", "booking_date", "start_time", "end_time"],
                condition=models.Q(status="active"),
                name="unique_active_booking_per_resource_slot"
            )
        ]

    def __str__(self):
        return f"{self.resource.name} | {self.booking_date} | {self.start_time}-{self.end_time}"

    @property
    def is_past(self):
        booking_end = timezone.datetime.combine(
            self.booking_date,
            self.end_time
        )
        booking_end = timezone.make_aware(booking_end)
        return booking_end < timezone.now()