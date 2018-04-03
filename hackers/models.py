from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.validators import MinValueValidator
import requests
from main.models import Settings
from .tasks import send_notify_admitted, send_notify_unwaitlist, send_notify_waitlist, send_notify_decline, send_notify_nag
from collections import OrderedDict
# Create your models here.


@property
def is_hacker(self):
    return hasattr(self, 'hacker')


User.add_to_class('is_hacker', is_hacker)


GENDER_TYPES = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outro'),
    ('NA', 'Prefiro não dizer'),
)
SHIRT_SIZES = (
    ('P', 'P'),
    ('M', 'M'),
    ('G', 'G'),
    ('GG', 'GG'),
)
SHIRT_STYLE = (
    ('Normal', 'Normal'),
    ('Babylook', 'Babylook'),
)
CV_TYPES = (
    ('LI', 'LinkedIn'),
    ('GH', 'GitHub'),
    ('WS', 'Website'),
    ('OT', 'Outro')
)

MAX_TEAM_SIZE = settings.TEAM_MAX_SIZE

TOKEN_SIZE = settings.TOKEN_SIZE


class Team(models.Model):
    """docstring for Team"""
    name = models.CharField(max_length=20, unique=True)
    project = models.CharField(max_length=300, default="")
    location = models.CharField(max_length=20, default="")
    github_url = models.CharField(max_length=200, default="")

    block_new_members = models.BooleanField(default=False)

    @property
    def size(self):
        return len(self.hackers.all())

    @property
    def is_full(self):
        return self.size >= MAX_TEAM_SIZE or self.block_new_members

    def __str__(self):
        return "{} @ {} ({})".format(self.name, self.location, self.size)


