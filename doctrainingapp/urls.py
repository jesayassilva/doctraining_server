
from django.urls import path
from .views  import  *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from django.conf.urls import url

app_name="doctrainingapp"

urlpatterns = [
    # path('login/',auth_views.LoginView.as_view(template_name="core_app/login.html",redirect_authenticated_user=True),name='Login'),
    # path('logout/',auth_views.LogoutView.as_view(template_name="core_app/logout.html"),name='Logout'),
    # path('',login_required(index),name='Index'),
    # path('candidato/add/',login_required(CandidatoCreate.as_view()),name='Add_Candidato'),
    # path('candidato/up/<int:pk>/', login_required(CandidatoUpdateView.as_view()), name='Update_Candidato'),
    # path('candidato/del/<int:pk>/', login_required(CandidatoDeleteView.as_view()), name='Delete_Candidato'),
    path('', index, name='index'),
    path('login/',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user=True),name='login'),#,redirect_authenticated_user=True
    path('logout/',sair,name='logout'),
    #path('logout/',auth_views.LogoutView.as_view(template_name="core_app/logout.html"),name='Logout'),



    # #WEB Solicitações Editar, deletar e novo
    # path('casos_clinicos/solicitar/editar/<int:pk>/',solicitar_editar_caso_clinico, name='solicitar_editar_caso_clinico'),
    # path('casos_clinicos/solicitar/novo/',solicitar_novo_caso_clinico,name='solicitar_novo_caso_clinico'),
    # path('casos_clinicos/solicitar/delete/<int:pk>/',solicitar_deletar_caso_clinico, name='solicitar_deletar_caso_clinico'),
    # #WEB Visualizar dados
    # path('casos_clinicos/',casos_clinicos,name='casos_clinicos'),

    #trocar
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


    path('casos_clinicos/solicitacoes/log',login_required(log_solicitacoes_alteracao_casos_clinicos),name='log_solicitacoes_alteracao_casos_clinicos'),



    #WEB SERVICE
    path('api/',api,name='api'),
    path('api/casos_clinicos/nome_doencas/',nome_doencas_casos_clinicos_api,name='nome_doencas_casos_clinicos_api'),
    path('api/casos_clinicos/nome_sintomas/',nome_sintomas_casos_clinicos_api,name='nome_sintomas_casos_clinicos_api'),
    path('api/casos_clinicos/todos/',todos_casos_clinicos_doencas_sintomas_api,name='todos_casos_clinicos_doencas_sintomas_api'),
    path('api/casos_clinicos/um/',um_caso_clinico_doenca_sintomas_api,name='um_caso_clinico_doenca_sintomas_api'),



    path('ler_dados_salvar/',ler_dados_salvar),

]
