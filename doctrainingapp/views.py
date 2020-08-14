from doctraining import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from django.views.generic.edit import DeleteView,CreateView,UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
import random
import pandas as pd
import numpy as np
from doctrainingapp.views_pack import views_ia
#DECORATORS
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls import reverse
from .forms import *
from django.core.mail import send_mail #Para mandar email

import requests
# from django.conf import settings
from decouple import config
# from django.core.urlresolvers import resolve

# import pyrebase

#scikit-learn==0.21.3

# Create your views here.
# DEBUG=10
# INFO=20
SUCCESS=25
WARNING=30
ERROR=40


redirecionar_sem_permissao = '/doctraining/'


def index(request):
    usuario = request.user#usuario logado
    return render(request,'index.html',{'usuario':usuario,'link':config('LINK')})

def doctraining(request):
    usuario = request.user#usuario logado
    try:
        print( views_ia.tentar_ativar_am() )
    except Exception as e:
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        return redirect('/')
    return render(request,'doctraining.html',{'usuario':usuario})

def usuarios(request):
    usuario = request.user#usuario logado
    if not usuario.is_staff:#Se não for administrador
        messages.add_message(request, ERROR, 'Você não tem Permissão para acessar esta página.')#mensagem para o usuario
        return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg
    try:
        users = User.objects.all().order_by("username")
        return render(request,'usuarios.html',{'usuarios':users})
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        return redirect('/')

def usuario_ativar(request,pk):
    usuario = request.user#usuario logado
    if not usuario.is_staff:#Se não for administrador
        messages.add_message(request, ERROR, 'Você não tem Permissão para acessar esta página.')#mensagem para o usuario
        return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg
    try:
        user = User.objects.get(pk=pk)
        user.is_active = True
        user.save()
        messages.add_message(request, SUCCESS, 'Usuário '+user.username+' Ativado com Sucesso.')#mensagem para o usuario
        return redirect('/usuarios/')
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        return redirect('/usuarios/')

def usuario_desativar(request,pk):
    usuario = request.user#usuario logado
    if not usuario.is_staff:#Se não for administrador
        messages.add_message(request, ERROR, 'Você não tem Permissão para acessar esta página.')#mensagem para o usuario
        return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg
    try:
        user = User.objects.get(pk=pk)
        if user.is_superuser:
            messages.add_message(request, ERROR, 'Você não tem Permissão para desativar um Super Usuário.')#mensagem para o usuario
            return redirect('/usuarios/')
        user.is_active = False
        user.save()
        messages.add_message(request, SUCCESS, 'O Usuário '+user.username+' foi Desativado.')#mensagem para o usuario
        return redirect('/usuarios/')
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        return redirect('/usuarios/')

def sair(request):
    usuario = request.user#usuario logado
    #codigo para se deslogar
    request.session.items = []
    request.session.modified = True
    logout(request)
    return redirect('/')#voltar para tela inicial

#Todos os casos clinicos
def casos_clinicos(request):
    usuario = request.user#usuario logado
    try:
        casos_clinicos = Caso_Clinico.objects.filter().order_by('doenca__nome_doenca')#todos os casos clinicos
        return render(request,'casos_clinicos.html',{'casos_clinicos':casos_clinicos,'usuario':usuario})
    except Exception as e:
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
        return redirect('/doctraining/')

def doenca(request, pk):#editar nome doenca
    usuario = request.user#usuario logado
    ver_remover = True
    doencas_todas = Doenca.objects.all().order_by('nome_doenca')
    if  request.method == "POST":#se tiver sido eviado os dados no formulario
        doenca = Doenca.objects.get(pk=pk)
        nome_doenca =  request.POST.get("nome_doenca")
        solicitacao_alterar_doenca = Solicitacao_Alterar_Caso_Clinico()#novo objeto
        solicitacao_alterar_doenca.nome_doenca_a_modificar = doenca
        try:
            Doenca.objects.get(nome_doenca=nome_doenca)
            messages.add_message(request, ERROR, 'Nome da doença já existe.')#mensagem para o usuario
            nome_doenca = doenca.nome_doenca
            return render(request,'doenca.html',{'ver_remover':ver_remover,'nome_doenca':nome_doenca,'doenca':doenca,'usuario':usuario,'doencas_todas':doencas_todas})
        except Exception as e:
            pass
        if len(nome_doenca) <= 2:# se nome digitado for curto
            messages.add_message(request, ERROR, 'Nome da doença é muito curto.')#mensagem para o usuario
            nome_doenca =  doenca.nome_doenca
            return render(request,'doenca.html',{'ver_remover':ver_remover,'nome_doenca':nome_doenca,'doenca':doenca,'usuario':usuario,'doencas_todas':doencas_todas})
        solicitacao_alterar_doenca.nome_nova_doenca_modificada = nome_doenca
        solicitacao_alterar_doenca.solicitante = usuario
        solicitacao_alterar_doenca.tipo_alteracao = 2#0-DELETE; 1-CREATE; ou (2)-UPDATE
        solicitacao_alterar_doenca.acao = 2#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
        solicitacao_alterar_doenca.save()
        messages.add_message(request, SUCCESS, 'Foi cadastrada uma solicitação para editar nome de doença.')#mensagem para o usuario
        return redirect('/doenca/nova/')
    else:
        try:
            doenca = Doenca.objects.get(pk=pk)
            nome_doenca =  doenca.nome_doenca
            return render(request,'doenca.html',{'ver_remover':ver_remover,'nome_doenca':nome_doenca,'doenca':doenca,'usuario':usuario,'doencas_todas':doencas_todas})
        except Exception as e:
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
            return redirect('/doctraining/')


def solicitar_deletar_doenca(request, pk):
    usuario = request.user#usuario logado
    try:
        doenca = Doenca.objects.get(pk=pk)
        solicitacao_alterar_doenca = Solicitacao_Alterar_Caso_Clinico()#novo objeto
        solicitacao_alterar_doenca.nome_doenca_a_modificar = doenca
        solicitacao_alterar_doenca.solicitante = usuario
        solicitacao_alterar_doenca.tipo_alteracao = 0#0-DELETE; 1-CREATE; ou (2)-UPDATE
        solicitacao_alterar_doenca.acao = 2#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
        solicitacao_alterar_doenca.save()
        messages.add_message(request, SUCCESS, 'Foi cadastrada uma solicitação para deletar doença.')#mensagem para o usuario
        return redirect('/doenca/nova/')
    except Exception as e:
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
        return redirect('/doctraining/')


