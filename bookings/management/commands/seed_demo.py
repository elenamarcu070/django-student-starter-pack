from django.core.management.base import BaseCommand

from bookings.models import Location, Resource


class Command(BaseCommand):
    help = "Create demo locations and resources for the starter pack."

    def handle(self, *args, **options):
        main_campus, _ = Location.objects.get_or_create(
            name="Main Campus",
            defaults={
                "description": "Main university campus demo location.",
                "address": "Demo Street 1",
                "interval_duration_minutes": 60,
                "opening_hour": 8,
                "closing_hour": 20,
                "is_active": True,
            }
        )

        innovation_hub, _ = Location.objects.get_or_create(
            name="Innovation Hub",
            defaults={
                "description": "Modern coworking and project space.",
                "address": "Demo Avenue 25",
                "interval_duration_minutes": 60,
                "opening_hour": 9,
                "closing_hour": 18,
                "is_active": True,
            }
        )

        resources = [
            {
                "location": main_campus,
                "name": "Room A101",
                "resource_type": "room",
                "description": "A modern classroom for courses and seminars.",
                "capacity": 30,
            },
            {
                "location": main_campus,
                "name": "Computer Lab 2",
                "resource_type": "lab",
                "description": "Computer laboratory suitable for programming sessions.",
                "capacity": 24,
            },
            {
                "location": innovation_hub,
                "name": "Conference Room",
                "resource_type": "room",
                "description": "Premium meeting room for presentations and team work.",
                "capacity": 12,
            },
            {
                "location": innovation_hub,
                "name": "3D Printer",
                "resource_type": "equipment",
                "description": "Bookable equipment for student projects.",
                "capacity": 1,
            },
        ]

        for item in resources:
            Resource.objects.get_or_create(
                location=item["location"],
                name=item["name"],
                defaults=item
            )

        self.stdout.write(
            self.style.SUCCESS("Demo data created successfully.")
        )