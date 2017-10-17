from mailchimp3 import MailChimp
from django.conf import settings
import hashlib
from requests.exceptions import HTTPError


client = MailChimp(settings.MAILCHIMP_USER, settings.MAILCHIMP_SECRET)


def md5(email):
    return hashlib.md5(email.encode('utf-8')).hexdigest()


def add_subscriber(l, hacker):
    if l is None:
        return
    merge_fields = {
        'FNAME': hacker.first_name,
        'LNAME': hacker.last_name,
        'TOKEN': hacker.token
    }
    email = hacker.email
    hash_email = md5(hacker.email)
    data = {"email_address": email, "merge_fields": merge_fields, "status_if_new": "subscribed"}
    client.lists.members.create_or_update(list_id=l, subscriber_hash=hash_email, data=data)


def remove_subscriber(l, hacker):
    if l is None:
        return
    hash_email = md5(hacker.email)
    try:
        client.lists.members.delete(list_id=l, subscriber_hash=hash_email)
    except HTTPError:
        print("Subscriber not found!")


def batch_confirm(hackers):
    for h in hackers:
        remove_subscriber(settings.MAILCHIMP_LIST_PRE, h)
        add_subscriber(settings.MAILCHIMP_LIST_CONFIRMED, h)
