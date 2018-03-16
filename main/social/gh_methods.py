import requests
from django.conf import settings
from urllib.parse import urlencode
from django.shortcuts import reverse
from hackers.models import Hacker
from staff.models import Staff
from django.contrib import messages
from django.contrib.auth import login
from main.models import Settings

app_id = settings.GITHUB_KEY
app_secret = settings.GITHUB_SECRET
state = 'random_string_not_needed_for_this_simple_app'


def redirect_url(request):
    if request.is_secure():
        return 'https://' + request.get_host() + reverse('main:github_login_response')
    else:
        # enforce https
        return 'https://' + request.get_host() + reverse('main:github_login_response')


def auth_url(request):
    """Auth URL

    Returns the github auth url using the current app's domain
    """

    canvas_url = redirect_url(request)

    # Permissions set by user. Default is none
    perms = settings.GITHUB_PERMISSIONS

    url = "https://github.com/login/oauth/authorize?"

    # Payload
    kvps = {'client_id': app_id, 'redirect_uri': canvas_url, 'state': state, 'allow_signup': 'false'}

    # Format permissions if needed
    if perms:
        kvps['scope'] = " ".join(perms)

    # Return the url
    return url + urlencode(kvps)


def get_access_token_from_code(code, redirect_uri, app_id, app_secret):
    url = 'https://github.com/login/oauth/access_token'
    payload = {
        'client_id': app_id,
        'client_secret': app_secret,
        'code': code
    }
    response = requests.post(url, headers={'Accept': 'application/json'}, data=payload)
    return response.json()


def debug_token(token):
    url = 'https://api.github.com/user'
    response = requests.get(url, headers={'Authorization': 'token {}'.format(token)})
    return response.json()


def login_successful(code, request):
    """Login Successful

    Process successful login by creating or updating an user using Facebook's response
    """

    canvas_url = auth_url(request)

    # Get token info from user
    token_info = get_access_token_from_code(code, canvas_url, app_id, app_secret)

    # Extract token from token info
    access_token = token_info['access_token']

    # Debug the token, as per documentation
    debug = debug_token(access_token)

    # nasty bug fix
    for key in debug:
        if debug[key] is None:
            debug[key] = ' '

    # Get the user's scope ID from debug data
    social_id = debug['id']
    first_name = debug.get('name', ' ').split(' ')[0]
    last_name = debug.get('name', ' ').split(' ')[1:][0] if len(debug.get('name', ' ').split(' ')) > 1 else ''
    email = debug.get('email', '')

    # Save new hacker information
    if request.user.is_authenticated:
        obj = request.user.hacker_or_staff
    else:
        obj = Hacker.objects.filter(gh_social_id=social_id).first() or Staff.objects.filter(gh_social_id=social_id).first()
        if obj is None:
            obj = Hacker.objects.filter(email=email).first() or Staff.objects.filter(email=email).first()

    if obj is None:
        if not Settings.registration_is_open():
            messages.add_message(request, messages.ERROR, 'Inscrições estão fechadas!')
            return request
        obj = Hacker()

    obj.gh_social_id = social_id
    obj.first_name = obj.first_name if getattr(obj, 'first_name', '') else first_name
    obj.last_name = obj.last_name if getattr(obj, 'last_name', '') else last_name
    obj.email = obj.email if getattr(obj, 'email', '') else email
    # Fix empty email edge case
    if obj.email == ' ' or obj.email == '':
        def generate_temp_email(n=0):
            e = 'temp_{}@email.com'.format(n)
            if Hacker.objects.filter(email=e).exists():
                return generate_temp_email(n + 1)
            return e
        obj.email = generate_temp_email()
    obj.save()

    # Try to login the user
    if obj is None:
        messages.add_message(request, messages.ERROR, 'Você precisa estar inscrito(a) para entrar!')
    else:
        login(request, obj.user)

    return request


def login_canceled(request):

    # If the user has canceled the login process, or something else happened, do nothing and display error message
    messages.add_message(request, messages.ERROR, 'Oops! Algo de errado aconteceu!')

    return request
