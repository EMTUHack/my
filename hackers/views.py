from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404, render, reverse
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q
from .models import Hacker
from .forms import ApplicationForm
from .social import fb_methods, gh_methods
from django.conf import settings
from main.decorators import require_condition
from main.email import recover_token_email, notify_checkin
from .util import proc
import json
import io
from time import sleep
# Create your views here.


def login_from_token(request, token="42"):
    hacker = Hacker.objects.filter(token=token).first()
    if hacker is None:
        messages.add_message(request, messages.ERROR, "Não te encontramos :(")
        sleep(2)
        return redirect('index')

    # Do not allow non active hackers
    if settings.HACKATHON_STARTED and not hacker.active:
        return HttpResponseForbidden()

    # Activate hackers on login
    if not hacker.active:
        hacker.active = True
        hacker.save()

    login(request, hacker.user)
    messages.add_message(request, messages.SUCCESS, "Olá, {}!".format(hacker.first_name))
    return redirect('dashboard')


@require_condition(settings.APPLICATION_OPEN)
@login_required
def application(request):
    app_instance = getattr(request.user.hacker, 'application', None)
    if request.method == 'POST':
        form = ApplicationForm(instance=app_instance, data=request.POST)
        if form.is_valid():
            form.save(hacker=request.user.hacker)
            messages.add_message(request, messages.SUCCESS, 'Aplicação atualizada!')

        else:
            messages.add_message(request, messages.ERROR, 'Aplicação contém erros!')
            return render(request, 'hackers/application.html', {'form': form, "sbar": "application"})

    form = ApplicationForm(instance=app_instance)
    return render(request, 'hackers/application.html', {'form': form, "sbar": "application"})


