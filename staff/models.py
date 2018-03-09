from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
# Create your models here.


TOKEN_SIZE = settings.TOKEN_SIZE


@property
def is_staff_member(self):
    return hasattr(self, 'staff') or self.is_superuser


User.add_to_class('is_staff_member', is_staff_member)


class Staff(models.Model):
    """docstring for Hacker"""

    user = models.OneToOneField(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    # Basic info
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=20, unique=True, null=True, blank=True)
    active = models.BooleanField(default=False)

    # Social Login
    fb_social_id = models.CharField(max_length=50, null=True, blank=True, unique=True)
    gh_social_id = models.CharField(max_length=50, null=True, blank=True, unique=True)

    @property
    def has_fb_login(self):
        return self.fb_social_id is not None and self.fb_social_id != ''

    @property
    def has_gh_login(self):
        return self.gh_social_id is not None and self.gh_social_id != ''

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def new_token(self):
        from hackers.models import Hacker
        token = get_random_string(length=TOKEN_SIZE)
        if Staff.objects.filter(token=token).first() is not None or Hacker.objects.filter(token=token).first() is not None:
            return self.new_token()
        self.token = token
        self.save()
        return self.token

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


# Process staff creation
@receiver(post_save, sender=Staff, dispatch_uid="staff_creation")
def staff_creation(sender, instance, **kwargs):
    if kwargs['created']:
        instance.new_token()
        if getattr(instance, 'user', None) is None:
            user = User(
                username=instance.email,
                email=instance.email,
                password=get_random_string(length=12)
            )
            user.set_unusable_password()
            user.save()
            instance.user = user
        instance.save()
