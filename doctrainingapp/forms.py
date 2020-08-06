
from django.forms import ModelForm
from doctrainingapp.models import Versao, Sala, Area



class VersaoForm(ModelForm):
    class Meta:
        model = Versao
        fields = ['versao', 'informacao', 'atualizacao_critica']


    def __init__(self, *args, **kwargs):
        super(VersaoForm, self).__init__(*args, **kwargs)

        self.fields['versao'].widget.attrs['class'] = 'ui form'
        self.fields['informacao'].widget.attrs['class'] = 'ui form'
        self.fields['atualizacao_critica'].widget.attrs['class'] = 'ui form'


class SalaForm(ModelForm):
    class Meta:
        model = Sala
        fields = ['nome_sala','descricao']


    def __init__(self, *args, **kwargs):
        super(SalaForm, self).__init__(*args, **kwargs)
        self.fields['nome_sala'].widget.attrs['class'] = 'ui form'
        self.fields['descricao'].widget.attrs['class'] = 'ui form'

class AreaForm(ModelForm):
    class Meta:
        model = Area
        fields = ['nome']


    def __init__(self, *args, **kwargs):
        super(AreaForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['class'] = 'ui form'








