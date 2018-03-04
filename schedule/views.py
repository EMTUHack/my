from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Event
from django.utils import timezone
import pytz
import json
from datetime import datetime
from django.contrib import messages
import locale
# Create your views here.


@user_passes_test(lambda u: u.hacker.is_checkedin)
def schedule(request):
    now = timezone.now()
    events = Event.objects.filter(starts__gt=now.astimezone(pytz.utc)).order_by('starts')
    return render(request, 'schedule/schedule.html', {'events': events, 'sbar': 'eventos'})


@user_passes_test(lambda u: u.hacker.is_checkedin)
def submit_feedback(request):
    event_id = request.POST['id']
    feedback = request.POST['feedback']
    rating = request.POST['rating']
    event = Event.objects.get(id=event_id)
    if event.rate_event(request.user.hacker, rating, feedback) is None:
        return HttpResponseForbidden()
    return HttpResponse(json.dumps({"data": ""}), content_type="application/json")


@user_passes_test(lambda u: u.hacker.is_checkedin)
def toggle_attendance(request):
    event_id = request.POST['id']
    event = Event.objects.get(id=event_id)
    resp, err = event.toggle_attendee(request.user.hacker)
    resp = True if resp else False
    return HttpResponse(json.dumps({"error": err, "resp": resp}), content_type="application/json")


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def fetch_schedule_simple(request):
    events = Event.objects.all().order_by('starts')
    data = {
        "data": [
            [
                event.name,
                event.human_time,
                event.place,
                event.kind,
                '<a onclick="show_edit_event(' + str(event.id) + ')" class="ui blue button">Editar</a>',
                '<a onclick="delete_event(' + str(event.id) + ')" class="ui red button">Apagar</a>'
            ] for event in events
        ]
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def fetch_schedule_full(request):
    event_id = request.POST.get('event_id', None)
    event = get_object_or_404(Event, id=event_id)
    data = {
        "name": event.name,
        "description": event.description,
        "starts": ((event.starts - datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds() * 1000),
        "kind": event.kind,
        "place": event.place,
        "requires_registration": event.requires_registration,
        "speaker": event.speaker,
        "speaker_description": event.speaker_description,
        "max_attendees": event.max_attendees
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def create_or_edit_event(request):
    raw = request.POST
    print(raw)
    data = {}
    for field in raw:
        data[field] = raw[field]
        if field == 'starts':
            tz = pytz.timezone('America/Sao_Paulo')
            data[field] = datetime.strptime(raw[field], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=pytz.UTC).astimezone(tz)
        if field == 'requires_registration':
            data[field] = True if (raw[field] == 'on' or raw[field] == 'true') else False
        if field == 'max_attendees':
            data[field] = int(raw[field]) if raw[field] else None
    event_id = data.pop('event_id', None)
    data.pop('csrfmiddlewaretoken')
    if event_id is not None:
        event = get_object_or_404(Event, id=event_id)
        for field in data:
            setattr(event, field, data[field])
    else:
        event = Event(**data)
    event.save()
    print(data)
    messages.add_message(request, messages.ERROR, "Evento salvo")
    return redirect('admin')


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def delete_event(request):
    event_id = request.POST.get('event_id', None)
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return HttpResponse()
