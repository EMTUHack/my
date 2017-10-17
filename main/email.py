from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse


def recover_token_email(hacker):
    context = {
        'title': 'Recuperação de Token',
        'subtitle': '',
        'description': 'Você está recebendo essa mensagem pois alguém pediu para que o seu token fosse recuperado.<br><br>Seu token atual é <b>{}</b> e você pode logar em sua conta usando o botão abaixo'.format(hacker.token),
        'actionUrl': settings.ROOT_URL + reverse('hackers:login_from_token', args={hacker.token}),
        'actionName': 'Acessar sua conta',
        'project_url': settings.ROOT_URL,
        'hackathon_name': settings.HACKATHON_NAME,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.email
    fr = str(settings.DEFAULT_FROM_EMAIL)
    msg_plain = render_to_string('main/email/action/text.txt', context)
    msg_html = render_to_string('main/email/action/html.html', context)

    send_mail(
        '[{}] Recuperar Token'.format(settings.HACKATHON_NAME),
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def notify_checkin(hacker):
    context = {
        'title': 'Check-in feito',
        'subtitle': 'Prepare-se!',
        'description': 'Seu check-in no {} foi feito! Ficamos felizes que você pôde vir e esperamos que você se divirta!<br>Seu próximo passo é acessar seu <b>>my<</b> novamente, criar sua equipe e ler as notícias. Para fazer isso, clique no botão abaixo!<br><b>Happy hacking!</b>'.format(settings.HACKATHON_NAME),
        'actionUrl': settings.ROOT_URL + reverse('hackers:login_from_token', args={hacker.token}),
        'actionName': 'Acessar sua conta',
        'project_url': settings.ROOT_URL,
        'hackathon_name': settings.HACKATHON_NAME,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.email
    fr = str(settings.HACKATHON_NAME)
    msg_plain = render_to_string('main/email/action/text.txt', context)
    msg_html = render_to_string('main/email/action/html.html', context)

    send_mail(
        '[{}] Check-in feito!'.format(settings.HACKATHON_NAME),
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )
