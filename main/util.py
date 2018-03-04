from hackers.models import Hacker
from .models import Settings


def cycle_waitlist(max_iterations=1, hackers=None):
    hackers = hackers if hackers is not None else list(Hacker.objects.filter(waitlist=True).order_by('waitlist_date'))
    if not Settings.hackathon_is_full() and max_iterations > 0 and len(hackers) > 0:
        hacker = hackers.pop(0)
        hacker.unwaitlist()
        cycle_waitlist(max_iterations - 1, hackers)
    return
