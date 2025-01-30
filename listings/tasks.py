from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_booking_email(to_email, subject, message):
    """
    Send a booking confirmation email asynchronously
    """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [to_email]
    
    send_mail(subject, message, email_from, recipient_list)