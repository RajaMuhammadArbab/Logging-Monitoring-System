from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .utils import log_activity

@receiver(user_logged_in)
def on_login(sender, request, user, **kwargs):
    if request:
        log_activity(request, action='login', status_code=200)

@receiver(user_logged_out)
def on_logout(sender, request, user, **kwargs):
    if request:
        log_activity(request, action='logout', status_code=200)
