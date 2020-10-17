import io
from django.forms import ModelForm
from django import forms
import json

from doctrainingapp.models import Versao, Area, Conteudo, Fase, Sala, AreaFase



class VersaoForm(ModelForm):
    class Meta:
        model = Versao
        fields = ['versao', 'informacao', 'atualizacao_critica']


    def __init__(self, *args, **kwargs):
        super(VersaoForm, self).__init__(*args, **kwargs)

        self.fields['versao'].widget.attrs['class'] = 'ui form'
        self.fields['informacao'].widget.attrs['class'] = 'ui form'
        self.fields['atualizacao_critica'].widget.attrs['class'] = 'ui form'

class AreaForm(ModelForm):
    class Meta:
        model = Area
        fields = ['nome']


    def __init__(self, *args, **kwargs):
        super(AreaForm, self).__init__(*args, **kwargs)

        self.fields['nome'].widget.attrs['class'] = 'ui form'

class AreaFaseForm(ModelForm):
    class Meta:
        model = AreaFase
        fields = ['nome']


    def __init__(self, *args, **kwargs):
        super(AreaFaseForm, self).__init__(*args, **kwargs)

        self.fields['nome'].widget.attrs['class'] = 'ui form'

class FaseForm(ModelForm):
    class Meta:
        model = Fase
        fields = ['nome_fase','descricao', 'dificuldade', 'imagem1', 'imagem2', 'imagem3' ]


    def __init__(self, *args, **kwargs):
        super(FaseForm, self).__init__(*args, **kwargs)

        self.fields['nome_fase'].widget.attrs['class'] = 'ui form'
        self.fields['descricao'].widget.attrs['class'] = 'ui form'
        self.fields['dificuldade'].widget.attrs['class'] = 'ui form'

class SalaForm(ModelForm):
    class Meta:
        model = Sala
        fields = ['nome_sala','descricao' ]


    def __init__(self, *args, **kwargs):
        super(SalaForm, self).__init__(*args, **kwargs)

        self.fields['nome_sala'].widget.attrs['class'] = 'ui form'
        self.fields['descricao'].widget.attrs['class'] = 'ui form'

class ConteudoForm(ModelForm):


    class Meta:
        model = Conteudo
        fields = ['area','sala', 'titulo', 'descricao', 'conteudo', 'link', 'referencia', 'imagem1', 'imagem2', 'imagem3']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sala'].queryset = Sala.objects.none()

        if 'area' in self.data:
            try:
                country_id = int(self.data.get('area'))
                self.fields['sala'].queryset = Sala.objects.filter(area_id=country_id).order_by('nome_sala')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['sala'].queryset = self.instance.area.sala_set.order_by('nome_sala')


class UploadAreaForm(forms.Form):
    data_file = forms.FileField()
