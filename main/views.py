from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import datetime
import json
import pytz
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.contrib import messages
from time import sleep
from .export import *
from hackers.models import Hacker, Application, Team
from staff.models import Staff
from django.db.models import Q
from collections import Counter
from .models import Settings
from .stats import get_grams
from .email import recover_token_email
from hackers.tasks import send_verify_email as sve
from .social import fb_methods, gh_methods
from .mailchimp import add_subscriber
from .util import cycle_waitlist
# Create your views here.


def index(request):
    if len(Settings.objects.all()) == 0:
        Settings().save()
    if request.user.is_authenticated:
        # Activate hackers on login
        obj = request.user.hacker_or_staff
        if not obj.active:
            obj.active = True
            obj.save()
        return redirect("dashboard")
    return render(request, 'main/login.html')


def login_from_token(request, token="42"):
    hacker_or_staff = Hacker.objects.filter(token=token).first() or Staff.objects.filter(token=token).first()
    if hacker_or_staff is None:
        messages.add_message(request, messages.ERROR, "Não te encontramos :(")
        sleep(2)
        return redirect('index')

    if hacker_or_staff.user.is_hacker:
        # Do not allow non active hackers
        if (Settings.hackathon_is_happening() and not hacker_or_staff):
            return HttpResponseForbidden()

        # Activate hackers on login
        if not hacker_or_staff.active:
            hacker_or_staff.active = True
            hacker_or_staff.save()

    login(request, hacker_or_staff.user)
    return redirect('dashboard')


@login_required
@user_passes_test(lambda u: u.is_hacker_or_staff)
def dashboard(request):
    return render(request, 'main/dashboard.html', {"sbar": "dashboard"})


@user_passes_test(lambda u: u.hacker.is_checkedin and Settings.hackathon_is_happening())
def team(request):
    return render(request, 'main/team.html', {"sbar": "team"})


