from django import forms
from .models import Application, Hacker
from .tasks import send_verify_email
from django.conf import settings
import re


class ApplicationBasicForm(forms.ModelForm):
    """ApplicationBasicForm
    Basic info form for the creation and editing of applications
    """

    class Meta:
        model = Hacker
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Primeiro Nome*',
            'last_name': 'Sobrenome*',
            'email': 'Email*',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        pattern = re.compile("^temp_[0-9]+@email.com$")
        if pattern.match(email):
            raise forms.ValidationError('Você precisa fornecer um email válido!')
        return email

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        pre_instance = Hacker.objects.get(id=instance.id)

        # If the email changed, ask for verification
        if instance.email != pre_instance.email:
            instance.unverified = True
        if commit:
            instance.save()
            if instance.unverified:
                instance.new_verification_code()
                send_verify_email.delay(instance.id)
        return instance


class ApplicationForm(forms.ModelForm):
    """ApplicationForm
    Base form for the creation and editing of applications
    """

    class Meta:
        model = Application
        fields = ['phone', 'gender', 'age', 'university', 'enroll_year', 'diet', 'special_needs', 'shirt_size', 'shirt_style', 'cv_type', 'cv', 'cv2_type', 'cv2', 'facebook', 'description', 'essay', 'bus_sp', 'bus_sc', 'sleeping_bag', 'pillow']
        labels = {
            'phone': 'Telefone',
            'gender': 'Gênero*',
            'age': 'Idade*',
            'university': 'Universidade*',
            'enroll_year': 'Ano de Ingresso*',
            'diet': 'Restrição alimentar',
            'special_needs': 'Necessidades especiais',
            'shirt_size': 'Tamanho da Camisa*',
            'shirt_style': 'Estilo da Camisa*',
            'cv_type': 'Tipo de Currículo',
            'cv': 'URL do Currículo',
            'cv2_type': 'Outro tipo de Currículo',
            'cv2': 'URL de outro Currículo',
            'facebook': 'facebook.com/',
            'description': 'Eu me descreveria como...*',
            'essay': 'Por que você quer participar do {}?*'.format(settings.HACKATHON_NAME),
            'bus_sc': 'Preciso de transporte <a class="why">Como assim?</a>',
            'bus_sp': 'Preciso de transporte <a class="why">Como assim?</a>',
            'pillow': '<div style="color: gray;" id="pillow"><i class="ui icon external share"></i>Travesseiro(R$ 35)</div>',
            'sleeping_bag': '<div style="color: gray;" id="sleeping" ><i class="ui icon external share"></i>Saco de Dormir(R$ 70)</div>',
        }

        widgets = {
            'description': forms.fields.TextInput(attrs={'placeholder': 'iOS Master, Data Scientist, Hacker, Designer...'}),
            'special_needs': forms.fields.TextInput(attrs={'placeholder': 'Só responder se tiver'}),
            'diet': forms.fields.TextInput(attrs={'placeholder': 'Só responder se tiver'}),
        }

    def clean_cv(self):
        cv = self.cleaned_data['cv']
        if cv == '':
            return cv
        cv_type = self.cleaned_data['cv_type']
        if cv_type == 'LI' and cv.find('linkedin.com/in/') < 0:
            cv = "https://linkedin.com/in/{}".format(cv)
        if cv_type == 'GH' and cv.find('github.com/') < 0:
            cv = "https://github.com/{}".format(cv)
        if cv.find("://") < 0:
            cv = "https://{}".format(cv)
        return cv

    def clean_cv2(self):
        cv = self.cleaned_data['cv2']
        if cv == '':
            return cv
        cv_type = self.cleaned_data['cv2_type']
        if cv_type == 'LI' and cv.find('linkedin.com/in/') < 0:
            cv = "https://linkedin.com/in/{}".format(cv)
        if cv_type == 'GH' and cv.find('github.com/') < 0:
            cv = "https://github.com/{}".format(cv)
        if cv.find("://") < 0:
            cv = "https://{}".format(cv)
        return cv

    def save(self, commit=True, hacker=None):
        instance = forms.ModelForm.save(self, False)
        instance.hacker = hacker
        instance.hacker.incomplete = False
        if commit:
            instance.save()
        return instance
