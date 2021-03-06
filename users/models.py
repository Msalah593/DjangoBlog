from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.db.models import signals
from rest_framework.authtoken.models import Token
from smtplib import SMTPException
import logging
from django.contrib.sites.models import Site

logger = logging.getLogger('send_email')


class CustomUser(AbstractUser):
    email = models.EmailField(('email address'), blank=False, unique=True,
                              error_messages={
        'unique': ("A user with that mail already exists."),
    })
    is_active = models.BooleanField(('active'), default=False,
                                    help_text=('''Designates whether this 
                                        user should be treated as
                                        active. Unselect this instead
                                        of deleting accounts.'''))  # noqa


@receiver(signals.post_save, sender=CustomUser)
def user_created_signal(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
        if not instance.is_active:
            token = default_token_generator.make_token(instance)
            username_hash = urlsafe_base64_encode(
                force_bytes(instance.username))
            subject = 'activate your acccount !'
            mail = instance.email
            hostname = Site.objects.get_current().domain
            url = (
                '/').join(['https:/', hostname, 'users/validate',
                           str(username_hash), token])
            print(url)
            msg = 'Hi ' + instance.username + \
                'please follow the below link to activate your account\n' + url
            try:
                send_mail(subject, msg, 'Blog@server.com',
                          [mail])
            except SMTPException as e:
                logger.error('Error sending confirmation email: %s', e)
