from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    """ApplicationForm
    Base form for the creation and editing of applications
    """

    class Meta:
        model = Application
        fields = ['phone', 'gender', 'age', 'university', 'enroll_year', 'diet', 'special_needs', 'shirt_size', 'cv_type', 'cv', 'cv2_type', 'cv2', 'facebook', 'sleeping_bag', 'description', 'essay', 'pillow']
        labels = {
            'phone': 'Telefone',
            'gender': 'Gênero*',
            'age': 'Idade*',
            'university': 'Universidade*',
            'enroll_year': 'Ano de Ingresso*',
            'diet': 'Restrição alimentar',
            'special_needs': 'Necessidades especiais',
            'shirt_size': 'Tamanho da Camisa*',
            'cv_type': 'Tipo de Currículo*',
            'cv': 'Currículo*',
            'cv2_type': 'Outro tipo de Currículo',
            'cv2': 'Outro Currículo',
            'facebook': 'facebook.com/',
            'sleeping_bag': '<a target="_blank" href="http://www.decathlon.com.br/camping/sacos-de-dormir-e-colchoes/saco-de-dormir-camping/saco-de-dormir-camping-arpenaz-25-quechua">Saco de Dormir (R$ 40)</a>',
            'pillow': '<a target="_blank" href="">Travesseiro (R$ 20)</a>',
            'description': 'Eu me descreveria como...*',
            'essay': 'Por que você quer participar do Hack the Campus?',
        }

        widgets = {
            'description': forms.fields.TextInput(attrs={'placeholder': 'iOS Master, Data Scientist, Hacker, Designer...'}),
        }

    def save(self, commit=True, hacker=None):
        instance = forms.ModelForm.save(self, False)
        instance.hacker = hacker
        instance.completed = True
        if commit:
            instance.save()
        return instance
