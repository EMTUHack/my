from django.db import models
from hackers.models import Hacker
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
import pytz
import locale
now = timezone.localtime(timezone.now())
local = pytz.timezone(str(now.tzinfo))
# locale.setlocale(locale.LC_TIME, "pt_BR")
# Create your models here.


EVENT_TYPES = (
    ('Workshop', 'Workshop'),
    ('Palestra', 'Palestra'),
    ('Tech Talk', 'Tech Talk'),
    ('Refeição', 'Refeição'),
    ('Meta', 'Meta')
)


class Event(models.Model):

    # Basic
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    kind = models.CharField(max_length=30, choices=EVENT_TYPES)
    requires_registration = models.BooleanField(default=False)

    # Specific
    speaker = models.CharField(max_length=100, blank=True, null=True)
    speaker_description = models.TextField(blank=True, null=True)
    max_attendees = models.IntegerField(blank=True, null=True)

    @property
    def is_past(self):
        return self.starts < now

    @property
    def hackers(self):
        return [h.hacker for h in self.attendees.all()]

    @property
    def human_time(self):
        return self.starts.astimezone(now.tzinfo).strftime('%a, %H:%M')

    def is_hacker_registered(self, hacker):
        return self.attendees.filter(hacker=hacker).exists()

    def register_attendee(self, hacker):
        # Check if event is not past
        if self.is_past:
            return None, 'Evento já começou!'
        if self.max_attendees is not None and self.attendees.all().count() >= self.max_attendees:
            return None, 'Evento lotado!'
        # check if already is
        if self.is_hacker_registered(hacker):
            return self.attendees.get(hacker=hacker), ''
        attendee = Attendee(
            hacker=hacker,
            event=self
        )
        attendee.save()
        return attendee, ''

    def unregister_attendee(self, hacker):
        if self.is_hacker_registered(hacker):
            att = self.attendees.get(hacker=hacker)
            att.delete()

    def toggle_attendee(self, hacker):
        if self.is_hacker_registered(hacker):
            self.unregister_attendee(hacker)
            return False, ''
        else:
            return self.register_attendee(hacker)

    def rate_event(self, hacker, rating, feedback):
        if not self.is_hacker_registered(hacker):
            return None
        attendee = self.attendees.get(hacker=hacker)
        attendee.rating = rating
        attendee.feedback = feedback
        attendee.save()
        return attendee

    def __str__(self):
        return "{}({}) @ {}".format(self.name, self.kind, self.starts.astimezone(now.tzinfo))


class Attendee(models.Model):
    hacker = models.ForeignKey(Hacker, related_name='events_attended', null=True)
    event = models.ForeignKey(Event, related_name='attendees')
    rating = models.IntegerField(blank=True, null=True)
    feedback = models.CharField(max_length=200, blank=True, null=True, default="")


@receiver(pre_save, sender=Event, dispatch_uid="pre_save_event")
def pre_save_event(sender, instance, **kwargs):
    print(instance.starts)
    instance.starts = instance.starts.replace(tzinfo=now.tzinfo)
    instance.ends = instance.ends.replace(tzinfo=now.tzinfo)
    print(instance.starts)
