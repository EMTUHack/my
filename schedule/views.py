from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from .models import Event
from django.utils import timezone
import pytz
import json
now = timezone.now()
# Create your views here.


def schedule(request):
    events = Event.objects.filter(starts__gt=now.astimezone(pytz.utc)).order_by('starts')
    return render(request, 'schedule/schedule.html', {'events': events, 'sbar': 'eventos'})


def submit_feedback(request):
    event_id = request.POST['id']
    feedback = request.POST['feedback']
    rating = request.POST['rating']
    event = Event.objects.get(id=event_id)
    if event.rate_event(request.user.hacker, rating, feedback) is None:
        return HttpResponseForbidden()
    return HttpResponse(json.dumps({"data": ""}), content_type="application/json")


def toggle_attendance(request):
    event_id = request.POST['id']
    event = Event.objects.get(id=event_id)
    resp, err = event.toggle_attendee(request.user.hacker)
    resp = True if resp else False
    return HttpResponse(json.dumps({"error": err, "resp": resp}), content_type="application/json")
