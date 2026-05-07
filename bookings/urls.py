from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.resource_list, name="resource_list"),
    path("resource/<int:resource_id>/", views.resource_detail, name="resource_detail"),
    path("book/<int:resource_id>/", views.create_booking, name="create_booking"),
    path("cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
]