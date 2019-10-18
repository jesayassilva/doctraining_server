from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register({Doenca, Sintoma, Caso_Clinico,Solicitacao_Alterar_Caso_Clinico,Solicitacao_Alterar_Sintoma_Ou_Doenca,Log})#para o admin reconhecer suas classes