def solicitar_nova_doenca(request):
    usuario = request.user#usuario logado
    ver_remover = False
    nome_doenca =  ""
    doencas_todas = Doenca.objects.all().order_by('nome_doenca')
    if  request.method == "POST":#se tiver sido eviado os dados no formulario
        solicitacao_alterar_doenca = Solicitacao_Alterar_Caso_Clinico()#novo objeto
        nome_doenca = request.POST.get("nome_doenca")
        try:
            Doenca.objects.get(nome_doenca=nome_doenca)
            messages.add_message(request, ERROR, 'Nome da doença já existe.')#mensagem para o usuario
            nome_doenca =  ''
            return render(request,'doenca.html',{'ver_remover':ver_remover,'nome_doenca':nome_doenca,'doenca':doenca,'usuario':usuario,'doencas_todas':doencas_todas})
        except Exception as e:
            pass
        if len(nome_doenca) <= 2:# se nome digitado for curto
            messages.add_message(request, ERROR, 'Nome da doença é muito curto.')#mensagem para o usuario
            nome_doenca = ''
            return render(request,'doenca.html',{'ver_remover':ver_remover,'nome_doenca':nome_doenca,'doenca':doenca,'usuario':usuario,'doencas_todas':doencas_todas})
        solicitacao_alterar_doenca.nome_nova_doenca_modificada = nome_doenca
        solicitacao_alterar_doenca.solicitante = usuario
        solicitacao_alterar_doenca.tipo_alteracao = 1#0-DELETE; 1-CREATE; ou (2)-UPDATE
        solicitacao_alterar_doenca.acao = 2#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
        solicitacao_alterar_doenca.save()
        messages.add_message(request, SUCCESS, 'Foi cadastrada uma solicitação para novo nome de doença.')#mensagem para o usuario
        return redirect('/doenca/nova/')
    else:
        try:
            return render(request,'doenca.html',{'ver_remover':ver_remover,'nome_doenca':nome_doenca,'doenca':doenca,'usuario':usuario,'doencas_todas':doencas_todas})
        except Exception as e:
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
            return redirect('/doctraining/')






##### sintomas
def sintoma(request, pk):#editar
    usuario = request.user#usuario logado
    sintomas_todos = Sintoma.objects.all().order_by('nome_sintoma')
    ver_remover = True
    if  request.method == "POST":#se tiver sido eviado os dados no formulario
        sintoma = Sintoma.objects.get(pk=pk)
        nome_sintoma = request.POST.get("nome_sintoma")
        solicitacao_alterar_sintoma = Solicitacao_Alterar_Caso_Clinico()#novo objeto
        solicitacao_alterar_sintoma.nome_sintoma_a_modificar = sintoma
        try:
            Sintoma.objects.get(nome_sintoma=nome_sintoma)
            messages.add_message(request, ERROR, 'Nome da doença já existe.')#mensagem para o usuario
            nome_sintoma =  sintoma.nome_sintoma
            return render(request,'sintoma.html',{'nome_sintoma':nome_sintoma,'sintoma':sintoma,'usuario':usuario,'sintomas_todos':sintomas_todos})
        except Exception as e:
            pass
            #Trata o erro pq não existe doenca com esse nome e continua
        if len(nome_sintoma) <= 2:# se nome digitado for curto
            messages.add_message(request, ERROR, 'Nome da doença é muito curto.')#mensagem para o usuario
            nome_sintoma =  sintoma.nome_sintoma
            return render(request,'sintoma.html',{'nome_sintoma':nome_sintoma,'sintoma':sintoma,'usuario':usuario,'sintomas_todos':sintomas_todos})
        solicitacao_alterar_sintoma.nome_novo_sintoma_modificado = nome_sintoma
        solicitacao_alterar_sintoma.solicitante = usuario
        solicitacao_alterar_sintoma.tipo_alteracao = 2#0-DELETE; 1-CREATE; ou (2)-UPDATE
        solicitacao_alterar_sintoma.acao = 2#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
        solicitacao_alterar_sintoma.save()
        messages.add_message(request, SUCCESS, 'Foi cadastrada uma solicitação para editar nome de sintoma.')#mensagem para o usuario
        return redirect('/casos_clinicos/')
    else:
        try:
            sintoma = Sintoma.objects.get(pk=pk)
            nome_sintoma =  sintoma.nome_sintoma
            return render(request,'sintoma.html',{'ver_remover':ver_remover,'nome_sintoma':nome_sintoma,'sintoma':sintoma,'usuario':usuario,'sintomas_todos':sintomas_todos})
        except Exception as e:
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
            return redirect('/sintoma/novo/')


def solicitar_deletar_sintoma(request, pk):
    usuario = request.user#usuario logado
    try:
        sintoma = Sintoma.objects.get(pk=pk)
        solicitacao_alterar_sintoma = Solicitacao_Alterar_Caso_Clinico()#novo objeto
        solicitacao_alterar_sintoma.nome_sintoma_a_modificar = sintoma
        solicitacao_alterar_sintoma.solicitante = usuario
        solicitacao_alterar_sintoma.tipo_alteracao = 0#0-DELETE; 1-CREATE; ou (2)-UPDATE
        solicitacao_alterar_sintoma.acao = 2#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
        solicitacao_alterar_sintoma.save()
        messages.add_message(request, SUCCESS, 'Foi cadastrada uma solicitação para deletar sintoma.')#mensagem para o usuario
        return redirect('/sintoma/novo/')
    except Exception as e:
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
        return redirect('/doctraining/')


