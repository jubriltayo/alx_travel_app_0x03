from rest_framework import viewsets
from rest_framework.response import Response
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_booking_email


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        # creates Booking object using validated data
        booking = serializer.save()

        to_email = 'test@example.com'
        subject = 'Booking Confirmation'
        message = f"""
        Thank you for your booking! 
        
        Booking ID: {booking.booking_id}
        Listing: {booking.listing.name}
        Start Date: {booking.start_date}
        End Date: {booking.end_date}
        Total Price: {booking.total_price}
        Status: {booking.status}
        """

        # trigger the email task asynchronously
        send_booking_email.delay(to_email, subject, message)