@user_passes_test(lambda u: u.is_superuser)
def admin(request):
    return render(request, 'main/admin.html', {"sbar": "admin"})


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def manage_hackers(request):
    return render(request, 'main/hacker_management.html', {"sbar": "manage_hackers"})


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def fetch_submitted_hackers(request):
    hackers = Hacker.objects.all()
    submitted = [hacker for hacker in hackers if hacker.is_submitted]
    data = {
        "data": [
            [
                hacker.name,
                hacker.email,
                hacker.application.university,
                hacker.application.enroll_year,
                '<a onclick="show_pending(' + str(hacker.id) + ')" class="ui button red">Avaliar</a>',
                (hacker.created - datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds()
            ] for hacker in submitted
        ]
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def fetch_admitted_hackers(request):
    hackers = Hacker.objects.all()
    submitted = [hacker for hacker in hackers if hacker.is_admitted]
    data = {
        "data": [
            [
                hacker.name,
                hacker.email,
                hacker.application.university,
                hacker.application.enroll_year,
                '<a onclick="show_admitted(' + str(hacker.id) + ')" class="ui button red">Avaliar</a>'
            ] for hacker in submitted
        ]
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def fetch_declined_hackers(request):
    hackers = Hacker.objects.all()
    submitted = [hacker for hacker in hackers if hacker.is_declined]
    data = {
        "data": [
            [
                hacker.name,
                hacker.email,
                hacker.application.university,
                hacker.application.enroll_year,
                '<a onclick="show_declined(' + str(hacker.id) + ')" class="ui button red">Avaliar</a>'
            ] for hacker in submitted
        ]
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def fetch_waitlist_hackers(request):
    hackers = Hacker.objects.all()
    submitted = [hacker for hacker in hackers if hacker.is_waitlist]
    data = {
        "data": [
            [
                hacker.name,
                hacker.email,
                hacker.application.university,
                hacker.application.enroll_year,
                '<a onclick="show_waitlist(' + str(hacker.id) + ')" class="ui button red">Avaliar</a>',
                (hacker.waitlist_date - datetime(1970, 1, 1).replace(tzinfo=pytz.UTC)).total_seconds()
            ] for hacker in submitted
        ]
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def fetch_checkedin_hackers(request):
    hackers = Hacker.objects.all()
    submitted = [hacker for hacker in hackers if hacker.is_checkedin]
    data = {
        "data": [
            [
                hacker.name,
                hacker.email,
                hacker.application.university,
                hacker.application.enroll_year,
                '<a onclick="show_checkedin(' + str(hacker.id) + ')" class="ui button red">Avaliar</a>'
            ] for hacker in submitted
        ]
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def get_hacker_application(request):
    hacker = get_object_or_404(Hacker, id=request.POST['id'])
    info = hacker.application.export_fields([])
    info.update(hacker.export_fields(['team']))
    info.update({"id": hacker.id})
    return HttpResponse(json.dumps(info), content_type="application/json")


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def admit_hacker(request):
    hacker = get_object_or_404(Hacker, id=request.POST['id'])
    hacker.admit()
    return HttpResponse()


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def nag_hacker(request):
    hacker = get_object_or_404(Hacker, id=request.POST['id'])
    hacker.nag()
    return HttpResponse()


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def decline_hacker(request):
    hacker = get_object_or_404(Hacker, id=request.POST['id'])
    hacker.decline()
    return HttpResponse()


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def unwaitlist_hacker(request):
    hacker = get_object_or_404(Hacker, id=request.POST['id'])
    hacker.unwaitlist()
    return HttpResponse()


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def manual_cycle_waitlist(request):
    cycle_waitlist(100)
    return redirect('admin')


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def search_people(request):
    data = request.POST['data']
    hackers = Hacker.objects.filter(Q(first_name__icontains=data) | Q(last_name__icontains=data) | Q(email__icontains=data))[0:5]
    staff = Staff.objects.filter(Q(first_name__icontains=data) | Q(last_name__icontains=data) | Q(email__icontains=data))[0:5]
    people = list(hackers)
    people.extend(list(staff))

    return HttpResponse(json.dumps([[
        person.name,
        person.email,
        'Staff' if hasattr(person.user, 'staff') else 'Hacker',
        '<button class="ui small blue button" type="button" onclick="convert(' + str(person.id) + ')">Converter</button>'
    ] for person in people]), content_type="application/json")


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def convert_people(request):
    p_id = request.POST['id']
    try:
        person = Hacker.objects.get(id=p_id)
        hacker = True
    except:
        person = get_object_or_404(Staff, id=p_id)
        hacker = False
    if hacker:
        person2 = Staff(
            user=person.user,
            first_name=person.first_name,
            last_name=person.last_name,
            email=person.email,
            token=person.token,
            fb_social_id=person.fb_social_id,
            gh_social_id=person.gh_social_id
        )
    else:
        person2 = Hacker(
            user=person.user,
            first_name=person.first_name,
            last_name=person.last_name,
            email=person.email,
            token=person.token,
            fb_social_id=person.fb_social_id,
            gh_social_id=person.gh_social_id
        )
    person2.save()
    person.delete()
    return HttpResponse()


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def checkin(request):
    return render(request, 'main/checkin.html', {"sbar": "checkin"})


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def stats(request):
    motivations = [a.essay for a in Application.objects.exclude(essay='').exclude(essay=None).filter(hacker__confirmed=True)]
    motivations_1 = get_grams(motivations)
    motivations_2 = get_grams(motivations, 2)
    descriptions = [a.description for a in Application.objects.exclude(description='').exclude(description=None).filter(hacker__confirmed=True)]
    descriptions_1 = get_grams(descriptions)
    descriptions_2 = get_grams(descriptions, 2)
    data = {
        # Basic
        "hackers": len(Hacker.objects.all()),
        "teams": len(Team.objects.all()),
        "staff": len(Staff.objects.all()),
        # Hackers
        "checkin": len([h for h in Hacker.objects.all() if h.is_checkedin]),
        "confirmed": len([h for h in Hacker.objects.all() if h.is_confirmed]),
        "admitted": len([h for h in Hacker.objects.all() if h.is_admitted]),
        "withdraw": len([h for h in Hacker.objects.all() if h.is_withdraw]),
        "waitlist": len([h for h in Hacker.objects.all() if h.is_waitlist]),
        # Teams
        "not_have_team": Hacker.objects.filter(team=None).filter(checked_in=True).count(),
        "empty_team": len([t for t in Team.objects.all() if len(t.hackers.all()) == 0]),
        "semi_team": len([t for t in Team.objects.all() if 2 >= len(t.hackers.all()) >= 1]),
        "full_team": len([t for t in Team.objects.all() if len(t.hackers.all()) > 2]),
        "complete_team": Team.objects.exclude(project__isnull=True).exclude(project__exact='').exclude(location__isnull=True).exclude(location__exact='').exclude(github_url=None).exclude(github_url__iexact=''),
        # Shirts
        "m_p": len(Application.objects.filter(shirt_style="Normal").filter(shirt_size="P").filter(hacker__confirmed=True)),
        "m_m": len(Application.objects.filter(shirt_style="Normal").filter(shirt_size="M").filter(hacker__confirmed=True)),
        "m_g": len(Application.objects.filter(shirt_style="Normal").filter(shirt_size="G").filter(hacker__confirmed=True)),
        "m_gg": len(Application.objects.filter(shirt_style="Normal").filter(shirt_size="GG").filter(hacker__confirmed=True)),
        "f_p": len(Application.objects.filter(shirt_style="Babylook").filter(shirt_size="P").filter(hacker__confirmed=True)),
        "f_m": len(Application.objects.filter(shirt_style="Babylook").filter(shirt_size="M").filter(hacker__confirmed=True)),
        "f_g": len(Application.objects.filter(shirt_style="Babylook").filter(shirt_size="G").filter(hacker__confirmed=True)),
        "f_gg": len(Application.objects.filter(shirt_style="Babylook").filter(shirt_size="GG").filter(hacker__confirmed=True)),
        # Extras
        "sleep": len(Application.objects.filter(sleeping_bag=True).filter(hacker__confirmed=True)),
        "pill": len(Application.objects.filter(pillow=True).filter(hacker__confirmed=True)),
        "bus_sp": len(Application.objects.filter(bus_sp=True).filter(hacker__confirmed=True)),
        "bus_sc": len(Application.objects.filter(bus_sc=True).filter(hacker__confirmed=True)),
        "diet": Counter([d.diet.lower() for d in Application.objects.exclude(diet__isnull=True).exclude(diet__exact='').filter(hacker__confirmed=True)]).most_common(),
        "needs": Counter([d.special_needs.lower() for d in Application.objects.exclude(special_needs__isnull=True).exclude(special_needs__exact='').filter(hacker__confirmed=True)]).most_common(),
        "motivations_1": Counter(motivations_1).most_common(10),
        "motivations_2": Counter(motivations_2).most_common(10),
        "descriptions_1": Counter(descriptions_1).most_common(10),
        "descriptions_2": Counter(descriptions_2).most_common(10),
    }
    return render(request, 'main/stats.html', {"sbar": "stats", "data": data})


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def change_registration_open(request):
    date = datetime.strptime(request.POST['date'], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=pytz.utc)
    sett = Settings.get()
    sett.registration_open = date
    sett.save()
    return HttpResponse()


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def change_registration_close(request):
    date = datetime.strptime(request.POST['date'], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=pytz.utc)
    sett = Settings.get()
    sett.registration_close = date
    sett.save()
    return HttpResponse()


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def change_confirmation(request):
    date = datetime.strptime(request.POST['date'], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=pytz.utc)
    sett = Settings.get()
    sett.confirmation = date
    sett.save()
    return HttpResponse()


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def change_hackathon_start(request):
    date = datetime.strptime(request.POST['date'], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=pytz.utc)
    sett = Settings.get()
    sett.hackathon_start = date
    sett.save()
    return HttpResponse()


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def change_hackathon_end(request):
    date = datetime.strptime(request.POST['date'], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=pytz.utc)
    sett = Settings.get()
    sett.hackathon_end = date
    sett.save()
    return HttpResponse()


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def change_max_hackers(request):
    n = request.POST['number']
    try:
        n = int(n)
        sett = Settings.get()
        sett.max_hackers = n
        sett.save()
    except ValueError:
        pass
    return HttpResponse()


@user_passes_test(lambda u: u.is_superuser)
def export_basic_info(request):
    return basic(request)


@user_passes_test(lambda u: u.is_superuser)
def export_basic_info_confirmed(request):
    return basic_confirmed(request)


@user_passes_test(lambda u: u.is_superuser)
def export_basic_info_unconfirmed(request):
    return basic_unconfirmed(request)


@user_passes_test(lambda u: u.is_superuser)
def export_basic_info_no_application(request):
    return basic_no_application(request)


@user_passes_test(lambda u: u.is_superuser)
def export_advanced_info(request):
    return advanced(request, [], [])


@user_passes_test(lambda u: u.is_superuser)
def export_advanced_checkedin_info(request):
    return advanced_attended(request, [], [])


@user_passes_test(lambda u: u.is_superuser)
def export_teams(request):
    return teams(request)


@user_passes_test(lambda u: u.is_superuser)
def export_teams_after(request):
    return teams_after(request)


@user_passes_test(lambda u: u.is_superuser)
def export_staff(request):
    return basic_staff(request)


@user_passes_test(lambda u: u.is_superuser)
def export_bus_passengers(request):
    return bus_passengers(request)


@user_passes_test(lambda u: u.is_superuser)
def export_events(request):
    return event_summary(request)


@login_required
def change_token(request):
    hacker_or_staff = request.user.hacker_or_staff
    hacker_or_staff.new_token()
    if request.user.is_hacker:
        add_subscriber(settings.MAILCHIMP_LIST_CONFIRMED, hacker_or_staff)
    messages.add_message(request, messages.SUCCESS, 'Token alterado!')
    return redirect('dashboard')


def recover_token(request):
    obj = Hacker.objects.filter(email=request.POST['email']).first() or Staff.objects.filter(email=request.POST['email']).first()
    if obj is None:
        sleep(2)
        messages.add_message(request, messages.ERROR, 'Não te encontramos :(')
    else:
        recover_token_email(obj)
        messages.add_message(request, messages.SUCCESS, 'Cheque seu email :)')
    return redirect('index')


@login_required
def send_verify_email(request):
    obj = request.user.hacker
    if not obj.unverified:
        return redirect('dashboard')
    obj.new_verification_code()
    sve.delay(obj.id)
    messages.add_message(request, messages.SUCCESS, 'Cheque seu email :)')
    return redirect('dashboard')


def check_verify_email(request, code):
    obj = get_object_or_404(Hacker, verification_code=code)
    obj.unverified = False
    user = obj.user
    user.username = obj.email
    user.email = obj.email
    user.save()
    obj.new_verification_code()
    login(request, obj.user)
    return redirect('dashboard')


# Social Views
def facebook_login(request):

    # Generate auth_url and redirect to it
    return redirect(fb_methods.auth_url(request))


def facebook_login_response(request):
    """Facebook Login Response

    Try to access 'code' from the response. If found, the login was successful. Unsuccessful otherwise
    """

    try:
        code = request.GET['code']
    except:
        # User cancelled login
        request = fb_methods.login_canceled(request)
        return redirect(reverse('index'))

    request = fb_methods.login_successful(code, request)
    return redirect('dashboard')


@login_required
def remove_facebook(request):
    obj = request.user.hacker_or_staff
    obj.fb_social_id = None
    obj.save()
    return redirect('dashboard')


# Social Views
def github_login(request):

    # Generate auth_url and redirect to it
    return redirect(gh_methods.auth_url(request))


def github_login_response(request):
    """GitHub Login Response

    Try to access 'code' from the response. If found, the login was successful. Unsuccessful otherwise
    """

    try:
        code = request.GET['code']
    except:
        # User cancelled login
        request = gh_methods.login_canceled(request)
        return redirect(reverse('index'))

    request = gh_methods.login_successful(code, request)
    return redirect('dashboard')


@login_required
def remove_github(request):
    obj = request.user.hacker_or_staff
    obj.gh_social_id = None
    obj.save()
    return redirect('dashboard')


def handler404(request):
    return render(request, 'main/errors/404.html', status=404)


def handler500(request):
    return render(request, 'main/errors/500.html', status=500)


def handler403(request):
    return render(request, 'main/errors/403.html', status=403)


@user_passes_test(lambda u: u.is_superuser)
def test_error(request):
    return request