def solicitar_novo_sintoma(request):
    usuario = request.user#usuario logado
    sintomas_todos = Sintoma.objects.all().order_by('nome_sintoma')
    ver_remover = False#Falso indica que essa pagina é de novo sintoma e assim não há como remover sem saber o que
    if  request.method == "POST":#se tiver sido eviado os dados no formulario
        solicitacao_alterar_sintoma = Solicitacao_Alterar_Caso_Clinico()#novo objeto
        nome_sintoma = request.POST.get("nome_sintoma")
        try:
            Sintoma.objects.get(nome_sintoma=nome_sintoma)
            messages.add_message(request, ERROR, 'Nome do sintoma já existe.')#mensagem para o usuario
            nome_sintoma =  ''
            return render(request,'sintoma.html',{'nome_sintoma':nome_sintoma,'sintoma':sintoma,'usuario':usuario,'sintomas_todos':sintomas_todos})
        except Exception as e:
            pass
            #Trata o erro pq não existe doenca com esse nome e continua
        if len(nome_sintoma) <= 2:# se nome digitado for curto
            messages.add_message(request, ERROR, 'Nome do sintoma é muito curto.')#mensagem para o usuario
            nome_sintoma =  ""
            dados={'ver_remover':ver_remover, 'nome_sintoma':nome_sintoma, 'sintoma':sintoma,'usuario':usuario,'sintomas_todos':sintomas_todos}
            return render(request,'sintoma.html',dados)
        solicitacao_alterar_sintoma.nome_novo_sintoma_modificado = nome_sintoma
        solicitacao_alterar_sintoma.solicitante = usuario
        solicitacao_alterar_sintoma.tipo_alteracao = 1#0-DELETE; 1-CREATE; ou (2)-UPDATE
        solicitacao_alterar_sintoma.acao = 2#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
        solicitacao_alterar_sintoma.save()
        messages.add_message(request, SUCCESS, 'Foi cadastrada uma solicitação para novo nome de sintoma.')#mensagem para o usuario
        return redirect('/sintoma/novo/')
    else:
        try:
            nome_sintoma =  ""
            dados={'ver_remover':ver_remover,'nome_sintoma':nome_sintoma,'sintoma':sintoma,'usuario':usuario,'sintomas_todos':sintomas_todos}
            return render(request,'sintoma.html',dados)
        except Exception as e:
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
            return redirect('/doctraining/')


#Solicitar edicão de caso clinico
def solicitar_editar_caso_clinico(request,pk):
    usuario = request.user
    if  request.method == "POST":#se tiver sido eviado os dados no formulario
        try:#tente
            lista_sintomas_novo = []#lista com novos sintomas
            for sintoma in Sintoma.objects.all():#todos os sintomas
                valor_on_off = request.POST.get(sintoma.nome_sintoma)#pegar valor da caisa de seleção no formulario (on ou off)
                #se o sintoma tiver sido selecionado (on)
                if valor_on_off == 'on':
                    print(sintoma)
                    item = Sintoma.objects.get(nome_sintoma=sintoma)#pegar o sintoma selecionado no formulario
                    lista_sintomas_novo.append(item.pk)#adiciona o id do sintoma selecionado no formulario a uma lista

            #se não tiver informado sintomas no formulario mostrar mensagem de erro
            if len(lista_sintomas_novo) == 0:
                messages.add_message(request, ERROR, 'Você precisa selecionar pelo menos um sintoma.')
                return redirect('/casos_clinicos/solicitar/editar/'+str(pk))
            #tente pegar pk da doenca selecionada
            try:
                nova_doenca = Doenca.objects.get(pk = int(request.POST.get('doenca')))#pegar doenca selecionada no formulario
                doenca_classificada = True #variavel indica que a doenca foi classificada na hora de salvar
            #se não conseguir não foi selecionada nenhuma doença
            except Exception as ee:
                nova_doenca = None
                doenca_classificada = False#variavel indica que a doenca foi não classificada na hora de salvar
            #Nova Solcicitação de alterar esse caso clinico
            caso_clinico = Caso_Clinico.objects.get(pk=pk)#Caso clinico que se deseja editar
            lista_objetos_sintomas_novo = Sintoma.objects.filter(pk__in=lista_sintomas_novo)#lista com os objetos de novos sintomas
            solicitacao_alterar_caso_clinico = Solicitacao_Alterar_Caso_Clinico()#novo objeto
            solicitacao_alterar_caso_clinico.caso_clinico_a_modificar = caso_clinico
            solicitacao_alterar_caso_clinico.nova_doenca = nova_doenca
            solicitacao_alterar_caso_clinico.tipo_alteracao = 2#0-DELETE; 1-CREATE; ou (2)-UPDATE
            solicitacao_alterar_caso_clinico.acao = 2#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            solicitacao_alterar_caso_clinico.doenca_classificada = doenca_classificada
            solicitacao_alterar_caso_clinico.solicitante = usuario
            solicitacao_alterar_caso_clinico.save()
            try:#tente adicionar sintomas
                solicitacao_alterar_caso_clinico.novos_sintomas.set(lista_objetos_sintomas_novo)#Inserirndo os sintomas após objeto salva pelo metodo get
                messages.add_message(request, SUCCESS, 'Foi cadastrada uma solicitação de edição de amostra.')#mensagem para o usuario
            except Exception as e:#se não salvar pelo menos apagar a solicitação mal formada
                solicitacao_alterar_caso_clinico.delete()
                mandar_email_error(str(e),usuario,request.resolver_match.url_name)
                messages.add_message(request, ERROR, 'Ocorreu um erro ao adicionar sintomas. Tente novamente mais tarde.')#mensagem para o usuario
            return redirect('/casos_clinicos/')
        except Exception as e:
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
            return redirect('/casos_clinicos/')
            # return HttpResponse('Erro: '+ str(e))
    else:
        try:
            # casos_clinicos = Caso_Clinico.objects.filter().order_by('doenca__nome_doenca')
            caso_clinico = Caso_Clinico.objects.get(pk=pk)#caso clinico a editar
            doencas = Doenca.objects.filter().order_by('nome_doenca')#todas as doencas
            sintomas = Sintoma.objects.filter().order_by('nome_sintoma')#todos os sintomas
            lista_sintomas = []#lista de sintiomas desse caso clinico
            lista_sintomas = set(valor.pk for valor in caso_clinico.sintomas.all())#adicinar sintiomas desse caso clinico a lista
            # self.child.instance = self.instance.get(id=item['id']) # Blog.objects.filter(pk__in=[1, 4, 7])
            return render(request,'solicitar_editar_caso_clinico.html',{'caso_clinico':caso_clinico,'doencas':doencas,'sintomas':sintomas,'lista_sintomas':lista_sintomas, 'usuario':usuario})
        except Exception as e:
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
            return redirect('/casos_clinicos/')

#Solicitar deletar um caso clinico
def solicitar_deletar_caso_clinico(request,pk):
    usuario = request.user
    try:
        #Nova Solicitação de exclusão de caso clinico
        caso_clinico = Caso_Clinico.objects.get(pk=pk)#Caso clinico que se deseja excluir
        solicitacao_alterar_caso_clinico = Solicitacao_Alterar_Caso_Clinico()
        solicitacao_alterar_caso_clinico.caso_clinico_a_modificar = caso_clinico
        solicitacao_alterar_caso_clinico.nova_doenca = caso_clinico.doenca
        solicitacao_alterar_caso_clinico.tipo_alteracao = 0#0-DELETE; 1-CREATE; ou (2)-UPDATE
        solicitacao_alterar_caso_clinico.acao = 2#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
        solicitacao_alterar_caso_clinico.doenca_classificada = caso_clinico.doenca_classificada
        solicitacao_alterar_caso_clinico.solicitante = usuario
        solicitacao_alterar_caso_clinico.save()
        try:#tente adicionar sintomas
            solicitacao_alterar_caso_clinico.novos_sintomas.set(caso_clinico.sintomas.all())
            messages.add_message(request, SUCCESS, 'Foi cadastrada uma solicitação de exclusão de amostra.')#mensagem para o usuario
        except Exception as e:#se não salvar pelo menos apagar a solicitação mal formada
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            messages.add_message(request, ERROR, 'Ocorreu um erro ao adicionar sintomas da exclusão. Tente novamente mais tarde.')#mensagem para o usuario
            solicitacao_alterar_caso_clinico.delete()
        return redirect('/casos_clinicos/')
        # a4.publications.set([p3])
        # return HttpResponse(str(lista_sintomas_novo))
    except Exception as e:
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
        return redirect('/casos_clinicos/')

