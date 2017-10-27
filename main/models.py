from django.contrib.auth.models import User
# Create your models here.


@property
def hacker_or_staff(self):
    return self.hacker if hasattr(self, 'hacker') else self.staff


User.add_to_class('hacker_or_staff', hacker_or_staff)
