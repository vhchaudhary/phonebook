from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Contact
from PhoneBook import settings


@receiver(post_save, sender=Contact)
def send_test_mail(sender, instance, created, **kwargs):

    subject = "Contact created successfully"
    body = "Test message for contact"

    email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [instance.email])

    email.send()