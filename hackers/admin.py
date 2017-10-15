from django.contrib import admin
from .models import Hacker, Team, Application
# Register your models here.

admin.site.register(Hacker)
admin.site.register(Team)
admin.site.register(Application)