#Solicitar cadastrar caso clinico
def solicitar_novo_caso_clinico(request):
    usuario = request.user
    if  request.method == "POST":#se tiver sido eviado os dados no formulario
        try:#tente
            lista_sintomas_novo = []#lista com novos sintomas
            for sintoma in Sintoma.objects.all():#Laço para adicomar id's dos sintomas a lista
                valor_on_off = request.POST.get(sintoma.nome_sintoma)#pegar valor da caixa de seleção no formulario (on ou off) pelo id
                #se o sintoma tiver sido selecionado (on)
                if valor_on_off == 'on':
                    print(sintoma)
                    item = Sintoma.objects.get(nome_sintoma=sintoma)#pegar o sintoma selecionado no formulario
                    lista_sintomas_novo.append(item.pk)#adiciona o id do sintoma selecionado no formulario a uma lista
            #se não tiver informado sintomas mostrar msg
            if len(lista_sintomas_novo) == 0:
                messages.add_message(request, ERROR, 'Você precisa selecionar pelo menos um sintoma.')
                return redirect('/casos_clinicos/solicitar/novo/')
                # return HttpResponse('Erro: Você precisa selecionar pelo menos um sintoma')
            #tente pegar pk da doenca selecionada
            try:
                nova_doenca = Doenca.objects.get(pk = int(request.POST.get('doenca')))#pegar doenca selecionada no formulario
                doenca_classificada = True #variavel indica que a doenca foi pelo usuario no formulario na hora de salvar
            except Exception as ee:
                nova_doenca = None
                doenca_classificada = False#variavel indica que a doenca NÃO foi pelo usuario no formulario na hora de salvar
            #Nova Solcicitação de cadastro de caso clinico
            lista_objetos_sintomas_novo = Sintoma.objects.filter(pk__in=lista_sintomas_novo)#lista com os objetos de novos sintomas
            solicitacao_alterar_caso_clinico = Solicitacao_Alterar_Caso_Clinico()#novo objeto
            solicitacao_alterar_caso_clinico.caso_clinico_a_modificar = None
            solicitacao_alterar_caso_clinico.nova_doenca = nova_doenca
            solicitacao_alterar_caso_clinico.tipo_alteracao = 1#0-DELETE; 1-CREATE; ou (2)-UPDATE
            solicitacao_alterar_caso_clinico.acao = 2#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            solicitacao_alterar_caso_clinico.doenca_classificada = doenca_classificada
            solicitacao_alterar_caso_clinico.solicitante = usuario
            solicitacao_alterar_caso_clinico.save()
            try:#tente adicionar sintomas
                solicitacao_alterar_caso_clinico.novos_sintomas.set(lista_objetos_sintomas_novo)#Inserirndo os sintomas após objeto salva pelo metodo get
                messages.add_message(request, SUCCESS, 'Foi cadastrada uma solicitação de nova de amostra.')
            except Exception as e:#se não salvar pelo menos apagar a solicitação mal formada
                solicitacao_alterar_caso_clinico.delete()
                mandar_email_error(str(e),usuario,request.resolver_match.url_name)
                messages.add_message(request, ERROR, 'Ocorreu um erro ao adicionar sintomas. Tente novamente mais tarde.')
            return redirect('/casos_clinicos/')
            # a4.publications.set([p3])
            # return HttpResponse(str(lista_sintomas_novo))
        except Exception as e:
            messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return redirect('/casos_clinicos/')
    else:
        try:
            doencas = Doenca.objects.filter().order_by('nome_doenca')#todas as doencas
            sintomas = Sintoma.objects.filter().order_by('nome_sintoma')#todos os sintomas
            return render(request,'solicitar_novo_caso_clinico.html',{'doencas':doencas,'sintomas':sintomas, 'usuario':usuario})
        except Exception as e:
            messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return redirect('/casos_clinicos/')
            # return HttpResponse('Erro: '+ str(e))


#Ver todas as solicitações de alterar caso clinico
def solicitacoes_alteracao_casos_clinicos(request):
    # if not request.user.is_staff:#Se não for administrador
    #     messages.add_message(request, ERROR, 'Você não tem Permissão para acessar esta página.')#mensagem para o usuario
    #     return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg

    usuario = request.user
    try:
        #todas as solicitações ordenadas pel data
        if not usuario.is_staff:#Se não for administrador
            solicitacao_alterar_caso_clinico = Solicitacao_Alterar_Caso_Clinico.objects.filter(solicitante = usuario).order_by('data_solicitacao')
        else:#se for adm
            solicitacao_alterar_caso_clinico = Solicitacao_Alterar_Caso_Clinico.objects.filter().order_by('data_solicitacao')
        return render(request,'solicitacao_alterar_caso_clinico.html',{'solicitacao_alterar_caso_clinico':solicitacao_alterar_caso_clinico,'usuario':usuario})
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        return redirect('/casos_clinicos/solicitacoes/')

#Aceitar uma solicitação de alteração de caso clinico (Novo, Editar ou Deletar)
def aceitar_solicitacao_alteracao_caso_clinico(request,pk):
    if not request.user.is_staff:#Se não for administrador
        messages.add_message(request, ERROR, 'Você não tem Permissão para acessar esta página.')#mensagem para o usuario
        return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg
    usuario = request.user#usuario logado, se tiver
    try:
        #Solicitação de alteração em casos clinicos
        solicitacao_alterar_caso_clinico = Solicitacao_Alterar_Caso_Clinico.objects.get(pk=pk)
        #se Deletar
        if solicitacao_alterar_caso_clinico.tipo_alteracao == 0:#Deletar
            # if self.nome_sintoma_a_modificar or self.nome_novo_sintoma_modificado or self.nome_doenca_a_modificar or self.nome_nova_doenca_modificada:
            item_deletar_caso_clinico_doenca_ou_sintoma = None
            if solicitacao_alterar_caso_clinico.nome_doenca_a_modificar:#Se for para deletar uma doença
                editar_casos_clinicos = Caso_Clinico.objects.filter(doenca = solicitacao_alterar_caso_clinico.nome_doenca_a_modificar)#pegando casos clinicos relacionados com aquela doença
                for editar_caso_clinico in editar_casos_clinicos:#retirando a doença relacionada aqueles casos clinos e colocando como sem classificação.
                    editar_caso_clinico.doenca = None
                    editar_caso_clinico.doenca_classificada = False
                    editar_caso_clinico.save()
                item_deletar_caso_clinico_doenca_ou_sintoma = Doenca.objects.get(pk=solicitacao_alterar_caso_clinico.nome_doenca_a_modificar.pk )
                solicitacao_alterar_caso_clinico.acao =1#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            elif solicitacao_alterar_caso_clinico.nome_sintoma_a_modificar:#Se for para deletar um sintoma
                item_deletar_caso_clinico_doenca_ou_sintoma = Sintoma.objects.get(pk=solicitacao_alterar_caso_clinico.nome_sintoma_a_modificar.pk )
                solicitacao_alterar_caso_clinico.acao =1#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            else:#Se for para deletar um caso clinico
                item_deletar_caso_clinico_doenca_ou_sintoma = Caso_Clinico.objects.get(pk = solicitacao_alterar_caso_clinico.caso_clinico_a_modificar.pk)#pegando caso clinico relacionado
                solicitacao_alterar_caso_clinico.acao =1#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE

            #Inicio ----------------------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
            log = Log()#cria objeto de log, linhas a seguir são de adicionar os dados
            log.data_solicitacao = solicitacao_alterar_caso_clinico.data_solicitacao#data e hora
            log.solicitante = solicitacao_alterar_caso_clinico.solicitante #user
            # log.id_user = solicitacao_alterar_caso_clinico.solicitante.pk#id para busca enquanto existir user que solicitou
            #Antigos
            log.doenca = solicitacao_alterar_caso_clinico.nome_doenca_antigo_DEF()#string
            log.sintomas = solicitacao_alterar_caso_clinico.sintomas_antigo_DEF()#string
            #Novos
            log.nova_doenca = solicitacao_alterar_caso_clinico.nome_doenca_novo_DEF()#string
            log.novos_sintomas = solicitacao_alterar_caso_clinico.sintomas_novos_DEF()#string

            log.doenca_classificada = solicitacao_alterar_caso_clinico.doenca_classificada#boolena
            log.tipo_alteracao = solicitacao_alterar_caso_clinico.tipo_alteracao#inteiro -> 0-DELETE; 1-CREATE; ou (2)-UPDATE
            log.aux_tipo_alteracao = solicitacao_alterar_caso_clinico.tipo_alteracao_DEF()
            log.acao = solicitacao_alterar_caso_clinico.acao#inteiro -> 0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            log.avaliador = usuario#user
            # log.avaliado_por = usuario.username#string
            #Fim----------------------------------Salvar aqui na tabela de log  ------------------------------------------------
            # solicitacao_alterar_caso_clinico.salvar_log(usuario=usuario)

            #Inicio --------------Executar-------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
            log.save()
            #Fim-------------------Executar-------------------Salvar aqui na tabela de log ----------------------------------------------------------

            solicitacao_alterar_caso_clinico.delete()#deletando solicitação, pois seus dados já se encontram na tabela de log
            item_deletar_caso_clinico_doenca_ou_sintoma.delete()#deletando caso clinico, pois pois pedido foi aceito (execultando pedido)
        # se Novo
        elif solicitacao_alterar_caso_clinico.tipo_alteracao == 1:#Novo
            # if self.nome_sintoma_a_modificar or self.nome_novo_sintoma_modificado or self.nome_doenca_a_modificar or self.nome_nova_doenca_modificada:
            if solicitacao_alterar_caso_clinico.nome_nova_doenca_modificada:#Se for para adicionar uma doença
                if not (Doenca.objects.filter(nome_doenca=solicitacao_alterar_caso_clinico.nome_nova_doenca_modificada )):#se já existir uma doença com esse nome
                    doenca = Doenca()
                    doenca.nome_doenca = solicitacao_alterar_caso_clinico.nome_nova_doenca_modificada
                    doenca.save()
                    solicitacao_alterar_caso_clinico.acao =1#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
                else:
                    return HttpResponse("Já existe uma doença com esse nome")
            elif solicitacao_alterar_caso_clinico.nome_novo_sintoma_modificado:#Se for para deletar um sintoma
                if not (Sintoma.objects.filter(nome_sintoma=solicitacao_alterar_caso_clinico.nome_novo_sintoma_modificado )):#se já existir uma sintoma com esse nome
                    sintoma = Sintoma()
                    sintoma.nome_sintoma = solicitacao_alterar_caso_clinico.nome_novo_sintoma_modificado
                    sintoma.save()
                    solicitacao_alterar_caso_clinico.acao =1#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
                else:
                    return HttpResponse("Já existe um sintoma com esse nome")
            else:#Se for para deletar um caso clinico
                solicitacao_alterar_caso_clinico.acao =1#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
                caso_clinico = Caso_Clinico()#Novo objeto de caso clinico
                caso_clinico.doenca = solicitacao_alterar_caso_clinico.nova_doenca#adicinando doenca
                caso_clinico.doenca_classificada = solicitacao_alterar_caso_clinico.doenca_classificada#adicionando se doença é classificada ou não
                caso_clinico.save()#salvando o caso clinico
                caso_clinico.sintomas.set(solicitacao_alterar_caso_clinico.novos_sintomas.all())#Adicionando os sintomas após objeto ser salvo pelo metodo get()

            #Inicio ----------------------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
            log = Log()#cria objeto de log, linhas a seguir são de adicionar os dados
            log.data_solicitacao = solicitacao_alterar_caso_clinico.data_solicitacao#data e hora
            log.solicitante = solicitacao_alterar_caso_clinico.solicitante#user
            # log.id_user = solicitacao_alterar_caso_clinico.solicitante.pk#id para busca enquanto existir user que solicitou
            #Antigos
            log.doenca = solicitacao_alterar_caso_clinico.nome_doenca_antigo_DEF()#string
            log.sintomas = solicitacao_alterar_caso_clinico.sintomas_antigo_DEF()#string
            #Novos
            log.nova_doenca = solicitacao_alterar_caso_clinico.nome_doenca_novo_DEF()#string
            log.novos_sintomas = solicitacao_alterar_caso_clinico.sintomas_novos_DEF()#string

            log.doenca_classificada = solicitacao_alterar_caso_clinico.doenca_classificada#boolena
            log.tipo_alteracao = solicitacao_alterar_caso_clinico.tipo_alteracao#inteiro -> 0-DELETE; 1-CREATE; ou (2)-UPDATE
            log.aux_tipo_alteracao = solicitacao_alterar_caso_clinico.tipo_alteracao_DEF()
            log.acao = solicitacao_alterar_caso_clinico.acao#inteiro -> 0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            log.avaliador = usuario#user
            #Fim----------------------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
            # solicitacao_alterar_caso_clinico.salvar_log(usuario=usuario)

            #Inicio --------------Executar-------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
            log.save()
            #Fim-------------------Executar-------------------Salvar aqui na tabela de log ----------------------------------------------------------

            solicitacao_alterar_caso_clinico.delete()#deletando solicitação, pois seus dados já se encontram na tabela de log
        #se Editar
        else:#Editar
            # if self.nome_sintoma_a_modificar or self.nome_novo_sintoma_modificado or self.nome_doenca_a_modificar or self.nome_nova_doenca_modificada:
            item_editar_caso_clinico_doenca_ou_sintoma = None
            #Se for para editar uma doença
            if solicitacao_alterar_caso_clinico.nome_doenca_a_modificar and solicitacao_alterar_caso_clinico.nome_nova_doenca_modificada:#Se for para deletar uma doença
                item_editar_caso_clinico_doenca_ou_sintoma = Doenca.objects.get(pk=solicitacao_alterar_caso_clinico.nome_doenca_a_modificar.pk )
            #Se for para editar um sintoma
            elif solicitacao_alterar_caso_clinico.nome_sintoma_a_modificar and solicitacao_alterar_caso_clinico.nome_novo_sintoma_modificado:
                item_editar_caso_clinico_doenca_ou_sintoma = Sintoma.objects.get(pk=solicitacao_alterar_caso_clinico.nome_sintoma_a_modificar.pk )
            #Se for para editar um caso clinico
            else:
                item_editar_caso_clinico_doenca_ou_sintoma = Caso_Clinico.objects.get(pk = solicitacao_alterar_caso_clinico.caso_clinico_a_modificar.pk)#caso clinico que será modificado

            solicitacao_alterar_caso_clinico.acao =1#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            #Não podem ser adicionados no final, pois os dados do caso clinico serão alretados, então não teremos mmais acesso aos valores antogos dele para jogar na tabela de log
            #Inicio ----------------------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
            log = Log()#cria objeto de log, linhas a seguir são de adicionar os dados
            log.data_solicitacao = solicitacao_alterar_caso_clinico.data_solicitacao#data e hora
            log.solicitante = solicitacao_alterar_caso_clinico.solicitante#user
            # log.id_user = solicitacao_alterar_caso_clinico.solicitante.pk#id para busca enquanto existir user que solicitou
            #Antigos
            log.doenca = solicitacao_alterar_caso_clinico.nome_doenca_antigo_DEF()#string
            log.sintomas = solicitacao_alterar_caso_clinico.sintomas_antigo_DEF()#string
            #Novos
            log.nova_doenca = solicitacao_alterar_caso_clinico.nome_doenca_novo_DEF()#string
            log.novos_sintomas = solicitacao_alterar_caso_clinico.sintomas_novos_DEF()#string

            log.doenca_classificada = solicitacao_alterar_caso_clinico.doenca_classificada#boolena
            log.tipo_alteracao = solicitacao_alterar_caso_clinico.tipo_alteracao#inteiro -> 0-DELETE; 1-CREATE; ou (2)-UPDATE
            log.aux_tipo_alteracao = solicitacao_alterar_caso_clinico.tipo_alteracao_DEF()
            log.acao = solicitacao_alterar_caso_clinico.acao#inteiro -> 0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            log.avaliador = usuario#user

            #Fim----------------------------------Salvar aqui na tabela de log ------------------------------------------------
            # solicitacao_alterar_caso_clinico.salvar_log(usuario=usuario)

            #Se for para deletar uma doença
            if solicitacao_alterar_caso_clinico.nome_doenca_a_modificar and solicitacao_alterar_caso_clinico.nome_nova_doenca_modificada:
                if not (Doenca.objects.filter(nome_doenca=solicitacao_alterar_caso_clinico.nome_nova_doenca_modificada )):#Se não existir doenca com esse nome
                    item_editar_caso_clinico_doenca_ou_sintoma.nome_doenca = solicitacao_alterar_caso_clinico.nome_nova_doenca_modificada
                    item_editar_caso_clinico_doenca_ou_sintoma.save()
                    solicitacao_alterar_caso_clinico.acao =1#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
                else:
                    return HttpResponse("Já existe uma doença com esse nome")
            #Se for para deletar um sintoma
            elif solicitacao_alterar_caso_clinico.nome_sintoma_a_modificar and solicitacao_alterar_caso_clinico.nome_novo_sintoma_modificado:
                if not (Sintoma.objects.filter(nome_sintoma=solicitacao_alterar_caso_clinico.nome_novo_sintoma_modificado )):#Se não existir sintoma com esse nome
                    item_editar_caso_clinico_doenca_ou_sintoma.nome_sintoma = solicitacao_alterar_caso_clinico.nome_novo_sintoma_modificado
                    item_editar_caso_clinico_doenca_ou_sintoma.save()
                    solicitacao_alterar_caso_clinico.acao =1#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
                else:
                    return HttpResponse("Já existe um sintoma com esse nome")
            #Se for para deletar um casp clinico
            else:
                #solicitacao_alterar_caso_clinico.salvar_log(usuario=usuario)
                item_editar_caso_clinico_doenca_ou_sintoma.doenca = solicitacao_alterar_caso_clinico.nova_doenca#adicinando doenca
                item_editar_caso_clinico_doenca_ou_sintoma.doenca_classificada = solicitacao_alterar_caso_clinico.doenca_classificada#adicionando se doença é classificada ou não
                item_editar_caso_clinico_doenca_ou_sintoma.save()#salvando o caso clinico
                item_editar_caso_clinico_doenca_ou_sintoma.sintomas.set(solicitacao_alterar_caso_clinico.novos_sintomas.all())#Adicionando os sintomas após objeto ser salvo pelo metodo get()

            #Inicio --------------Executar-------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
            log.save()
            #Fim-------------------Executar-------------------Salvar aqui na tabela de log ----------------------------------------------------------
            solicitacao_alterar_caso_clinico.delete()#deletando solicitação, pois seus dados já se encontram na tabela de log
        #mensagem para usuario
        print(views_ia.tentar_ativar_am() )
        messages.add_message(request, SUCCESS, 'Foi aceitada a alteração da amostra.')
        return redirect('/casos_clinicos/solicitacoes/')
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde. ')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        return redirect('/casos_clinicos/solicitacoes/')


