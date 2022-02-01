from .serializers import UserSerializer
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from config import settings


User = get_user_model()


    
@receiver(post_save, sender=User)
def notification(sender, instance, created, **kwargs):
    if created:
        
        subject = "ACCOUNT VERIFICATION FOR SMART PARCEL"
        
        message = f"""Hi, {str(instance.first_name).title()}.
Welcome to ideathinkers test app. Here we pride ourselves in build the best software solutions for our client!

Welcome on board!!!

Thank you,
Desmond             
"""   
       
        
        email_from = settings.Common.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail( subject, message, email_from, recipient_list)
        
        return
    
 