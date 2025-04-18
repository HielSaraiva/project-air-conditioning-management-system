import re

from django import forms
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower

from .models import Pavilhao, Horario, Sala, ArCondicionado, Grafico

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

TURNOS = [
    ('Matutino', 'Matutino'),
    ('Vespertino', 'Vespertino'),
    ('Noturno', 'Noturno'),
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

    def clean_numero_salas(self):
        numero_salas = self.cleaned_data.get('numero_salas')

        if self.instance and self.instance.pk:  # Certifica-se de que estamos na edição de um objeto existente no banco de dados
            numero_salas_existente = self.instance.salas.count()

            if numero_salas < numero_salas_existente:
                raise ValidationError(
                    f"O número de salas não pode ser reduzido para abaixo de {numero_salas_existente}, pois já existem salas cadastradas no pavilhão."
                )

        return numero_salas


# Formulário para o modelo Sala
class SalaModelForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = [
            'nome',
            'pavilhao',
        ]
        labels = {
            'nome': 'Sala',
            'pavilhao': 'Pavilhão',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if usuario is not None:
            self.fields['pavilhao'].queryset = Pavilhao.objects.filter(usuario=usuario).order_by(Lower('nome'))

    def clean_pavilhao(self):
        pavilhao = self.cleaned_data.get('pavilhao')

        if pavilhao:
            # Exclui a sala atual da contagem se estiver em edição
            salas_existentes = pavilhao.salas.all()
            if self.instance.pk:
                salas_existentes = salas_existentes.exclude(pk=self.instance.pk)
            if salas_existentes.count() >= pavilhao.numero_salas:
                raise ValidationError(
                    f"O pavilhão '{pavilhao.nome}' já atingiu o número máximo de salas permitido ({pavilhao.numero_salas})."
                )
        return pavilhao

    def clean_nome(self):
        nome = self.cleaned_data.get("nome")
        if not re.match(r'^[a-zA-Z0-9 ]+$', nome):
            raise forms.ValidationError("O nome da sala só pode conter letras, números e espaços.")
        return nome

    def save(self, commit=True):
        sala = super().save(commit=False)
        sala.nome = re.sub(r'[^a-zA-Z0-9 ]', '', sala.nome)  # Remove caracteres especiais
        sala.topico_mqtt = sala.nome.lower().replace(" ", "_")  # Formata o tópico MQTT

        if commit:
            sala.save()
        return sala


# Formulário para o modelo ArCondicionado
class ArCondicionadoModelForm(forms.ModelForm):
    class Meta:
        model = ArCondicionado
        fields = [
            'nome',
            'sala',
            'consumo',
            'consumo_unidade'
        ]
        labels = {
            'nome': 'Ar-condicionado',
            'consumo': 'Consumo'
        }
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'consumo': forms.NumberInput(attrs={'placeholder': '(kWh/mês ou kWh/ano)', 'min': 0.1}),
            'consumo_unidade': forms.Select(attrs={'placeholder': 'Unidade'}),
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if usuario is not None:
            self.fields['sala'].queryset = Sala.objects.filter(pavilhao__usuario=usuario).order_by(Lower('nome'))

    def clean_sala(self):
        sala = self.cleaned_data.get('sala')
        if sala:
            # Exclui o ar-condicionado atual da contagem se estiver em edição
            ares_existentes = sala.ares_condicionados.all()
            if self.instance.pk:
                ares_existentes = ares_existentes.exclude(pk=self.instance.pk)
            if ares_existentes.count() >= 3:
                raise ValidationError("Já existem 3 ar-condicionados registrados para esta sala.")
        return sala


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
            'sala',
            'dias_da_semana',
            'horario_inicio',
            'horario_fim',
        ]
        labels = {
            'sala': 'Sala',
            'horario_inicio': 'Horário de Início',
            'horario_fim': 'Horário de Término',
        }
        widgets = {
            'horario_inicio': forms.TextInput(attrs={'type': 'time', 'placeholder': 'HH:mm'}),
            'horario_fim': forms.TextInput(attrs={'type': 'time', 'placeholder': 'HH:mm'}),
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['dias_da_semana'] = self.instance.dias_da_semana.split(
                ",") if self.instance.dias_da_semana else []
        if usuario is not None:
            self.fields['sala'].queryset = Sala.objects.filter(pavilhao__usuario=usuario).order_by(Lower('nome'))

    def clean_dias_da_semana(self):
        return ",".join(self.cleaned_data['dias_da_semana'])


class GraficoModelForm(forms.ModelForm):
    class Meta:
        model = Grafico
        fields = ['valor_kWh']
        labels = {
            'valor_kWh': 'Valor em R$ por kWh',
        }
        widgets = {
            'valor_kWh': forms.NumberInput(attrs={'placeholder': 'Valor em R$ por kWh'}),
        }
