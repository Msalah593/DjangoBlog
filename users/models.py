from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
# Create your models here.
from django.db.models import signals
class CustomUser(AbstractUser):
    email = models.EmailField(('email address'), blank=False)
    is_active = models.BooleanField(('active'), default=False,
        help_text=('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    def __str__(self):
        return self.email

@receiver(signals.post_save,sender=CustomUser)
def user_created_signal(sender,instance,created,**kwargs):
    if created:
        if not instance.is_active:
            print(instance.username,instance.email)
            token = default_token_generator.make_token(instance)
            username_hash = urlsafe_base64_encode(force_bytes(instance.username))
            print(token,username_hash)

