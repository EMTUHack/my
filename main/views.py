from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from main.decorators import require_condition

# Create your views here.

# TODO: View para pegar csv básico de todo mundo para criar lista no mailchimp
# TODO: View para pegar csv avançado de todo mundo para enviar pra microsoft


def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, 'main/login.html')


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


@user_passes_test(lambda u: u.is_superuser)
def checkin(request):
    return render(request, 'main/checkin.html', {"sbar": "checkin"})


def handler404(request):
    return render(request, 'main/errors/404.html', status=404)


def handler500(request):
    return render(request, 'main/errors/500.html', status=500)


def handler403(request):
    return render(request, 'main/errors/403.html', status=403)


@user_passes_test(lambda u: u.is_superuser)
def test_error(request):
    return request
