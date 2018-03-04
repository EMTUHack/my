from __future__ import absolute_import, unicode_literals
from main.email import notify_admitted, notify_decline, notify_waitlist, notify_unwaitlist, verify_email
from celery import shared_task


@shared_task
def send_notify_admitted(hacker_id):
    from .models import Hacker
    hacker = Hacker.objects.get(id=hacker_id)
    return notify_admitted(hacker)


@shared_task
def send_notify_decline(hacker_id):
    from .models import Hacker
    hacker = Hacker.objects.get(id=hacker_id)
    return notify_decline(hacker)


@shared_task
def send_notify_waitlist(hacker_id):
    from .models import Hacker
    hacker = Hacker.objects.get(id=hacker_id)
    return notify_waitlist(hacker)


@shared_task
def send_notify_unwaitlist(hacker_id):
    from .models import Hacker
    hacker = Hacker.objects.get(id=hacker_id)
    return notify_unwaitlist(hacker)


@shared_task
def send_verify_email(hacker_id):
    from .models import Hacker
    hacker = Hacker.objects.get(id=hacker_id)
    return verify_email(hacker)