class Hacker(models.Model):
    """docstring for Hacker"""

    user = models.OneToOneField(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    # Basic info
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200, default="", blank=True)
    email = models.EmailField(unique=True)

    @property
    def name(self):
        return "{} {}".format(self.first_name.strip(), self.last_name.strip())

    # Team
    team = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING,
        related_name="hackers",
        blank=True,
        null=True
    )

    # Registration
    token = models.CharField(max_length=20, unique=True, null=True, blank=True)

    # Registration Status
    active = models.BooleanField(default=False)  # Active hackers are those that log in at least once
    incomplete = models.BooleanField(default=True)
    unverified = models.BooleanField(default=False)

    verification_code = models.CharField(max_length=20, unique=True, null=True, blank=True)

    @property
    def submitted(self):
        return not self.incomplete and not self.unverified

    admitted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    waitlist = models.BooleanField(default=False)
    waitlist_date = models.DateTimeField(auto_now_add=True)
    checked_in = models.BooleanField(default=False)
    withdraw = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)

    # Social Login
    fb_social_id = models.CharField(max_length=50, null=True, blank=True, unique=False)
    gh_social_id = models.CharField(max_length=50, null=True, blank=True, unique=False)

    # Sponsor
    # azure_pass = models.CharField(max_length=100, null=True, blank=True, unique=True)

    @property
    def has_fb_login(self):
        return self.fb_social_id is not None and self.fb_social_id != ''

    @property
    def has_gh_login(self):
        return self.gh_social_id is not None and self.gh_social_id != ''

    @property
    def has_team(self):
        return self.team is not None

    @property
    def finished_application(self):
        return hasattr(self, 'application') and not self.incomplete

    @property
    def state(self):
        # Code number grows proportionaly to how far they are from being a valid hacker
        if self.checked_in:
            return ("checkedin", "Check-in Realizado")
        if self.confirmed:
            return ("confirmed", "Confirmado")
        if not Settings.can_confirm(self.waitlist):
            return ("late", "Inscrições Encerradas")
        if self.withdraw:
            return ("withdraw", "Desistência")
        if self.waitlist:
            return ("waitlist", "Fila de Espera")
        if self.admitted:
            return ("admitted", "Aplicação Aprovada")
        if self.declined:
            return ("declined", "Aplicação Recusada")
        if self.submitted:
            return ("submitted", "Aplicação Enviada")
        if not Settings.registration_is_open():
            return ("late", "Inscrições Encerradas")
        if self.unverified:
            return ("unverified", "Confirmar Email")
        if self.incomplete:
            return ("incomplete", "Aplicação Incompleta")
        return ("unknown", "unknown")

    @property
    def is_checkedin(self):
        # Is present at the event
        return self.state[0] == "checkedin"

    @property
    def is_confirmed(self):
        # Was admitted and confirmed that can go
        return self.state[0] == "confirmed"

    @property
    def is_withdraw(self):
        # Withdrew from the event. If decides to return, must be put on waitlist
        return self.state[0] == "withdraw"

    @property
    def is_waitlist(self):
        # Was admitted but the maximum number of hackers was exceeded.
        # Will be unwaitlisted as people withdraw or on the day after confirmation date.
        return self.state[0] == "waitlist"

    @property
    def is_admitted(self):
        # Was admitted and can confirm or withdraw from the event
        return self.state[0] == "admitted"

    @property
    def is_declined(self):
        # Was declined
        return self.state[0] == "declined"

    @property
    def is_submitted(self):
        # Submitted their application for review
        return self.state[0] == "submitted"

    @property
    def is_late(self):
        # Did not confirm their presence by the specified date
        return self.state[0] == "late"

    @property
    def is_unverified(self):
        # Did not verify their email address
        return self.state[0] == "unverified"

    @property
    def is_incomplete(self):
        # Application is still incomplete
        return self.state[0] == "incomplete"

    def admit(self):
        self.admitted = True
        self.declined = False
        self.waitlist = False
        self.withdraw = False
        self.save()
        if Settings.hackathon_is_full():
            return self.put_on_waitlist()
        send_notify_admitted.delay(self.id)

    def nag(self):
        # Send nag notification remembering that
        # the hacker has been admitted
        send_notify_nag.delay(self.id)

    def decline(self):
        self.admitted = False
        self.declined = True
        self.waitlist = False
        self.withdraw = False
        self.save()
        send_notify_decline.delay(self.id)
        from main.util import cycle_waitlist
        cycle_waitlist(1)

    def put_on_waitlist(self):
        self.waitlist = True
        self.waitlist_date = timezone.now()
        self.save()

        send_notify_waitlist.delay(self.id)

    def unwaitlist(self):
        self.waitlist = False
        self.save()
        send_notify_unwaitlist.delay(self.id)

    def withdraw_from_event(self):
        self.confirmed = False
        self.withdraw = True
        self.save()
        from main.util import cycle_waitlist
        cycle_waitlist(1)

    def confirm(self):
        self.confirmed = True
        self.save()

    # Enter or Create Team method
    def enter_team(self, name):
        team = Team.objects.filter(name=name).first()

        # if hacker already has a team, leave it first
        if self.has_team:
            self.leave_team()

        if team is None:
            # If team does not exist, create it
            team = Team(name=name)
            team.save()
            team.hackers.add(self)
        elif team.is_full:
            # Returns none if team is full.
            # Make it an exception later
            return None
        else:
            # Join team
            team.hackers.add(self)

        return self.team

    def leave_team(self):
        team = self.team
        team.hackers.remove(self)

    def new_verification_code(self):
        code = get_random_string(length=TOKEN_SIZE)
        if Hacker.objects.filter(verification_code=code).first() is not None:
            return self.new_verification_code()
        self.verification_code = code
        self.save()
        return self.verification_code

    def new_token(self):
        from staff.models import Staff
        token = get_random_string(length=TOKEN_SIZE)
        if Hacker.objects.filter(token=token).first() is not None or Staff.objects.filter(token=token).first() is not None:
            return self.new_token()
        self.token = token
        self.save()
        return self.token

    def get_azure_pass(self, i=0, passes=[]):
        if passes == []:
            if settings.AZURE_PASSES is None:
                return
            file = requests.get(settings.AZURE_PASSES).text
            passes = eval('["' + file.replace('\r\n', '", "') + '"]')

        if i >= len(passes):
            return

        azure = passes[i]
        if Hacker.objects.filter(azure_pass=azure).first() is not None:
            return self.get_azure_pass(i + 1, passes)
        self.azure_pass = azure
        self.save()
        return self.azure_pass

    def export_fields(self, exclude=[]):
        fields = OrderedDict([
            ('first_name', 'Primeiro Nome'),
            ('last_name', 'Sobrenome'),
            ('email', 'Email'),
            ('state', 'Estado'),
            ('team', 'Nome da Equipe')
        ])
        res = OrderedDict()
        for ex in exclude:
            if fields.get(ex, False):
                fields.pop(ex)

        for k, v in fields.items():
            res[v] = getattr(self, k)
        return res

    @staticmethod
    def create(**kwargs):
        first_name = kwargs.pop("first_name")
        last_name = kwargs.pop("last_name")
        email = kwargs.pop("email")
        hacker = Hacker(first_name=first_name, last_name=last_name, email=email)
        hacker.save()
        if len(kwargs) > 0:
            app = Application(**kwargs)
            app.hacker = hacker
            app.save()
        return hacker

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Application(models.Model):
    """docstring for Application"""
    hacker = models.OneToOneField(
        Hacker,
        on_delete=models.CASCADE
    )
    # Communication
    phone = models.CharField(max_length=20, null=True, blank=True)
    # Basic
    gender = models.CharField(max_length=2, choices=GENDER_TYPES)
    age = models.IntegerField(validators=[MinValueValidator(18, "A idade mínima é 18 anos.")])
    university = models.CharField(max_length=100)
    enroll_year = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    # Needs
    diet = models.CharField(max_length=100, default="", null=True, blank=True)
    special_needs = models.CharField(max_length=100, default="", null=True, blank=True)
    # Swag
    shirt_size = models.CharField(max_length=3, choices=SHIRT_SIZES)
    shirt_style = models.CharField(max_length=15, choices=SHIRT_STYLE)
    # CV
    cv_type = models.CharField(max_length=3, choices=CV_TYPES, null=True, blank=True)
    cv = models.CharField(max_length=300, null=True, blank=True)
    cv2_type = models.CharField(max_length=3, choices=CV_TYPES, null=True, blank=True)
    cv2 = models.CharField(max_length=300, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    # Extra
    description = models.CharField(max_length=100, null=True)
    essay = models.TextField(null=True, blank=False)
    # Purchase
    sleeping_bag = models.BooleanField(default=False)
    pillow = models.BooleanField(default=False)
    # Bus tickets
    bus_sc = models.BooleanField(default=False)
    bus_sp = models.BooleanField(default=True)

    @property
    def shirt_string(self):
        return "[{}]{} {}".format(self.gender, self.shirt_size, self.shirt_style)

    @property
    def eligible_bus_spot(self):
        if self.bus_sp:
            sp = Application.objects.filter(hacker__confirmed=True).filter(bus_sp=True).filter(created__lte=self.created)
            if len(sp) < Settings.get().max_bus_spots:
                return True
        elif self.bus_sc:
            sc = Application.objects.filter(hacker__confirmed=True).filter(bus_sc=True).filter(created__lte=self.created)
            if len(sc) < Settings.get().max_bus_spots:
                return True
        return False

    @property
    def extras(self):
        extras = {
            'pillow': "Travesseiro($35)",
            "sleeping_bag": "Saco de Dormir($70)",
        }
        res = []
        for extra, text in extras.items():
            if getattr(self, extra):
                res.append(text)

        return '<br>'.join(res)

    def export_fields(self, exclude=['gender', 'shirt_size', 'shirt_style', 'special_needs', 'diet', 'essay', 'bus_sp', 'bus_sc']):
        fields = OrderedDict([
            ('phone', 'Celular'),
            ('age', 'Idade'),
            ('gender', 'Gênero'),
            ('university', 'Universidade'),
            ('enroll_year', 'Ano de Ingresso'),
            ('shirt_size', 'Tamanho da Camisa'),
            ('shirt_style', 'Tipo da Camisa'),
            ('special_needs', 'Necessidades Especiais'),
            ('diet', 'Dieta'),
            ('cv_type', 'Tipo do Currículo'),
            ('cv', 'Currículo'),
            ('cv2_type', 'Tipo do Currículo 2'),
            ('cv2', 'Currículo 2'),
            ('facebook', 'Facebook'),
            ('description', 'Descrição'),
            ('essay', 'Motivação'),
            ('bus_sp', 'Transporte de SP'),
            ('bus_sc', 'Transporte de SC')
        ])
        res = OrderedDict()
        for ex in exclude:
            if fields.get(ex, False):
                fields.pop(ex)

        simple_cv = OrderedDict(list(CV_TYPES))

        def simplify_cv(val):
            return simple_cv.get(val, val)

        for k, v in fields.items():
            res[v] = getattr(self, k) if k not in ['cv_type', 'cv2_type'] else simplify_cv(getattr(self, k))
        return res

    def __str__(self):
        return "{} {}".format(self.hacker.first_name, self.hacker.last_name)


# Process hacker creation
@receiver(post_save, sender=Hacker, dispatch_uid="hacker_creation")
def hacker_creation(sender, instance, **kwargs):
    instance.full_name = "{} {}".format(instance.first_name.strip(), instance.last_name.strip())
    if kwargs['created']:
        instance.new_token()
        if getattr(instance, 'user', None) is None:
            user = User(
                username=instance.email,
                email=instance.email,
                password=get_random_string(length=12)
            )
            user.set_unusable_password()
            user.save()
            instance.user = user
        instance.save()
