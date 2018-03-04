from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime
import pytz
# Create your models here.


@property
def hacker_or_staff(self):
    return self.hacker if hasattr(self, 'hacker') else self.staff


User.add_to_class('hacker_or_staff', hacker_or_staff)


class Settings(models.Model):
    registration_open = models.DateTimeField(auto_now_add=True)
    registration_close = models.DateTimeField(auto_now_add=True)
    confirmation = models.DateTimeField(auto_now_add=True)
    hackathon_start = models.DateTimeField(auto_now_add=True)
    hackathon_end = models.DateTimeField(auto_now_add=True)
    max_hackers = models.IntegerField(default=100)

    @staticmethod
    def get():
        return Settings.objects.first()

    @staticmethod
    def registration_opened():
        op = Settings.get().registration_open
        return timezone.now() > op

    @staticmethod
    def registration_is_open():
        op = Settings.get().registration_open
        ed = Settings.get().registration_close
        return timezone.now() > op and timezone.now() < ed

    @staticmethod
    def hackathon_is_happening():
        op = Settings.get().hackathon_start
        ed = Settings.get().hackathon_end
        return timezone.now() > op and timezone.now() < ed

    @staticmethod
    def hackathon_ended():
        return timezone.now() > Settings.get().hackathon_end

    @staticmethod
    def can_confirm(waitlist=False):
        op = Settings.get().registration_open
        ed = Settings.get().confirmation
        if waitlist:
            ed = ed + datetime.timedelta(days=2)
        return timezone.now() > op and timezone.now() < ed

    @staticmethod
    def hackathon_is_full():
        from hackers.models import Hacker
        m = Settings.get().max_hackers
        c = [None for hacker in Hacker.objects.all() if hacker.is_admitted or hacker.is_confirmed]
        return len(c) > m

    @staticmethod
    def registration_open_seconds():
        return int((Settings.get().registration_open - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)

    @staticmethod
    def registration_close_seconds():
        return int((Settings.get().registration_close - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)

    @staticmethod
    def confirmation_seconds():
        return int((Settings.get().confirmation - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)

    @staticmethod
    def hackathon_start_seconds():
        return int((Settings.get().hackathon_start - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)

    @staticmethod
    def hackathon_end_seconds():
        return int((Settings.get().hackathon_end - datetime.datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000)
