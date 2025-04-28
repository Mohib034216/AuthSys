from django.core.mail import send_mail
# from django.conf import os
from django.conf import settings
 
def send_simple_email(subject, message, recipient_list, from_email=None):
    try:
       send_mail(
                    subject,
                    message,
                    from_email or settings.EMAIL_HOST_USER,
                    recipient_list,
                    fail_silently=False,
                    )
      
    except Exception:
        return f'something is wrong error'
    return 'done'
