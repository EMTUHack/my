import requests
from django.conf import settings
from urllib.parse import urlencode
from django.shortcuts import reverse
from hackers.models import Hacker
from django.contrib import messages
from django.contrib.auth import login

app_id = settings.GITHUB_KEY
app_secret = settings.GITHUB_SECRET
state = 'random_string_not_needed_for_this_simple_app'


def redirect_url(request):
    if request.is_secure():
        return 'https://' + request.get_host() + reverse('hackers:github_login_response')
    else:
        return 'http://' + request.get_host() + reverse('hackers:github_login_response')


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

    # Get the user's scope ID from debug data
    social_id = debug['id']

    # Save new hacker information
    if request.user.is_authenticated:
        hacker = request.user.hacker
        hacker.gh_social_id = social_id
        hacker.save()
    else:
        hacker = Hacker.objects.filter(gh_social_id=social_id).first()

    # Try to login the user
    if hacker is None:
        messages.add_message(request, messages.ERROR, 'Você precisa estar inscrito(a) para entrar!')
    else:
        login(request, hacker.user)
        messages.add_message(request, messages.SUCCESS, 'Olá, ' + hacker.first_name + '!')

    return request


def login_canceled(request):

    # If the user has canceled the login process, or something else happened, do nothing and display error message
    messages.add_message(request, messages.ERROR, 'Oops! Algo de errado aconteceu!')

    return request
