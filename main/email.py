from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse

hack_name = settings.HACKATHON_NAME


def recover_token_email(hacker):
    context = {
        'title': 'Recuperação de Token',
        'subtitle': '',
        'description': 'Você está recebendo essa mensagem pois alguém pediu para que o seu token fosse recuperado.<br><br>Seu token atual é <b>{}</b> e você pode logar em sua conta usando o botão abaixo'.format(hacker.token),
        'actionUrl': settings.ROOT_URL + reverse('main:login_from_token', args={hacker.token}),
        'actionName': 'Acessar sua conta',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.email
    fr = str(settings.DEFAULT_FROM_EMAIL)
    msg_plain = render_to_string('main/email/action/text.txt', context)
    msg_html = render_to_string('main/email/action/html.html', context)

    send_mail(
        '[{}] Recuperar Token'.format(hack_name),
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def verify_email(hacker):
    context = {
        'title': 'Verificação de Email',
        'subtitle': '',
        'description': 'Você está recebendo essa mensagem pois alterou seu email.<br><br>Use o botão abaixo para verificar seu email:',
        'actionUrl': settings.ROOT_URL + reverse('main:verify_email', args={hacker.verification_code}),
        'actionName': 'Verificar Email',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.email
    fr = str(settings.DEFAULT_FROM_EMAIL)
    msg_plain = render_to_string('main/email/action/text.txt', context)
    msg_html = render_to_string('main/email/action/html.html', context)

    send_mail(
        '[{}] Verificar email'.format(hack_name),
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def notify_checkin(hacker):
    context = {
        'title': 'Check-in feito',
        'subtitle': 'Prepare-se!',
        'description': 'Seu check-in no {} foi feito! Ficamos felizes que você pôde vir e esperamos que você se divirta!<br>Seu próximo passo é acessar seu <b>>my<</b> novamente, criar sua equipe e ler as notícias. Para fazer isso, clique no botão abaixo!<br><b>Happy hacking!</b>'.format(hack_name),
        'actionUrl': settings.ROOT_URL + reverse('main:login_from_token', args={hacker.token}),
        'actionName': 'Acessar sua conta',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.email
    fr = str(hack_name)
    msg_plain = render_to_string('main/email/action/text.txt', context)
    msg_html = render_to_string('main/email/action/html.html', context)

    send_mail(
        '[{}] Check-in feito!'.format(hack_name),
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def notify_admitted(hacker):
    context = {
        'title': 'Informações importantes',
        'subtitle': 'Leia tudo!',
        'description': 'Avaliamos sua aplicação e queremos você no {}!<br><b>Atenção!</b> Seu próximo passo é acessar seu <b>>my<</b> novamente para confirmar seu interesse em participar.<br><br><b>Não confirmar seu interesse resultará na perda de sua vaga!</b><br><br><b>Não tem interesse?</b> Declare que vai se abster para que sua vaga possa ser cedida a alguém na fila de espera.'.format(hack_name),
        'actionUrl': settings.ROOT_URL + reverse('main:login_from_token', args={hacker.token}),
        'actionName': 'Acessar sua conta',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.email
    fr = str(hack_name)
    msg_plain = render_to_string('main/email/action/text.txt', context)
    msg_html = render_to_string('main/email/action/html.html', context)

    send_mail(
        '[{}] Aplicação aceita!'.format(hack_name),
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def notify_nag(hacker):
    context = {
        'title': '[Lembrete] Informações importantes',
        'subtitle': 'Leia tudo!',
        'description': 'Avaliamos sua aplicação e queremos você no {}!<br><b>Atenção!</b> Seu próximo passo é acessar seu <b>>my<</b> novamente para confirmar seu interesse em participar.<br><br><b>Não confirmar seu interesse resultará na perda de sua vaga!</b><br><br><b>Não tem interesse?</b> Declare que vai se abster para que sua vaga possa ser cedida a alguém na fila de espera.'.format(hack_name),
        'actionUrl': settings.ROOT_URL + reverse('main:login_from_token', args={hacker.token}),
        'actionName': 'Acessar sua conta',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.email
    fr = str(hack_name)
    msg_plain = render_to_string('main/email/action/text.txt', context)
    msg_html = render_to_string('main/email/action/html.html', context)

    send_mail(
        '[{}] Ação necessária!'.format(hack_name),
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def notify_waitlist(hacker):
    context = {
        'title': 'Foi por pouco!',
        'subtitle': 'Leia tudo!',
        'description': 'Sua aplicação para o {} foi aceita, mas infelizmente nós já atingimos o máximo de participantes.<br><b>Não perca as esperanças!</b> Alguém ainda pode desistir até o dia da confirmação de interesse e a vaga abrir para você.<br>Você receberá um <b>email</b> no instante que isso acontecer, então fique de olhos abertos!'.format(hack_name),
        'actionUrl': settings.ROOT_URL + reverse('main:login_from_token', args={hacker.token}),
        'actionName': 'Acessar sua conta',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.email
    fr = str(hack_name)
    msg_plain = render_to_string('main/email/action/text.txt', context)
    msg_html = render_to_string('main/email/action/html.html', context)

    send_mail(
        '[{}] Fila de Espera'.format(hack_name),
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def notify_unwaitlist(hacker):
    context = {
        'title': 'Abriu uma vaga!',
        'subtitle': 'Leia tudo!',
        'description': 'Alguém desistiu e uma vaga foi aberta para você no {}!<br><b>Atenção!</b> Seu próximo passo é acessar seu <b>>my<</b> novamente para confirmar seu interesse em participar.<br><br><b>Não confirmar seu interesse resultará na perda de sua vaga!</b><br><br><b>Não tem interesse?</b> Declare que vai se abster para que sua vaga possa ser cedida a alguém na fila de espera.<br> Para fazer isso, clique no botão abaixo:'.format(hack_name),
        'actionUrl': settings.ROOT_URL + reverse('main:login_from_token', args={hacker.token}),
        'actionName': 'Acessar sua conta',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.email
    fr = str(hack_name)
    msg_plain = render_to_string('main/email/action/text.txt', context)
    msg_html = render_to_string('main/email/action/html.html', context)

    send_mail(
        '[{}] Abriu uma vaga!'.format(hack_name),
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def notify_decline(hacker):
    context = {
        'title': 'Sentimos muito',
        'subtitle': '',
        'description': 'Avaliamos sua aplicação e infelizmente decidimos que você não poderá fazer parte dessa edição do {}.<br>Esperamos ver você em edições futuras!'.format(hack_name),
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.email
    fr = str(hack_name)
    msg_plain = render_to_string('main/email/basic/text.txt', context)
    msg_html = render_to_string('main/email/basic/html.html', context)

    send_mail(
        '[{}] Sobre sua aplicação'.format(hack_name),
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def notify_late(hacker):
    context = {
        'title': 'Segunda chance',
        'subtitle': 'Você tem uma segunda chance!',
        'description': 'Você recebeu uma segunda chance de completar sua aplicação para o {}.<br>Assim que sua aplicação estiver completa, você poderá fazer seu check-in.<br>Seu próximo passo é acessar seu <b>>my<</b> para preencher seus dados'.format(hack_name),
        'actionUrl': settings.ROOT_URL + reverse('main:login_from_token', args={hacker.token}),
        'actionName': 'Acessar sua conta',
        'project_url': settings.ROOT_URL,
        'hackathon_name': hack_name,
        'facebookHandle': settings.FACEBOOK_HANDLE
    }
    to = hacker.email
    fr = str(hack_name)
    msg_plain = render_to_string('main/email/action/text.txt', context)
    msg_html = render_to_string('main/email/action/html.html', context)

    send_mail(
        '[{}] Segunda chance!'.format(hack_name),
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )
