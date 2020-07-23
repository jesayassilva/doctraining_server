
from django.forms import ModelForm
from doctrainingapp.models import Versao



class VersaoForm(ModelForm):
    class Meta:
        model = Versao
        fields = ['versao', 'informacao', 'nova_versao', 'atualizacao_critica']


    def __init__(self, *args, **kwargs):
        super(VersaoForm, self).__init__(*args, **kwargs)

        self.fields['versao'].widget.attrs['class'] = 'ui form'
        self.fields['informacao'].widget.attrs['class'] = 'ui form'
        self.fields['nova_versao'].widget.attrs['class'] = 'ui form'
        self.fields['atualizacao_critica'].widget.attrs['class'] = 'ui form'