#Rejeitar pedido de alteração de casos clinico (editar, novo ou delete)
def rejeitar_solicitacao_alteracao_caso_clinico(request,pk):
    if not request.user.is_staff:#Se não for administrador
        messages.add_message(request, ERROR, 'Você não tem Permissão para acessar esta página.')#mensagem para o usuario
        return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg

    usuario = request.user#usuario logado, se tiver
    try:
        #Solicitação de alteração em casos clinicos
        solicitacao_alterar_caso_clinico = Solicitacao_Alterar_Caso_Clinico.objects.get(pk=pk)
        solicitacao_alterar_caso_clinico.acao =0#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE

        #Inicio ----------------------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
        log = Log()#cria objeto de log, linhas a seguir são de adicionar os dados
        log.data_solicitacao = solicitacao_alterar_caso_clinico.data_solicitacao#data e hora
        log.solicitante = solicitacao_alterar_caso_clinico.solicitante#string
        # log.id_user = solicitacao_alterar_caso_clinico.solicitante.pk#id para busca enquanto existir user que solicitou
        #Antigos
        log.doenca = solicitacao_alterar_caso_clinico.nome_doenca_antigo_DEF()#string
        log.sintomas = solicitacao_alterar_caso_clinico.sintomas_antigo_DEF()#string
        #Novos
        log.nova_doenca = solicitacao_alterar_caso_clinico.nome_doenca_novo_DEF()#string
        log.novos_sintomas = solicitacao_alterar_caso_clinico.sintomas_novos_DEF()#string

        log.doenca_classificada = solicitacao_alterar_caso_clinico.doenca_classificada#boolena
        log.tipo_alteracao = solicitacao_alterar_caso_clinico.tipo_alteracao#inteiro -> 0-DELETE; 1-CREATE; ou (2)-UPDATE
        log.aux_tipo_alteracao = solicitacao_alterar_caso_clinico.tipo_alteracao_DEF()
        log.acao = solicitacao_alterar_caso_clinico.acao#inteiro -> 0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
        log.avaliador = usuario#user
        #Fim----------------------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
        # solicitacao_alterar_caso_clinico.salvar_log(usuario=usuario)

        #Inicio --------------Executar-------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
        log.save()
        #Fim-------------------Executar-------------------Salvar aqui na tabela de log ----------------------------------------------------------

        solicitacao_alterar_caso_clinico.delete()#deletando solicitação, pois seus dados já se encontram na tabela de log
        messages.add_message(request, SUCCESS, 'Foi recusada a alteração da amostra.')
        return redirect('/casos_clinicos/solicitacoes/')
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        return redirect('/casos_clinicos/solicitacoes/')

