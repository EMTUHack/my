from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from main.decorators import require_condition
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.contrib import messages
from time import sleep
from .export import basic, basic_confirmed, basic_unconfirmed, advanced, teams, basic_staff
from hackers.models import Hacker, Application, Team
from staff.models import Staff
from django.db.models import Q
from collections import Counter
from .stats import get_grams
from .email import recover_token_email
from .social import fb_methods, gh_methods
from .mailchimp import add_subscriber
# Create your views here.


def index(request):
    if request.user.is_authenticated:
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
        if settings.HACKATHON_STARTED and not hacker_or_staff.active:
            return HttpResponseForbidden()

        # Activate hackers on login
        if not hacker_or_staff.active:
            hacker_or_staff.active = True
            hacker_or_staff.save()

    login(request, hacker_or_staff.user)
    messages.add_message(request, messages.SUCCESS, "Olá, {}!".format(hacker_or_staff.first_name))
    return redirect('dashboard')


@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html', {"sbar": "dashboard"})


@require_condition(settings.HACKATHON_STARTED)
@user_passes_test(lambda u: u.hacker.is_checkedin)
def team(request):
    return render(request, 'main/team.html', {"sbar": "team"})


@user_passes_test(lambda u: u.is_superuser)
def admin(request):
    return render(request, 'main/admin.html', {"sbar": "admin"})


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def checkin(request):
    return render(request, 'main/checkin.html', {"sbar": "checkin"})


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def stats(request):
    motivations = [a.essay for a in Application.objects.exclude(essay='').exclude(essay=None)]
    motivations_1 = get_grams(motivations)
    motivations_2 = get_grams(motivations, 2)
    descriptions = [a.description for a in Application.objects.exclude(description='').exclude(description=None)]
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
        "incomplete": len([h for h in Hacker.objects.all() if h.is_incomplete]),
        "withdraw": len([h for h in Hacker.objects.all() if h.is_withdraw]),
        "late": len([h for h in Hacker.objects.all() if h.is_late]),
        # Teams
        "not_have_team": len(Hacker.objects.all()) - len([h for h in Hacker.objects.all() if h.has_team]),
        "empty_team": len([t for t in Team.objects.all() if len(t.hackers.all()) == 0]),
        "semi_team": len([t for t in Team.objects.all() if 2 >= len(t.hackers.all()) >= 1]),
        "full_team": len([t for t in Team.objects.all() if len(t.hackers.all()) > 2]),
        "complete_team": Team.objects.exclude(project__isnull=True).exclude(project__exact='').exclude(location__isnull=True).exclude(location__exact=''),
        # Shirts
        "m_p": len(Application.objects.filter(gender="M").filter(shirt_size="P")),
        "m_m": len(Application.objects.filter(gender="M").filter(shirt_size="M")),
        "m_g": len(Application.objects.filter(gender="M").filter(shirt_size="G")),
        "m_gg": len(Application.objects.filter(gender="M").filter(shirt_size="GG")),
        "f_p": len(Application.objects.filter(Q(gender="F") | Q(gender="O")).filter(shirt_size="P")),
        "f_m": len(Application.objects.filter(Q(gender="F") | Q(gender="O")).filter(shirt_size="M")),
        "f_g": len(Application.objects.filter(Q(gender="F") | Q(gender="O")).filter(shirt_size="G")),
        "f_gg": len(Application.objects.filter(Q(gender="F") | Q(gender="O")).filter(shirt_size="GG")),
        # Extras
        "sleep": len(Application.objects.filter(sleeping_bag=True)),
        "pill": len(Application.objects.filter(pillow=True)),
        "diet": Counter([d.diet.lower() for d in Application.objects.exclude(diet__isnull=True).exclude(diet__exact='')]).most_common(),
        "needs": Counter([d.special_needs.lower() for d in Application.objects.exclude(special_needs__isnull=True).exclude(special_needs__exact='')]).most_common(),
        "motivations_1": Counter(motivations_1).most_common(10),
        "motivations_2": Counter(motivations_2).most_common(10),
        "descriptions_1": Counter(descriptions_1).most_common(10),
        "descriptions_2": Counter(descriptions_2).most_common(10),
    }
    return render(request, 'main/stats.html', {"sbar": "stats", "data": data})


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
def export_advanced_info(request):
    return advanced(request, [], [])


@user_passes_test(lambda u: u.is_superuser)
def export_teams(request):
    return teams(request)


@user_passes_test(lambda u: u.is_superuser)
def export_staff(request):
    return basic_staff(request)


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
