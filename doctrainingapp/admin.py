from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register({Doenca, Sintoma, Caso_Clinico,Solicitacao_Alterar_Caso_Clinico,Log, Perfil, Sala, Pergunta })#para o admin reconhecer suas classes
