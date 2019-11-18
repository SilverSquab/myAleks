from .models import *

def send_notification(receiver, msg, sender=None, msg_type=None):
    n = Notification(receiver = receiver, msg = msg)
    if sender:
        n.sender = sender
    if msg_type:
        n.msg_type = msg_type
    n.save()
