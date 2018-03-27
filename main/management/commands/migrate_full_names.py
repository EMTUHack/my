from django.core.management.base import BaseCommand
from staff.models import Staff
from hackers.models import Hacker


class Command(BaseCommand):

    def handle(self, *args, **options):
        for hacker in Hacker.objects.all():
            hacker.full_name = "{} {}".format(hacker.first_name.strip(), hacker.last_name.strip())
            hacker.save()
        for staff in Staff.objects.all():
            staff.full_name = "{} {}".format(staff.first_name.strip(), staff.last_name.strip())
            staff.save()
        return "Done"
