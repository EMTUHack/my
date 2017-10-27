from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import requests
from collections import OrderedDict
# Create your models here.


@property
def is_hacker(self):
    return hasattr(self, 'hacker')


User.add_to_class('is_hacker', is_hacker)


GENDER_TYPES = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outro')
)
SHIRT_SIZES = (
    ('P', 'P'),
    ('M', 'M'),
    ('G', 'G'),
    ('GG', 'GG'),
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
    email = models.EmailField(unique=True)

    # Team
    team = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING,
        related_name="hackers",
        blank=True,
        null=True
    )

    # Registration
    token = models.CharField(max_length=6, unique=True, null=True, blank=True)
    active = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)
    withdraw = models.BooleanField(default=False)

    # Social Login
    fb_social_id = models.CharField(max_length=50, null=True, blank=True, unique=True)
    gh_social_id = models.CharField(max_length=50, null=True, blank=True, unique=True)

    # Sponsor
    azure_pass = models.CharField(max_length=100, null=True, blank=True, unique=True)

    @property
    def has_fb_login(self):
        return self.fb_social_id is not None

    @property
    def has_gh_login(self):
        return self.gh_social_id is not None

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def has_team(self):
        return self.team is not None

    @property
    def finished_application(self):
        return hasattr(self, 'application') and getattr(self, 'application').completed

    @property
    def state_code(self):
        # Code number grows proportionaly to how far they are from being a valid hacker
        # Checked in - Hackers can only be checked in if they are confirmed as well
        if self.checked_in:
            return 0
        # Check if the hacker hasnt completed their application
        if not self.finished_application:
            # If the application period has ended, thet cant complete their registration
            if not settings.APPLICATION_OPEN:
                return 4
            # Incompleted hackers can still complete their registration
            return 2
        if self.withdraw:
            if not settings.APPLICATION_OPEN:
                return 4
            # withdraw'd hackers don't want to take part in the hackathon
            return 3

        # Else, the hacker is ready to go
        return 1

    @property
    def state(self):
        responses = {
            0: ("checked in", "Check-in realizado"),
            1: ("confirmed", "Tudo Pronto"),
            2: ("incomplete", "Aplicação Incompleta"),
            3: ("withdraw", "Aplicação Cancelada"),
            4: ("late", "Aplicação atrasada"),
        }
        return responses[self.state_code]

    @property
    def is_checkedin(self):
        return self.state[0] == "checked in"

    @property
    def is_confirmed(self):
        return self.state[0] == "confirmed"

    @property
    def is_incomplete(self):
        return self.state[0] == "incomplete"

    @property
    def is_withdraw(self):
        return self.state[0] == "withdraw"

    @property
    def is_late(self):
        return self.state[0] == "late"

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
            ('checked_in', 'Atendeu'),
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
    gender = models.CharField(max_length=1, choices=GENDER_TYPES)
    age = models.IntegerField()
    university = models.CharField(max_length=100)
    enroll_year = models.IntegerField(null=True)
    # Needs
    diet = models.CharField(max_length=100, default="", null=True, blank=True)
    special_needs = models.CharField(max_length=100, default="", null=True, blank=True)
    # Swag
    shirt_size = models.CharField(max_length=3, choices=SHIRT_SIZES)
    # CV
    cv_type = models.CharField(max_length=3, choices=CV_TYPES, null=True, blank=False)
    cv = models.CharField(max_length=300, null=True, blank=False)
    cv2_type = models.CharField(max_length=3, choices=CV_TYPES, null=True, blank=True)
    cv2 = models.CharField(max_length=300, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    # Extra
    description = models.CharField(max_length=100, null=True)
    essay = models.TextField(null=True, blank=True)
    # Purchase
    sleeping_bag = models.BooleanField(default=False)
    pillow = models.BooleanField(default=False)

    # Internal
    completed = models.BooleanField(default=False)

    @property
    def extras(self):
        extras = {
            'pillow': "Travesseiro",
            "sleeping_bag": "Saco de Dormir($40)",
        }
        res = []
        for extra, text in extras.items():
            if getattr(self, extra):
                res.append(text)

        return '<br>'.join(res)

    def export_fields(self, exclude=[]):
        fields = OrderedDict([
            ('phone', 'Celular'),
            ('age', 'Idade'),
            ('university', 'Universidade'),
            ('enroll_year', 'Ano de Ingresso'),
            ('cv_type', 'Tipo do Currículo'),
            ('cv', 'Currículo'),
            ('cv2_type', 'Tipo do Currículo 2'),
            ('cv2', 'Currículo 2'),
            ('facebook', 'Facebook'),
            ('description', 'Descrição'),
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
    if kwargs['created']:
        instance.new_token()
        user = User(
            username=instance.email,
            email=instance.email,
            password=get_random_string(length=12)
        )
        user.set_unusable_password()
        user.save()
        instance.user = user
        instance.save()


# Process hacker deletion
@receiver(post_delete, sender=Hacker, dispatch_uid="hacker_deletion")
def hacker_deletion(sender, instance, **kwargs):
    try:
        if getattr(instance, 'user'):
            instance.user.delete()
    except ObjectDoesNotExist:
        pass
