
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Order, OrderItem

@receiver(post_save, sender=OrderItem)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    if created:
        order = instance.order
        total_price = order.get_total_price  # Calculate after items are added
        
        # Build the order items summary
        items_summary = ""
        for item in order.items.all():
            items_summary += f"- {item.product.title}: {item.quantity} x €{item.price} = €{item.get_cost()}\n"

        subject = f"Conferma d'ordine - ID: {order.id}"
        message = (
            f"Gentile {order.user.full_name},\n\n"
            f"Grazie per il tuo ordine!\n\n"
            f"Riepilogo del tuo ordine:\n"
            f"{items_summary}\n"
            f"Totale: €{total_price}\n\n"
            f"Saluti,\nIl Team"
        )
        recipient_email = order.user.email
        
        send_mail(
            subject,
            message,
            'no-reply@clc.shop',  # Mittente
            [recipient_email],  # Indirizzo destinatario
            fail_silently=False,
        )