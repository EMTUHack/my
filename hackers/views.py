from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q
from .models import Hacker
from .forms import ApplicationForm
from django.conf import settings
from main.decorators import require_condition
from main.email import notify_checkin
from main.mailchimp import add_subscriber, remove_subscriber, batch_confirm
from .util import proc
import json
import io
# Create your views here.


@require_condition(settings.APPLICATION_OPEN)
@login_required
def application(request):
    app_instance = getattr(request.user.hacker, 'application', None)
    if request.method == 'POST':
        form = ApplicationForm(instance=app_instance, data=request.POST)
        if form.is_valid():
            form.save(hacker=request.user.hacker)
            messages.add_message(request, messages.SUCCESS, 'Aplicação atualizada!')
            remove_subscriber(settings.MAILCHIMP_LIST_PRE, request.user.hacker)
            add_subscriber(settings.MAILCHIMP_LIST_CONFIRMED, request.user.hacker)
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
def update_github_url(request):
    """Update Projeto URL API
    returns forbidden if hacker has no team
    """
    github_url = request.POST['github_url']
    hacker = request.user.hacker
    if not hacker.has_team:
        return HttpResponseForbidden()
    team = hacker.team
    team.github_url = github_url
    team.save()
    return HttpResponse(json.dumps({"github_url": hacker.team.github_url}), content_type="application/json")


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
                add_subscriber(settings.MAILCHIMP_LIST_PRE, h)
                response_success.append({"name": h.name})
        except Exception as e:
            response_fail.append({"name": "{} {}".format(hacker["first_name"], hacker["last_name"]), "error": repr(e)})

    return HttpResponse(json.dumps({"success": response_success, "repeated": response_repeated, "fail": response_fail}), content_type="application/json")


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def search_hacker(request):
    data = request.POST['data']
    hackers = Hacker.objects.filter(Q(first_name__icontains=data) | Q(last_name__icontains=data) | Q(email__icontains=data) | Q(token__icontains=data)).filter(application__completed=True)[0:10]
    return HttpResponse(json.dumps([[
        hacker.name,
        hacker.email,
        hacker.application.extras,
        '<button class="ui small blue button" type="button" onclick="sweet(\'' + hacker.name + '\', ' + str(hacker.id) + ')">Check-in</button>'
    ] for hacker in hackers]), content_type="application/json")


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
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


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
def notify_check_in_hacker(request):
    hacker = get_object_or_404(Hacker, id=request.POST['id'])
    if hacker.checked_in:
        notify_checkin(hacker)
    return HttpResponse()


@user_passes_test(lambda u: u.is_staff_member or u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
def batch_confirm_hackers(request):
    hackers = [h for h in Hacker.objects.all() if h.is_confirmed]
    batch_confirm(hackers)
    messages.add_message(request, messages.SUCCESS, '{} hackers migrados'.format(len(hackers)))
    return redirect('dashboard')