@require_condition(settings.HACKATHON_STARTED and not settings.HACKATHON_ENDED)
@user_passes_test(lambda u: u.hacker.is_checkedin)
def enter_team(request):
    """Enter Team API
    Returns forbidden if team is full
    """
    team_name = request.POST['team_name']
    hacker = request.user.hacker
    hacker.enter_team(team_name)
    if not hacker.has_team:
        return HttpResponseForbidden(json.dumps({"error": "Time lotado!"}), content_type="application/json")
    response = {
        "team": hacker.team.name,
        "project": hacker.team.project,
        "location": hacker.team.location,
        "new_blocked": hacker.team.block_new_members,
        "members": [{"name": h.name} for h in hacker.team.hackers.all()]
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


@require_condition(settings.HACKATHON_STARTED and not settings.HACKATHON_ENDED)
@user_passes_test(lambda u: u.hacker.is_checkedin)
def leave_team(request):
    """Leave Team API
    """
    hacker = request.user.hacker
    hacker.leave_team()
    return HttpResponse()


@require_condition(settings.HACKATHON_STARTED and not settings.HACKATHON_ENDED)
@user_passes_test(lambda u: u.hacker.is_checkedin)
def update_project(request):
    """Update Project API
    returns forbidden if hacker has no team
    """
    project = request.POST['project']
    hacker = request.user.hacker
    if hacker.team is None:
        return HttpResponseForbidden()
    team = hacker.team
    team.project = project
    team.save()
    return HttpResponse(json.dumps({"project": hacker.team.project}), content_type="application/json")


@require_condition(settings.HACKATHON_STARTED and not settings.HACKATHON_ENDED)
@user_passes_test(lambda u: u.hacker.is_checkedin)
def update_location(request):
    """Update Location API
    returns forbidden if hacker has no team
    """
    location = request.POST['location']
    hacker = request.user.hacker
    if not hacker.has_team:
        return HttpResponseForbidden()
    team = hacker.team
    team.location = location
    team.save()
    return HttpResponse(json.dumps({"location": hacker.team.location}), content_type="application/json")


@require_condition(settings.HACKATHON_STARTED and not settings.HACKATHON_ENDED)
@user_passes_test(lambda u: u.hacker.is_checkedin)
def update_allow_new_members(request):
    """Update Location API
    returns forbidden if hacker has no team
    """
    hacker = request.user.hacker
    if not hacker.has_team:
        return HttpResponseForbidden()
    team = hacker.team
    team.block_new_members = not team.block_new_members
    team.save()
    return HttpResponse()


@user_passes_test(lambda u: u.is_superuser)
def import_hackers(request):
    data = request.POST['data']
    hackers, errors = proc(io.StringIO(data))
    response_success = []
    response_repeated = []
    response_fail = []
    for err in errors:
        response_fail.append({"name": err["name"], "error": err["error"]})
    for hacker in hackers:
        try:
            if Hacker.objects.filter(email=hacker['email']).exists():
                response_repeated.append({"name": "{} {}".format(hacker["first_name"], hacker["last_name"])})
            else:
                h = Hacker.create(**hacker)
                response_success.append({"name": h.name})
        except Exception as e:
            response_fail.append({"name": "{} {}".format(hacker["first_name"], hacker["last_name"]), "error": repr(e)})

    return HttpResponse(json.dumps({"success": response_success, "repeated": response_repeated, "fail": response_fail}), content_type="application/json")


@user_passes_test(lambda u: u.is_superuser)
def search_hacker(request):
    data = request.POST['data']
    hackers = Hacker.objects.filter(Q(first_name__icontains=data) | Q(last_name__icontains=data) | Q(email__icontains=data) | Q(token__icontains=data)).filter(application__completed=True)[0:10]
    return HttpResponse(json.dumps([[
        hacker.name,
        hacker.email,
        hacker.application.extras,
        '<button class="ui small blue button" type="button" onclick="sweet(\'' + hacker.name + '\', ' + str(hacker.id) + ')">Check-in</button>'
    ] for hacker in hackers]), content_type="application/json")


@user_passes_test(lambda u: u.is_superuser)
def check_in_hacker(request):
    hacker_id = request.POST['id']
    hacker = get_object_or_404(Hacker, id=hacker_id)
    # Only allow confirmed or checked in hackers to be checked in
    if not (hacker.is_confirmed or hacker.is_checkedin):
        return HttpResponseForbidden()
    hacker.checked_in = not hacker.checked_in
    hacker.save()
    hacker.get_azure_pass()
    return HttpResponse(json.dumps({"res": hacker.checked_in, "id": hacker.id}), content_type="application/json")


@user_passes_test(lambda u: u.is_superuser)
def notify_check_in_hacker(request):
    hacker = get_object_or_404(Hacker, id=request.POST['id'])
    if hacker.checked_in:
        notify_checkin(hacker)
    return HttpResponse()


@user_passes_test(lambda u: u.is_superuser)
def get_hacker_check_in(request):
    hacker_id = request.POST['id']
    hacker = get_object_or_404(Hacker, id=hacker_id)
    return HttpResponse(json.dumps({"data": hacker.checked_in}), content_type="application/json")


@require_condition(settings.APPLICATION_OPEN)
@login_required
def toggle_withdraw(request):
    hacker = request.user.hacker
    hacker.withdraw = not hacker.withdraw
    hacker.save()
    return redirect('dashboard')


@login_required
def change_token(request):
    hacker = request.user.hacker
    hacker.new_token()
    messages.add_message(request, messages.SUCCESS, 'Token alterado!')
    return redirect('dashboard')


def recover_token(request):
    hacker = Hacker.objects.filter(email=request.POST['email']).first()
    if hacker is None:
        sleep(2)
        messages.add_message(request, messages.ERROR, 'Não te encontramos :(')
    else:
        recover_token_email(hacker)
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
    hacker = request.user.hacker
    hacker.fb_social_id = None
    hacker.save()
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
    hacker = request.user.hacker
    hacker.gh_social_id = None
    hacker.save()
    return redirect('dashboard')
