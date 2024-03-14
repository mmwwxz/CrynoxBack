from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import LeadSupport
from .utils import send_support_completion_email
from datetime import timedelta


@receiver(post_save, sender=LeadSupport)
def send_support_completion_notification(sender, instance, created, **kwargs):
    if created:
        lead = instance.lead
        today = timezone.now().date()
        if instance.testing.date() <= today and instance.updating.date() <= today:
            send_support_completion_email(lead)
            send_support_completion_email(lead, is_admin=True)
