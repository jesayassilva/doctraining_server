from .views_pack import views_versao, views_api, views_ia, views_firebase, views_areafase, views_user, views_backup, views_area, views_conteudo, views_fases, views_upload
from django.urls import path
from .views  import  *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from django.conf.urls import url
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

app_name="doctrainingapp"


urlpatterns = [

    path('', index, name='index'),
    path('login/',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user=True),name='login'),#,redirect_authenticated_user=True
    path('logout/',sair,name='logout'),

    path('doctraining/',login_required(doctraining),name='doctraining'),

    path('user/novo/',login_required(views_user.UserCreate.as_view()),name='user_create'),
    path('user/perfil/editar/<int:pk>/',login_required(views_user.PerfilUpdate.as_view()),name='perfil_update'),
    path('user/<int:pk>/',login_required(views_user.UserUpdate.as_view()),name='user_update'),
    path('usuarios/',login_required(usuarios),name='usuarios'),
    path('user/ativar/<int:pk>/',login_required(usuario_ativar),name='user_ativar'),
    path('user/desativar/<int:pk>/',login_required(usuario_desativar),name='user_desativar'),




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
    #path('salas/todas/',login_required(todas_salas),name='todas_salas'),
    path('salas/nova/<int:area_pk>',sala_add,name='nova_sala'),
    path('salas/editar/<int:pk>/',login_required(Editar_Sala.as_view()),name='editar_sala'),
    path('salas/deletar/<int:pk>/',login_required(Deletar_Sala.as_view()),name='delete_sala'),

    # FASES
    path('fases/todas/', login_required(views_fases.todas_fases), name='todas_fases'),
    path('fases/nova/<int:area_pk>', views_fases.fase_add, name='nova_fase'),
    path('fases/editar/<int:pk>/', login_required(views_fases.Editar_Fase.as_view()), name='editar_fase'),
    path('fases/deletar/<int:pk>/', login_required(views_fases.Deletar_Fase.as_view()), name='delete_fase'),

    # PERGUNTAS FASES
    path('fases/<int:pk_fase>/perguntas/nova/',login_required(views_fases.nova_pergunta),name='nova_perguntafase'),
    path('fases/<int:pk_fase>/perguntas/',login_required(views_fases.todas_perguntas),name='todas_perguntasfase'),
    path('fases/editar/perguntas/<int:pk>/',login_required(views_fases.Editar_PerguntaFase.as_view()),name='editar_perguntafase'),
    path('fases/perguntas/deletar/<int:pk>/',login_required(views_fases.Deletar_PerguntaFase.as_view()),name='delete_perguntafase'),


    # PERGUNTAS
    path('salas/<int:pk_sala>/perguntas/nova/',login_required(nova_pergunta),name='nova_pergunta'),
    path('salas/<int:pk_sala>/perguntas/',login_required(todas_perguntas),name='todas_perguntas'),
    path('salas/editar/perguntas/<int:pk>/',login_required(Editar_Pergunta.as_view()),name='editar_pergunta'),
    path('salas/perguntas/deletar/<int:pk>/',login_required(Deletar_Pergunta.as_view()),name='delete_pergunta'),




    #WEB SERVICE
    path('api/',login_required(views_api.api),name='api'),
    path('api/casos_clinicos/nome_doencas/', views_api.nome_doencas_casos_clinicos_api,name='nome_doencas_casos_clinicos_api'),
    path('api/casos_clinicos/nome_sintomas/', views_api.nome_sintomas_casos_clinicos_api,name='nome_sintomas_casos_clinicos_api'),
    path('api/casos_clinicos/todos/', views_api.todos_casos_clinicos_doencas_sintomas_api,name='todos_casos_clinicos_doencas_sintomas_api'),
    path('api/casos_clinicos/um/', views_api.um_caso_clinico_doenca_sintomas_api,name='um_caso_clinico_doenca_sintomas_api'),
    path('api/salas/<int:pk_sala>/perguntas/', views_api.perguntas_de_uma_sala_api,name='perguntas_de_uma_sala_api'),
    path('api/salas/', views_api.todos_salas_api,name='todos_salas_api'),
    path('api/area/salas/', views_api.areas_salas_api,name='areas_salas_api'),
    path('api/areasfases/', views_api.areasFase,name='areasfases'),
    path('api/fases/<int:pk_area>', views_api.fases_api, name='fases_api'),
    url(r"^api/versao/(?P<versao_versao>\d+\.\d+)$", views_api.versao_api, name='versao-api'),
    # url(r"^item/value/(?P<dollar>\d+\.\d+)$", views.show_item, name="show-item"),
    path('api/conteudo/todos/', views_api.conteudos_api, name='conteudos_api'),


    #APRENDIZADO DE MÁQUINA controle das threads
    path('ativar_am/', login_required(views_ia.ativar_am), name='ativar_am'),
    # path('desativar_am/', login_required(desativar_am), name='desativar_am'),
    path('status_am/', login_required(views_ia.status_am), name='status_am'),
    path('am_agora/', login_required(views_ia.am_agora), name='am_agora'),

    #BACKUP E RESTAURAR BACKUP
    #path('ler_dados_salvar/',login_required(views_backup.ler_dados_salvar)),#Caso o backup sejá restaurado é interessante apagar todos os dados da tabela caso clinico,doenca e sintomas pois serão novamente salvos e pode haver duplicação de caso clinico
    #path('ler_dados_salvar/',views_backup.ler_dados_salvar),#Caso o backup sejá restaurado é interessante apagar todos os dados da tabela caso clinico,doenca e sintomas pois serão novamente salvos e pode haver duplicação de caso clinico
    #path('gerar_csv/',login_required(views_backup.gerar_csv)),

    #VERSIONAMENTO
    path('versao', views_versao.versao_list, name='lista-versao'),
    #path('versao/<int:pk>', versao_view, name='view-versao'),
    path('versao/add', views_versao.versao_add, name='add-versao'),
    path('versao/edit/<int:pk>', views_versao.versao_edit, name='edit-versao'),
    path('versao/delete/<int:pk>', views_versao.versao_delete, name='delete-versao'),
    #path('versao/delete/<int:pk>', versao_delete, name='delete-versao'),


    #AREAS
    path('areas/', views_area.area_list, name='areas_list'),
    path('areas/fases/<int:pk_area>', views_fases.todas_fases, name='area_fases'),
    path('areas/salas/<int:pk_area>', todas_salas, name='area_salas'),
    path('area/add', views_area.area_add, name='area_add'),
    path('area/edit/<int:pk>', views_area.area_edit, name='area_edit'),
    path('area/delete/<int:pk>', views_area.area_delete, name='area_delete'),

    #AREAFASES
    path('areafase/', views_areafase.area_list, name='areas_fase_list'),
    path('areafase/add', views_areafase.area_add, name='area_fase_add'),
    path('areafase/edit/<int:pk>', views_areafase.area_edit, name='area_fase_edit'),
    path('areafase/delete/<int:pk>', views_areafase.area_delete, name='area_fase_delete'),


    #CONTEUDO
    path('conteudos/', views_conteudo.conteudo_list, name='list-conteudo'),
    path('conteudo/add', views_conteudo.conteudo_add, name='add-conteudo'),
    path('conteudo/edit/<int:pk>', views_conteudo.conteudo_edit, name='edit-conteudo'),
    path('conteudo/view/<int:pk>', views_conteudo.conteudo_view, name='view-conteudo'),
    path('conteudo/delete/<int:pk>', views_conteudo.conteudo_delete, name='delete-conteudo'),


    #UPLOADS
    path('upload-area/', views_upload.area_upload, name="area_upload"),
    path('upload-areafase/', views_upload.areafase_upload, name="areafase_upload"),
    path('upload-sala/', views_upload.sala_upload, name="sala_upload"),
    path('upload-fase/', views_upload.fase_upload, name="fase_upload"),
    path('upload-pergunta-sala/', views_upload.pergunta_sala_upload, name="pergunta_sala_upload"),
    path('upload-pergunta-fase/', views_upload.pergunta_fase_upload, name="pergunta_fase_upload"),
    path('upload', views_upload.upload, name='upload'),

    path('data_firebase/', views_firebase.data_firebase, name='data_firebase')





]















#
