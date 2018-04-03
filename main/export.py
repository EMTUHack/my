import csv
from hackers.models import Hacker, Application, Team
from main.models import Settings
from staff.models import Staff
from schedule.models import Event
from django.http import HttpResponse


def basic(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=basic.csv'
    writer = csv.writer(response, csv.excel)
    writer.writerow([
        "First Name",
        "Last Name",
        "Email",
        "Token",
    ])
    for obj in Hacker.objects.all():
        writer.writerow([
            obj.first_name,
            obj.last_name,
            obj.email,
            obj.token
        ])
    return response


def basic_staff(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=basic_staff.csv'
    writer = csv.writer(response, csv.excel)
    writer.writerow([
        "First Name",
        "Last Name",
        "Email",
        "Token",
    ])
    for obj in Staff.objects.all():
        writer.writerow([
            obj.first_name,
            obj.last_name,
            obj.email,
            obj.token
        ])
    return response


def bus_passengers(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=bus_passengers.csv'
    writer = csv.writer(response, csv.excel)
    writer.writerow([
        "First Name",
        "Last Name",
        "Email",
        "University",
        "From",
    ])
    for obj in Application.objects.filter(hacker__confirmed=True).filter(bus_sp=True)[:Settings.get().max_bus_spots]:
        writer.writerow([
            obj.hacker.first_name,
            obj.hacker.last_name,
            obj.hacker.email,
            obj.university,
            'São Paulo'
        ])
    for obj in Application.objects.filter(hacker__confirmed=True).filter(bus_sc=True)[:Settings.get().max_bus_spots]:
        writer.writerow([
            obj.hacker.first_name,
            obj.hacker.last_name,
            obj.hacker.email,
            obj.university,
            'São Carlos'
        ])
    return response


def basic_confirmed(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=basic_confirmed.csv'
    writer = csv.writer(response, csv.excel)
    writer.writerow([
        "First Name",
        "Last Name",
        "Email",
        "Token",
    ])
    for obj in Hacker.objects.all():
        if obj.is_confirmed:
            writer.writerow([
                obj.first_name,
                obj.last_name,
                obj.email,
                obj.token
            ])
    return response


def basic_unconfirmed(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=basic_unconfirmed.csv'
    writer = csv.writer(response, csv.excel)
    writer.writerow([
        "First Name",
        "Last Name",
        "Email",
        "Token",
    ])
    for obj in Hacker.objects.all():
        if obj.is_admitted:
            writer.writerow([
                obj.first_name,
                obj.last_name,
                obj.email,
                obj.token
            ])
    return response


def basic_no_application(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=basic_no_application.csv'
    writer = csv.writer(response, csv.excel)
    writer.writerow([
        "First Name",
        "Last Name",
        "Email",
        "Token",
    ])
    for obj in Hacker.objects.all():
        if not obj.finished_application:
            writer.writerow([
                obj.first_name,
                obj.last_name,
                obj.email,
                obj.token
            ])
    return response


def advanced(request, exclude_hacker=[], exclude_application=[]):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=advanced.csv'
    writer = csv.writer(response, csv.excel)
    fields = [k for k, v in Hacker.objects.first().export_fields(exclude_hacker).items()]
    fields.extend([k for k, v in Application.objects.first().export_fields(exclude_application).items()])
    writer.writerow(fields)
    for hacker in Hacker.objects.all():
        if hacker.finished_application:
            row = [v for k, v in hacker.export_fields(exclude_hacker).items()]
            row.extend([v for k, v in hacker.application.export_fields(exclude_application).items()])
            writer.writerow(row)
    return response


def advanced_attended(request, exclude_hacker=[], exclude_application=[]):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=advanced.csv'
    writer = csv.writer(response, csv.excel)
    fields = [k for k, v in Hacker.objects.first().export_fields(exclude_hacker).items()]
    fields.extend([k for k, v in Application.objects.first().export_fields(exclude_application).items()])
    writer.writerow(fields)
    for hacker in Hacker.objects.filter(checked_in=True):
        if hacker.finished_application:
            row = [v for k, v in hacker.export_fields(exclude_hacker).items()]
            row.extend([v for k, v in hacker.application.export_fields(exclude_application).items()])
            writer.writerow(row)
    return response


def teams(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=teams.csv'
    writer = csv.writer(response, csv.excel)
    for obj in Team.objects.exclude(project__isnull=True).exclude(project__exact='').exclude(location__isnull=True).exclude(location__exact='').exclude(github_url=None).exclude(github_url__iexact=''):
        if obj.hackers.all().count() > 0:
            writer.writerow([
                obj.name,
                obj.location,
                obj.project
            ])
    return response


def teams_after(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=teams.csv'
    writer = csv.writer(response, csv.excel)
    writer.writerow(["Nome", "Local", "Descrição", "Github", "Participantes"])
    for obj in Team.objects.exclude(project__isnull=True).exclude(project__exact='').exclude(location__isnull=True).exclude(location__exact='').exclude(github_url=None).exclude(github_url__iexact=''):
        if obj.hackers.all().count() > 0:
            writer.writerow([
                obj.name,
                obj.location,
                obj.project,
                obj.github_url,
                str([hacker.name for hacker in obj.hackers.all()])
            ])
    return response


def event_summary(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=events.csv'
    writer = csv.writer(response, csv.excel, delimiter='\t')
    writer.writerow(["Nome", "Hora", "Palestrante", "Participantes", "Avaliação média", "Comentários"])
    for obj in Event.objects.all().exclude(requires_registration=False):
        rr = [r.rating for r in obj.attendees.exclude(rating__isnull=True)]
        writer.writerow([
            obj.name,
            obj.human_time,
            obj.speaker,
            len(obj.attendees.all()),
            (float(sum(rr) / len(rr)) if len(rr) > 0 else '-'),
            " -#- ".join(["({}) {}".format(r.rating, r.feedback) for r in obj.attendees.exclude(feedback__isnull=True)])
        ])
    return response