#Ver todos os log de alterações aceitadas e recusadas
def log_solicitacoes_alteracao_casos_clinicos(request):
    # if not request.user.is_staff:#Se não for administrador
    #     messages.add_message(request, ERROR, 'Você não tem Permissão para acessar esta página.')#mensagem para o usuario
    #     return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg

    usuario = request.user
    try:
        #todas as solicitações ordenadas pel data
        if not usuario.is_staff:#Se não for administrador
            logs = Log.objects.filter(solicitante=usuario).order_by('-data_solicitacao')
        else:#se for adm
            logs = Log.objects.filter().order_by('-data_alteracao')
        return render(request,'log_caso_clinico.html',{'logs':logs})
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        return redirect('/casos_clinicos/solicitacoes/')

#LoginRequiredMixin significa que o usuario precisar estar logado pra acesssar a pagina

################################################################### INICIO SALAS #################################################################################



class Nova_Sala(LoginRequiredMixin, CreateView):
    model = Sala
    success_url = reverse_lazy("doctrainingapp:todas_salas")
    # success_url = reverse_lazy('todas_salas')
    template_name = 'create_generico.html'
    fields = ['nome_sala','descricao', 'area']
    # fields = '__all__'
    # exclude = ['user']
    # success_url = reverse_lazy('author-list')
    # from django.urls import reverse_lazy
    def form_valid(self, form):
        form.instance.responsavel_sala = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        messages.add_message(request, WARNING, 'Nova Sala Virtual .')#mensagem para o usuario
        return super(Nova_Sala, self).get(request, *args, **kwargs)


class Editar_Sala(UpdateView):
    model = Sala
    success_url = reverse_lazy("doctrainingapp:todas_salas")
    template_name = 'update_generico.html'#
    fields = ['nome_sala','descricao']

    def get(self, request, *args, **kwargs):
        if (self.get_object().responsavel_sala != self.request.user):
            messages.add_message(request, ERROR, 'Você não tem Permissão para editar esta sala.')#mensagem para o usuario
            return redirect('/salas/todas/')
        messages.add_message(request, WARNING, 'Sala Virtual .')#mensagem para o usuario
        return super(Editar_Sala, self).get(request, *args, **kwargs)

class Deletar_Sala(DeleteView):
    model = Sala
    success_url = '/salas/todas/'
    template_name = 'delete.html'

    def get(self, request, *args, **kwargs):
        if ((self.get_object().responsavel_sala != self.request.user) and not request.user.is_staff):
            messages.add_message(request, ERROR, 'Você não tem Permissão para deletar esta sala.')#mensagem para o usuario
            return redirect('/salas/todas/')
        messages.add_message(request, WARNING, 'Sala "' + self.get_object().nome_sala + '" será excluida.')#mensagem para o usuario
        messages.add_message(request, WARNING, 'Todas perguntas nesta sala serão excluidas.')#mensagem para o usuario
        return super(Deletar_Sala, self).get(request, *args, **kwargs)

def todas_salas(request):
    usuario = request.user
    try:
        #todas as solicitações ordenadas pel data
        salas = Sala.objects.all().extra( select={'nome_sala_QS': 'lower(nome_sala)'}).order_by('nome_sala_QS')
        return render(request,'salas_todas.html',{'salas':salas})
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro ao abriar salas. Tente novamente mais tarde.')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        return redirect('/doctraining/')


