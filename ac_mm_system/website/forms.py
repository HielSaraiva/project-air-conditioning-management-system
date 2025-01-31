from django import forms

from .models import Pavilhao, Horario, Sala

# Constante para os dias da semana
DIAS_DA_SEMANA = [
    ('Segunda', 'Segunda-feira'),
    ('Terça', 'Terça-feira'),
    ('Quarta', 'Quarta-feira'),
    ('Quinta', 'Quinta-feira'),
    ('Sexta', 'Sexta-feira'),
    ('Sábado', 'Sábado'),
    ('Domingo', 'Domingo'),
]


# Formulário para o modelo Pavilhao
class PavilhaoModelForm(forms.ModelForm):
    class Meta:
        model = Pavilhao
        fields = [
            'nome',
            'numero_salas',
        ]
        labels = {
            'nome': 'Pavilhão',
            'numero_salas': 'Número de Salas',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'numero_salas': forms.NumberInput(attrs={'placeholder': 'Número', 'min': 1}),
        }


# Formulário para o modelo Horario
class HorarioModelForm(forms.ModelForm):
    dias_da_semana = forms.MultipleChoiceField(
        choices=DIAS_DA_SEMANA,
        widget=forms.CheckboxSelectMultiple,
        label="Dias da Semana"
    )  # Permite escolher mais de um dia da semana

    class Meta:
        model = Horario
        fields = [
            'pavilhao',
            'dias_da_semana',
            'horario_inicio',
            'horario_fim',
        ]
        labels = {
            'pavilhao': 'Pavilhão',
            'horario_inicio': 'Horário de Início',
            'horario_fim': 'Horário de Término',
        }
        widgets = {
            'horario_inicio': forms.TextInput(attrs={'type':'time', 'placeholder': 'HH:mm'}),
            'horario_fim': forms.TextInput(attrs={'type':'time', 'placeholder': 'HH:mm'}),
        }

# Formulário para o modelo Sala
class SalaModelForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = [
            'nome',
            'pavilhao',
            'horario',
        ]
        labels = {
            'nome': 'Sala',
            'pavilhao': 'Pavilhão',
            'horario': 'Horário',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
        }