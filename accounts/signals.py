from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User

@receiver(post_save, sender=User)
def send_account_confirmation_email(sender, instance, created, **kwargs):
    if created:
        subject = "Benvenuto su CLC Shop!"
        message = f"Caro {instance.full_name},\n\n" \
                  f"Il tuo account è stato creato con successo.\n" \
                  f"Siamo entusiasti di averti con noi!\n\n" \
                  f"Saluti,\nIl Team CLC Shop"
        recipient_email = instance.email

        send_mail(
            subject,
            message,
            'no-reply@clc.shop', 
            [recipient_email],
            fail_silently=False,
        )
