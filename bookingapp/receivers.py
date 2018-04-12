from django.dispatch import receiver
from .signals import *

#use decorator to telldesignate the send_mail_on_publish function as the receiver
# for the book_published signal

@receiver(book_published)
def send_mail_on_publish(sender, **kwargs):
    # contains the logic to send the email to author.
    print('receiver fired')