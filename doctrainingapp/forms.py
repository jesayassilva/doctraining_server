
from django.forms import ModelForm
from doctrainingapp.models import Versao, Area, Conteudo, Fase



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

class FaseForm(ModelForm):
    class Meta:
        model = Fase
        fields = ['caso_clinico','nome_fase','descricao', 'dificuldade' ]


    def __init__(self, *args, **kwargs):
        super(FaseForm, self).__init__(*args, **kwargs)

        self.fields['caso_clinico'].widget.attrs['class'] = 'ui form'
        self.fields['nome_fase'].widget.attrs['class'] = 'ui form'
        self.fields['descricao'].widget.attrs['class'] = 'ui form'
        self.fields['dificuldade'].widget.attrs['class'] = 'ui form'

class ConteudoForm(ModelForm):
    class Meta:
        model = Conteudo
        fields = ['area', 'titulo', 'descricao', 'conteudo', 'link', 'referencia', 'imagem']


    def __init__(self, *args, **kwargs):
        super(ConteudoForm, self).__init__(*args, **kwargs)

        self.fields['area'].widget.attrs['class'] = 'ui form'
        self.fields['titulo'].widget.attrs['class'] = 'ui form'
        self.fields['descricao'].widget.attrs['class'] = 'ui form'
        self.fields['conteudo'].widget.attrs['class'] = 'ui form'
        self.fields['link'].widget.attrs['class'] = 'ui form'
        self.fields['referencia'].widget.attrs['class'] = 'ui form'
        self.fields['imagem'].widget.attrs['class'] = 'ui form'


