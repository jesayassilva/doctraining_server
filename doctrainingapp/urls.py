
from django.urls import path
from .views  import  *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from django.conf.urls import url

app_name="doctrainingapp"

urlpatterns = [

    path('', index, name='index'),
    path('login/',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user=True),name='login'),#,redirect_authenticated_user=True
    path('logout/',sair,name='logout'),

    path('doctraining/',login_required(doctraining),name='doctraining'),

    path('user/novo/',login_required(UserCreate.as_view()),name='user_create'),

    path('user/perfil/editar/<int:pk>/',login_required(PerfilUpdate.as_view()),name='perfil_update'),
    path('user/<int:pk>/',login_required(UserUpdate.as_view()),name='user_update'),


    #WEB Solicitações Editar, deletar e novo
    path('casos_clinicos/solicitar/editar/<int:pk>/',login_required(solicitar_editar_caso_clinico), name='solicitar_editar_caso_clinico'),
    path('casos_clinicos/solicitar/novo/',login_required(solicitar_novo_caso_clinico),name='solicitar_novo_caso_clinico'),
    path('casos_clinicos/solicitar/delete/<int:pk>/',login_required(solicitar_deletar_caso_clinico), name='solicitar_deletar_caso_clinico'),



    #WEB Visualizar dados
    path('casos_clinicos/',login_required(casos_clinicos),name='casos_clinicos'),


    #Solicitações de Alteração de dados
    path('casos_clinicos/solicitacoes/',login_required(solicitacoes_alteracao_casos_clinicos),name='solicitacoes_alteracao_casos_clinicos'),
    path('casos_clinicos/solicitacoes/aceitar/<int:pk>/',login_required(aceitar_solicitacao_alteracao_caso_clinico),name='aceitar_solicitacao_alteracao_caso_clinico'),
    path('casos_clinicos/solicitacoes/rejeitar/<int:pk>/',login_required(rejeitar_solicitacao_alteracao_caso_clinico),name='rejeitar_solicitacao_alteracao_caso_clinico'),

    path('casos_clinicos/solicitacoes/log/',login_required(log_solicitacoes_alteracao_casos_clinicos),name='log_solicitacoes_alteracao_casos_clinicos'),

    #Doenca
    path('doenca/<int:pk>/',login_required(doenca),name='doenca'),
    path('doenca/solicitacoes/delete/<int:pk>/',login_required(solicitar_deletar_doenca),name='solicitar_deletar_doenca'),
    path('doenca/nova/',login_required(solicitar_nova_doenca),name='solicitar_nova_doenca'),

    #Sintoma
    path('sintoma/<int:pk>/',login_required(sintoma),name='sintoma'),
    path('sintoma/solicitacoes/delete/<int:pk>/',login_required(solicitar_deletar_sintoma),name='solicitar_deletar_sintoma'),
    path('sintoma/novo/',login_required(solicitar_novo_sintoma),name='solicitar_novo_sintoma'),


    #SALAS
    path('salas/todas/',login_required(todas_salas),name='todas_salas'),
    path('salas/nova/',login_required(Nova_Sala.as_view()),name='nova_sala'),
    path('salas/editar/<int:pk>/',login_required(Editar_Sala.as_view()),name='editar_sala'),
    path('salas/deletar/<int:pk>/',login_required(Deletar_Sala.as_view()),name='delete_sala'),

    # PERGUNTAS
    path('salas/<int:pk_sala>/perguntas/nova/',login_required(nova_pergunta),name='nova_pergunta'),
    path('salas/<int:pk_sala>/perguntas/',login_required(todas_perguntas),name='todas_perguntas'),
    path('salas/editar/perguntas/<int:pk>/',login_required(Editar_Pergunta.as_view()),name='editar_pergunta'),
    path('salas/perguntas/deletar/<int:pk>/',login_required(Deletar_Pergunta.as_view()),name='delete_pergunta'),




    #WEB SERVICE
    path('api/',login_required(api),name='api'),
    path('api/casos_clinicos/nome_doencas/',nome_doencas_casos_clinicos_api,name='nome_doencas_casos_clinicos_api'),
    path('api/casos_clinicos/nome_sintomas/',nome_sintomas_casos_clinicos_api,name='nome_sintomas_casos_clinicos_api'),
    path('api/casos_clinicos/todos/',todos_casos_clinicos_doencas_sintomas_api,name='todos_casos_clinicos_doencas_sintomas_api'),
    path('api/casos_clinicos/um/',um_caso_clinico_doenca_sintomas_api,name='um_caso_clinico_doenca_sintomas_api'),
    path('api/salas/<int:pk_sala>/perguntas/',perguntas_de_uma_sala_api,name='perguntas_de_uma_sala_api'),
    path('api/salas/',todos_salas_api,name='todos_salas_api'),


    #APRENDIZADO DE MÁQUINA controle das threads
    path('ativar_am/', login_required(ativar_am), name='ativar_am'),
    # path('desativar_am/', login_required(desativar_am), name='desativar_am'),
    path('status_am/', login_required(status_am), name='status_am'),
    path('am_agora/', login_required(am_agora), name='am_agora'),
    path('ler_dados_salvar/',ler_dados_salvar),

]
















#