def nova_pergunta(request,pk_sala):
    usuario = request.user
    try:
        sala = Sala.objects.get(pk=pk_sala)
        if(sala.responsavel_sala.pk != request.user.pk):
            messages.add_message(request, ERROR, 'Você não tem Permissão para entrar nesta sala.')#mensagem para o usuario
            return redirect('/salas/todas/')
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro ao abriar perguntas. Tente novamente mais tarde.')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        return redirect('/salas/todas/')

    if  request.method == "POST":#se tiver sido eviado os dados no formulario
        continuar = request.POST.get('post')#Qual botão foi presionado
        try:#tente
            pergunta = request.POST.get('pergunta')
            opcao_correta = request.POST.get('opcao_correta')
            opcao_incorreta_1 = request.POST.get('opcao_incorreta_1')
            opcao_incorreta_2 = request.POST.get('opcao_incorreta_2')
            opcao_incorreta_3 = request.POST.get('opcao_incorreta_3')
            #se os dados forem muito pequenos
            if( len(pergunta) < 10 or len(opcao_correta) <1 or len(opcao_incorreta_1) <1 or len(opcao_incorreta_2) <1 or len(opcao_incorreta_3) <1):
                messages.add_message(request, ERROR, 'Os dados são muito pequenos')#mensagem para o usuario
                return render(request,'pergunta_na_sala_nova.html',{'sala':sala})
            #se os dados forem muito grandes
            if( len(pergunta) > 1500 or len(opcao_correta) > 600 or len(opcao_incorreta_1) >600 or len(opcao_incorreta_2) >600 or len(opcao_incorreta_3) > 600):
                messages.add_message(request, ERROR, 'Os dados são muito grandes')#mensagem para o usuario
                return render(request,'pergunta_na_sala_nova.html',{'sala':sala})
            Pergunta(sala=sala, pergunta=pergunta, opcao_correta=opcao_correta, opcao_incorreta_1=opcao_incorreta_1, opcao_incorreta_2=opcao_incorreta_2, opcao_incorreta_3=opcao_incorreta_3 ).save()
            messages.add_message(request, SUCCESS, 'Foi adicionada uma pergunta na sala '+ str(sala.nome_sala) )
            if ( continuar == 'Salvar'):#Salvar apenas esse
                return redirect('/salas/'+str(pk_sala)+'/perguntas/')
                # return reverse("doctrainingapp:todas_perguntas", args=[pk_sala])
            else:#Continuar
                return render(request,'pergunta_na_sala_nova.html',{'sala':sala})
        except Exception as e:
            messages.add_message(request, ERROR, 'Ocorreu um erro ao salvar pergunta. Tente novamente mais tarde.')#mensagem para o usuario
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return redirect('/salas/todas/')
    else:#Abrir tela
        return render(request,'pergunta_na_sala_nova.html',{'sala':sala})
    #fields = ['pergunta','opcao_correta','opcao_incorreta_1','opcao_incorreta_2','opcao_incorreta_3']


class Editar_Pergunta(UpdateView):
    model = Pergunta
    # success_url = '/salas/todas/'
    # success_url = reverse_lazy("doctrainingapp:todas_salas")
    template_name = 'update_generico.html'#
    fields = ['pergunta','opcao_correta','opcao_incorreta_1','opcao_incorreta_2','opcao_incorreta_3']

    def get(self, request, *args, **kwargs):
        if (self.get_object().sala.responsavel_sala != self.request.user):
            messages.add_message(request, ERROR, 'Você não tem Permissão para editar esta pergunta.')#mensagem para o usuario
            return redirect('/salas/todas/')
        # self.success_url = '/salas/'+ str(self.get_object().sala.pk) +'/perguntas/'
        # self.success_url = '/'
        messages.add_message(request, WARNING, 'Editar Pergunta.')#mensagem para o usuario
        return super(Editar_Pergunta, self).get(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        # return '/salas/'+ str(self.get_object().sala.pk) +'/perguntas/'
        return reverse_lazy("doctrainingapp:todas_perguntas", args=(self.get_object().sala.pk, ))

class Deletar_Pergunta(DeleteView):
    model = Pergunta
    template_name = 'delete.html'

    def get(self, request, *args, **kwargs):
        if (self.get_object().sala.responsavel_sala != self.request.user):
            messages.add_message(request, ERROR, 'Você não tem Permissão para deletar esta pergunta.')#mensagem para o usuario
            return redirect('/salas/todas/')
        messages.add_message(request, WARNING, 'Pergunta "' + self.get_object().pergunta + '" da Sala "'+self.get_object().sala.nome_sala+' "será excluida.')#mensagem para o usuario
        return super(Deletar_Pergunta, self).get(request, *args, **kwargs)
    def get_success_url(self, **kwargs):
        # return '/salas/'+ str(self.get_object().sala.pk) +'/perguntas/'
        return reverse_lazy("doctrainingapp:todas_perguntas", args=(self.get_object().sala.pk, ))

def todas_perguntas(request,pk_sala):
    usuario = request.user
    try:
        sala = Sala.objects.get(pk=pk_sala)
        if((sala.responsavel_sala.pk != request.user.pk) and not request.user.is_staff):
            messages.add_message(request, ERROR, 'Você não tem Permissão para entrar nesta sala.')#mensagem para o usuario
            return redirect('/salas/todas/')
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro ao abriar perguntas. Tente novamente mais tarde.')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        return redirect('/salas/todas/')

    try:
        # perguntas = Pergunta.objects.filter(sala=sala).order_by('pergunta')
        perguntas = Pergunta.objects.filter(sala=sala).extra( select={'pergunta_QS': 'lower(pergunta)'}).order_by('pergunta_QS')
        # return HttpResponse(perguntas)
        return render(request,'perguntas_sala_todas.html',{'sala':sala,'perguntas':perguntas})
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro ao abriar a sala. Tente novamente mais tarde.')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        return redirect('/doctraining/')


if not(settings.PROJETO_EM_TESTE):
    def mandar_email_error( msg_erro,usuario='Desconhecido',url_erro='Desconhecida'):
        send_mail(
        'Erro em Execução Doctraining',#Titulo da msg
        'Olá Jesaías Silva, \nHouve um erro ocultado durante a execução do DocTraining.\n\nUsuário Logado:\n'+str(usuario)+'\n\nURL:\n'+str(url_erro)+ '\n\nErro: \n'+msg_erro+'\n\nAtt \nDocTraining \ndoctraining.herokuapp.com',#Mensagem
        'doctraining.ufersa.contato@gmail.com',
        ['jesayassilva@gmail.com','doctraining.ufersa@gmail.com'],
        # settings.ADMINS,
        fail_silently=False,
        )
        print('Email de Erro enviado')
else:
    print("PROJETO EM TESTE")



