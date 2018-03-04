from django import forms
from .models import Application, Hacker
from .tasks import send_verify_email


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

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        pre_instance = Hacker.objects.get(id=instance.id)

        # If the email changed, ask for verification
        if instance.email != pre_instance.email:
            instance.unverified = True
        if commit:
            if instance.unverified:
                instance.new_verification_code()
            instance.save()
            send_verify_email.delay(instance.id)
        return instance


class ApplicationForm(forms.ModelForm):
    """ApplicationForm
    Base form for the creation and editing of applications
    """

    class Meta:
        model = Application
        fields = ['phone', 'gender', 'age', 'university', 'enroll_year', 'diet', 'special_needs', 'shirt_size', 'shirt_style', 'cv_type', 'cv', 'cv2_type', 'cv2', 'facebook', 'sleeping_bag', 'description', 'essay', 'pillow']
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
            'cv_type': 'Tipo de Currículo*',
            'cv': 'Currículo (Válido)* <a id="why">Por quê?</a>',
            'cv2_type': 'Outro tipo de Currículo',
            'cv2': 'Outro Currículo',
            'facebook': 'facebook.com/',
            'sleeping_bag': '<div style="color: gray;" id="sleeping" ><i class="ui icon external share"></i>Saco de Dormir(R$ 40)</div>',
            'pillow': '<div style="color: gray;" id="pillow"><i class="ui icon external share"></i>Travesseiro(R$ 35)</div>',
            'description': 'Eu me descreveria como...*',
            'essay': 'Por que você quer participar do Hack the Campus?',
        }

        widgets = {
            'description': forms.fields.TextInput(attrs={'placeholder': 'iOS Master, Data Scientist, Hacker, Designer...'}),
        }

    def save(self, commit=True, hacker=None):
        instance = forms.ModelForm.save(self, False)
        instance.hacker = hacker
        instance.hacker.incomplete = False
        if commit:
            instance.save()
        return instance
