from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.views.generic.edit import DeleteView,CreateView,UpdateView
from django.contrib.auth.forms import  UserCreationForm#,AuthenticationForm,UserChangeForm,PasswordResetForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
import random
import pandas as pd
import numpy as np

from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls import reverse

import requests

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
    return render(request,'index.html',{'usuario':usuario})

def doctraining(request):
    usuario = request.user#usuario logado
    return render(request,'doctraining.html',{'usuario':usuario})

def api(request):
    usuario = request.user#usuario logado
    return render(request,'api.html',{'usuario':usuario})

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
         return HttpResponse('Erro: '+ str(e))

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
                messages.add_message(request, ERROR, 'Ocorreu um erro ao adicionar sintomas. Tente novamente mais tarde.')#mensagem para o usuario
            return redirect('/casos_clinicos/')
        except Exception as e:
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
            messages.add_message(request, ERROR, 'Ocorreu um erro ao adicionar sintomas da exclusão. Tente novamente mais tarde.')#mensagem para o usuario
            solicitacao_alterar_caso_clinico.delete()
        return redirect('/casos_clinicos/')
        # a4.publications.set([p3])
        # return HttpResponse(str(lista_sintomas_novo))
    except Exception as e:
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
                messages.add_message(request, ERROR, 'Ocorreu um erro ao adicionar sintomas. Tente novamente mais tarde.')
            return redirect('/casos_clinicos/')
            # a4.publications.set([p3])
            # return HttpResponse(str(lista_sintomas_novo))
        except Exception as e:
            messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
            return redirect('/casos_clinicos/')
    else:
        try:
            doencas = Doenca.objects.filter().order_by('nome_doenca')#todas as doencas
            sintomas = Sintoma.objects.filter().order_by('nome_sintoma')#todos os sintomas
            return render(request,'solicitar_novo_caso_clinico.html',{'doencas':doencas,'sintomas':sintomas, 'usuario':usuario})
        except Exception as e:
            messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
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
        #se Deletar amostra
        if solicitacao_alterar_caso_clinico.tipo_alteracao == 0:#Deletar caso clinico
            caso_clinico = Caso_Clinico.objects.get(pk = solicitacao_alterar_caso_clinico.caso_clinico_a_modificar.pk)#pegando caso clinico relacionado
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
            log.acao = solicitacao_alterar_caso_clinico.acao#inteiro -> 0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            log.avaliador = usuario#user
            # log.avaliado_por = usuario.username#string
            #Fim----------------------------------Salvar aqui na tabela de log  ------------------------------------------------
            # solicitacao_alterar_caso_clinico.salvar_log(usuario=usuario)

            #Inicio --------------Executar-------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
            log.save()
            #Fim-------------------Executar-------------------Salvar aqui na tabela de log ----------------------------------------------------------


            solicitacao_alterar_caso_clinico.delete()#deletando solicitação, pois seus dados já se encontram na tabela de log
            caso_clinico.delete()#deletando caso clinico, pois pois pedido foi aceito (execultando pedido)
        # se Nova amostra
        elif solicitacao_alterar_caso_clinico.tipo_alteracao == 1:#Novo caso clinico
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
            log.acao = solicitacao_alterar_caso_clinico.acao#inteiro -> 0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            log.avaliador = usuario#user
            #Fim----------------------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
            # solicitacao_alterar_caso_clinico.salvar_log(usuario=usuario)

            #Inicio --------------Executar-------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
            log.save()
            #Fim-------------------Executar-------------------Salvar aqui na tabela de log ----------------------------------------------------------

            solicitacao_alterar_caso_clinico.delete()#deletando solicitação, pois seus dados já se encontram na tabela de log
        #se Editar amostra
        else:#Editar caso clinico
            caso_clinico = Caso_Clinico.objects.get(pk = solicitacao_alterar_caso_clinico.caso_clinico_a_modificar.pk)#caso clinico que será modificado
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
            log.acao = solicitacao_alterar_caso_clinico.acao#inteiro -> 0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            log.avaliador = usuario#user

            #Fim----------------------------------Salvar aqui na tabela de log ------------------------------------------------
            # solicitacao_alterar_caso_clinico.salvar_log(usuario=usuario)

            #solicitacao_alterar_caso_clinico.salvar_log(usuario=usuario)
            caso_clinico.doenca = solicitacao_alterar_caso_clinico.nova_doenca#adicinando doenca
            caso_clinico.doenca_classificada = solicitacao_alterar_caso_clinico.doenca_classificada#adicionando se doença é classificada ou não
            caso_clinico.save()#salvando o caso clinico
            caso_clinico.sintomas.set(solicitacao_alterar_caso_clinico.novos_sintomas.all())#Adicionando os sintomas após objeto ser salvo pelo metodo get()

            #Inicio --------------Executar-------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
            log.save()
            #Fim-------------------Executar-------------------Salvar aqui na tabela de log ----------------------------------------------------------
            solicitacao_alterar_caso_clinico.delete()#deletando solicitação, pois seus dados já se encontram na tabela de log
        #mensagem para usuario
        messages.add_message(request, SUCCESS, 'Foi aceitada a alteração da amostra.')
        # r = requests.get('http://127.0.0.1:8000/ativar_am')
        return redirect('/casos_clinicos/solicitacoes/')
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde. '+ str(e))#mensagem para o usuario
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
            logs = Log.objects.filter(solicitante=usuario).order_by('-data_alteracao')
        else:#se for adm
            logs = Log.objects.filter().order_by('-data_alteracao')
        return render(request,'log_caso_clinico.html',{'logs':logs})
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
        return redirect('/casos_clinicos/solicitacoes/')

#LoginRequiredMixin significa que o usuario precisar estar logado pra acesssar a pagina



################################################################### INICIO SALAS #################################################################################

class Nova_Sala(LoginRequiredMixin, CreateView):
    model = Sala
    success_url = reverse_lazy("doctrainingapp:todas_salas")
    # success_url = reverse_lazy('todas_salas')
    template_name = 'create_generico.html'
    fields = ['nome_sala','descricao']
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
        if (self.get_object().responsavel_sala != self.request.user):
            messages.add_message(request, ERROR, 'Você não tem Permissão para deletar esta sala.')#mensagem para o usuario
            return redirect('/salas/todas/')
        messages.add_message(request, WARNING, 'Sala "' + self.get_object().nome_sala + '" será excluida.')#mensagem para o usuario
        messages.add_message(request, WARNING, 'Todas perguntas nesta sala serão excluidas.')#mensagem para o usuario
        return super(Deletar_Sala, self).get(request, *args, **kwargs)

def todas_salas(request):
    try:
        #todas as solicitações ordenadas pel data
        salas = Sala.objects.all().extra( select={'nome_sala_QS': 'lower(nome_sala)'}).order_by('nome_sala_QS')
        return render(request,'salas_todas.html',{'salas':salas})
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro ao abriar salas. Tente novamente mais tarde.')#mensagem para o usuario
        return redirect('/doctraining/')


def nova_pergunta(request,pk_sala):
    try:
        sala = Sala.objects.get(pk=pk_sala)
        if(sala.responsavel_sala.pk != request.user.pk):
            messages.add_message(request, ERROR, 'Você não tem Permissão para entrar nesta sala.')#mensagem para o usuario
            return redirect('/salas/todas/')
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro ao abriar perguntas. Tente novamente mais tarde.')#mensagem para o usuario
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
    try:
        sala = Sala.objects.get(pk=pk_sala)
        if(sala.responsavel_sala.pk != request.user.pk):
            messages.add_message(request, ERROR, 'Você não tem Permissão para entrar nesta sala.')#mensagem para o usuario
            return redirect('/salas/todas/')
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro ao abriar perguntas. Tente novamente mais tarde.')#mensagem para o usuario
        return redirect('/salas/todas/')

    try:
        # perguntas = Pergunta.objects.filter(sala=sala).order_by('pergunta')
        perguntas = Pergunta.objects.filter(sala=sala).extra( select={'pergunta_QS': 'lower(pergunta)'}).order_by('pergunta_QS')
        # return HttpResponse(perguntas)
        return render(request,'perguntas_sala_todas.html',{'sala':sala,'perguntas':perguntas})
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro ao abriar a sala. Tente novamente mais tarde.'+ str(e))#mensagem para o usuario
        return redirect('/doctraining/')


###################################################################### INICIO API WEB SERVICE ##############################################################################
#API
def nome_doencas_casos_clinicos_api(request):
    if request.method == 'GET':#Mostra todos os objetos
        try:
            json_lista_doencas = []
            doencas = Doenca.objects.order_by('nome_doenca')
            for doenca in doencas:#todas as Linhas
                linha_doenca = {
                'id':doenca.pk,
                'doenca': doenca.nome_doenca
                }
                json_lista_doencas.append(linha_doenca)
            return JsonResponse(json_lista_doencas,safe=False)
        except Exception as e:
             return JsonResponse({"Erro":str(e)}, status = 400)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 400)

#API
def nome_sintomas_casos_clinicos_api(request):
    if request.method == 'GET':#Mostra todos os objetos
        try:
            json_lista_sintomas = []
            sintomas = Sintoma.objects.order_by('nome_sintoma')
            for sintoma in sintomas:#todas as Linhas
                linha_sintoma = {
                'id':sintoma.pk,
                'sintoma': sintoma.nome_sintoma
                }
                json_lista_sintomas.append(linha_sintoma)

            return JsonResponse(json_lista_sintomas,safe=False)
        except Exception as e:
             return JsonResponse({"Erro":str(e)}, status = 400)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 400)

#API
def nome_sintomas_casos_clinicos_api(request):
    if request.method == 'GET':#Mostra todos os objetos
        try:
            json_lista_sintomas = []
            sintomas = Sintoma.objects.order_by('nome_sintoma')
            for sintoma in sintomas:#todas as Linhas
                linha_sintoma = {
                'id':sintoma.pk,
                'sintoma': sintoma.nome_sintoma
                }
                json_lista_sintomas.append(linha_sintoma)

            return JsonResponse(json_lista_sintomas,safe=False)
        except Exception as e:
             return JsonResponse({"Erro":str(e)}, status = 400)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 400)

#API
def todos_casos_clinicos_doencas_sintomas_api(request):
    if request.method == 'GET':#Mostra todos os objetos
        try:
            json_lista_casos_clinicos = []
            casos_clinicos = Caso_Clinico.objects.exclude(doenca = None).order_by('doenca__nome_doenca')
            for caso_clinico in casos_clinicos:#todas as Linhas
                lista_sintomas = []
                for sintoma in caso_clinico.sintomas.order_by('nome_sintoma'):
                    lista_sintomas.append(sintoma.nome_sintoma)
                linha_caso_clinico = {
                'id':caso_clinico.pk,
                'doenca': caso_clinico.doenca.nome_doenca,
                'sintomas': lista_sintomas
                }
                json_lista_casos_clinicos.append(linha_caso_clinico)
            return JsonResponse(json_lista_casos_clinicos,safe=False)
        except Exception as e:
             return JsonResponse({"Erro":str(e)}, status = 400)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 400)

#API
def um_caso_clinico_doenca_sintomas_api(request):
    if request.method == 'GET':#Mostra todos os objetos
        try:
            caso_clinico = random.choice(Caso_Clinico.objects.exclude(doenca = None).order_by('doenca__nome_doenca'))
            lista_sintomas = []
            for sintoma in caso_clinico.sintomas.order_by('nome_sintoma'):
                lista_sintomas.append(sintoma.nome_sintoma)

            json_caso_clinico = {
            'id':caso_clinico.pk,
            'doenca': caso_clinico.doenca.nome_doenca,
            'sintomas': lista_sintomas
            }

            return JsonResponse(json_caso_clinico,safe=False)
        except Exception as e:
             return JsonResponse({"Erro":str(e)}, status = 400)

    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 400)



def perguntas_de_uma_sala_api(request,pk_sala):
    if request.method == 'GET':#Mostra todos os objetos
        try:
            json_lista_perguntas_de_uma_sala = []
            sala = Sala.objects.get(pk = pk_sala)
            perguntas = Pergunta.objects.filter(sala=sala).order_by('pergunta')
            for pergunta in perguntas:#todas as Linhas
                linha_pergunta = {
                'id':pergunta.pk,
                'mainQuestion':pergunta.pergunta,
                'rightOp': pergunta.opcao_correta,
                'wrongOp01': pergunta.opcao_incorreta_1,
                'wrongOp02': pergunta.opcao_incorreta_2,
                'wrongOp03': pergunta.opcao_incorreta_3
                }
                json_lista_perguntas_de_uma_sala.append(linha_pergunta)
            return JsonResponse(json_lista_perguntas_de_uma_sala,safe=False)
        except Exception as e:
             return JsonResponse({"Erro":str(e)}, status = 406)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 404)



def todos_salas_api(request):
    if request.method == 'GET':#Mostra todos os objetos
        try:
            json_lista_salas = []
            salas = Sala.objects.all().order_by('nome_sala')
            for sala in salas:#todas as Linhas
                linha_sala = {
                'id':sala.pk,
                'sala_nome': sala.nome_sala,
                'quantidade_perguntas':sala.quantidade_perguntas()
                }
                json_lista_salas.append(linha_sala)
            return JsonResponse(json_lista_salas,safe=False)
        except Exception as e:
             return JsonResponse({"Erro":str(e)}, status = 406)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 404)


###################################################################### FIM API WEB SERVICE ##############################################################################



###################################################################### INICIO SALVAR DADOS DO CSV NO BANCO ##############################################################################
classe_casos_clinicos = 'class'
def ler_dados_salvar(request):
    df = pd.read_csv('casos_clinicos.csv') #lendo os dados
    print(' -------- Data Frame --------')
    print(df)

    print(' -------- Salvando Doenças --------')
    lista_doencas = df[classe_casos_clinicos].unique()
    for item in lista_doencas:
        try:
            doenca = Doenca.objects.get(nome_doenca=item.upper().replace("_", " "))
        except Exception as e:
            doenca = Doenca(nome_doenca=item.upper().replace("_", " "))
            doenca.save()
            print(item.upper().replace("_", " "))

    print(' -------- Salvando Sintomas --------')
    lista_sintomas = df.columns
    for item in lista_sintomas:
        if item != classe_casos_clinicos:
            try:
                sintoma = Sintoma.objects.get(nome_sintoma=item.upper().replace("_", " "))
            except Exception as e:
                sintoma = Sintoma(nome_sintoma=item.upper().replace("_", " "))
                sintoma.save()
                print(item.upper().replace("_", " "))

    print(' -------- Salvando Casos Clínicos --------')
    for linha in df.values:#todas as Linhas do DataFrame
        lista_sintomas_caso_clinico = []
        doenca_caso_clinico = None
        linhas_e_colunas = zip(linha,df.columns) #Zipar as duas variaveis em uma só ou seja Uma linhas com as colunas respectivas
        for valor,coluna in linhas_e_colunas:#Rodar laço com nome da coluna e valor
            if coluna != classe_casos_clinicos:#se aquela coluna não for do nome da doença
                    if valor == 1:#Se tiver o sintoma
                        # lista_sintomas_caso_clinico.append(coluna)
                        lista_sintomas_caso_clinico.append(Sintoma.objects.get(nome_sintoma=coluna.upper().replace("_", " ")))
            else:
                doenca_caso_clinico = Doenca.objects.get(nome_doenca=valor.upper().replace("_", " "))

        caso_clinico = Caso_Clinico()#Novo objeto de caso clinico
        caso_clinico.doenca = doenca_caso_clinico#adicinando doenca
        caso_clinico.doenca_classificada = True#adicionando se doença é classificada ou não
        caso_clinico.save()#salvando o caso clinico
        caso_clinico.sintomas.set(lista_sintomas_caso_clinico)#Adicionando os sintomas após objeto ser salvo pelo metodo get()
        print(caso_clinico)




    print(' -------- Todos os Dados Salvos --------')
    return HttpResponse('Salvo com sucesso')
    # return redirect('/')#voltar para tela inicial
###################################################################### FIM SALVAR DADOS DO CSV NO BANCO ##############################################################################





################################################################### INICIO USER ##################################################

# class SenhaAndUserUpdate(UpdateView):
#     model = User
#     form_class = UserCreationForm
#     #form_class = ProvaForm
#     success_url = '/'
#     template_name = 'update_generico.html'
#
#     def get(self, request, *args, **kwargs):
#         if (self.get_object().pk != self.request.user.pk):
#             messages.add_message(request, ERROR, 'Você não tem Permissão para editar este usuário.')#mensagem para o usuario
#             return redirect('/salas/todas/')
#         messages.add_message(request, WARNING, 'Atualizar Usuário.')#mensagem para o usuario
#         return super(SenhaAndUserUpdate, self).get(request, *args, **kwargs)


class UserUpdate(UpdateView):
    model = User
    # form_class = UserCreationForm
    #form_class = username
    fields = ['username','first_name','last_name','email']
    success_url = '/doctraining/'
    template_name = 'update_generico.html'

    def get(self, request, *args, **kwargs):
        if (self.get_object().pk != self.request.user.pk):
            messages.add_message(request, ERROR, 'Você não tem Permissão para editar este usuário.')#mensagem para o usuario
            return redirect('/doctraining/')
        # messages.add_message(request, WARNING, 'Atualizar Usuário.')#mensagem para o usuario
        return super(UserUpdate, self).get(request, *args, **kwargs)



class UserCreate(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = '/doctraining/'
    template_name = 'create_generico.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_staff:#Se não for administrador
            messages.add_message(request, ERROR, 'Você não tem Permissão para adicionar usuários.')#mensagem para o usuario
            return redirect('/doctraining/')
        # messages.add_message(request, WARNING, 'Atualizar Usuário.')#mensagem para o usuario
        return super(UserCreate, self).get(request, *args, **kwargs)





class PerfilUpdate(UpdateView):
    model = Perfil
    success_url = '/doctraining/'
    template_name = 'update_generico.html'
    fields = ['apelido','instituicao','idade']

    def get(self, request, *args, **kwargs):
        if (self.get_object().user.pk != self.request.user.pk):
            messages.add_message(request, ERROR, 'Você não tem Permissão para editar este perfil.')#mensagem para o usuario
            return redirect('/doctraining/')
        messages.add_message(request, WARNING, 'Atualizar Perfil.')#mensagem para o usuario
        return super(PerfilUpdate, self).get(request, *args, **kwargs)



############################################# Machine Learning #################################
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split#Importar divisão
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import classification_report, confusion_matrix # importar metodo de avaliação
from sklearn.linear_model import LogisticRegression #Importar regressão logistica

###### Threading
import logging#Mostra logs neste caso de horario
import threading
import time

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

stop_threads = False

nome_class_DF_casos_clinicos = 'class'
taxa_aprendizado = ''
# def aprender(request):
def aprender():
    print('Inicio Função aprender')
    global stop_threads
    global taxa_aprendizado
    print("Obter dados...")
    sintomas = Sintoma.objects.all().order_by('pk')
    casos_clinicos = Caso_Clinico.objects.exclude(doenca = None,doenca_classificada = False).order_by('pk')
    casos_clinicos_sem_classificacao = Caso_Clinico.objects.filter(doenca_classificada = False).order_by('pk')
    print("Obter dados: OK")

    print("Lista Sintomas...")
    lista_sintomas = []
    lista_sintomas_sem_class =[]
    for sintoma in sintomas:#adicinar sintiomas desse caso clinico a lista
        lista_sintomas.append(sintoma.nome_sintoma)
        lista_sintomas_sem_class.append(sintoma.nome_sintoma)
    lista_sintomas.append(nome_class_DF_casos_clinicos)
    df = pd.DataFrame(columns=lista_sintomas)
    # casos_clinicos = Caso_Clinico.Sintoma.objects.all().order_by('pk')
    print("Lista Sintomas: OK")

    if stop_threads:#se for para parar
        return

    print("Data Frame...")
    for caso_clinico in casos_clinicos:
        valor_linha = []

        for sintoma in sintomas:
            if sintoma in caso_clinico.sintomas.all():
                valor_linha.append(1)
            else:
                valor_linha.append(0)
        valor_linha.append(caso_clinico.doenca.nome_doenca)
        df_auxiliar = pd.DataFrame([valor_linha], columns=lista_sintomas)
        df = df.append(df_auxiliar,ignore_index=True)
    # print(df.head())
    print("Data Frame: OK")

    ######### DATA SET MONTADO #############
    if stop_threads:#se for para parar
        return

    print("Treino e Teste...")
    X = df.drop('class',axis=1)
    y = df['class']
    X_train, X_test, y_train, y_test = train_test_split(X, #train.drop('Survived',axis=1) remove a coluna e a retorna mas não altera na variavel
                                                        y, test_size=0.20,
                                                        random_state=254)#Dividir os dados em treino e teste
    logmodel = LogisticRegression(C=10000)#contrutor
    logmodel.fit(X_train,y_train)#treino
    logmodel_predictions = logmodel.predict(X_test)#predizer dados de treinos
    print(confusion_matrix(y_test,logmodel_predictions)) #Ver resultados
    print(classification_report(y_test,logmodel_predictions)) #Ver resultados
    scores = cross_val_score(logmodel, X, y, cv=5, scoring='f1_micro')
    print(scores)
    print(scores.mean())
    taxa_aprendizado = str(round(scores.mean()*100,2))
    print("Treino e Teste: OK")

    if stop_threads:
        return
    print("Classificação Dados...")
    for caso_clinico in casos_clinicos_sem_classificacao:
        valor_linha_classificar = []

        for sintoma in sintomas:
            if sintoma in caso_clinico.sintomas.all():
                valor_linha_classificar.append(1)
            else:
                valor_linha_classificar.append(0)
        df_classificar = pd.DataFrame([valor_linha_classificar], columns=lista_sintomas_sem_class)
        #classificando novo dado
        print(df_classificar)
        print("Classificado como: ")
        resultado = logmodel.predict(df_classificar)
        print(resultado)

        try:
            nova_doenca = Doenca.objects.get(nome_doenca = resultado[0])#pegar doenca selecionada no formulario
            caso_clinico.doenca = nova_doenca#adicinando doenca
            caso_clinico.doenca_classificada = False#variavel indica que a doenca não foi classificada pelo usuario
            caso_clinico.save()#salvando o caso clinico

        except Exception as e:
            print('ERRO: '+str(e))
    # '''
    print("Classificação Dados: OK")

    print('Fim Função aprender')




horario_inicio_am = 2
horario_fim_am = 3

def chamar_funcao_aprender():
    while True:
        global stop_threads
        if stop_threads:
            break#parar thread
        if ( int(time.strftime('%H')) >= horario_inicio_am and int(time.strftime('%H')) <= horario_fim_am ):
            print('CHAMA FUNÇÃO APRENDER')
            aprender()
        else:
            print("FORA DO HORARIO. Classificação: "+ str(horario_inicio_am) +' e '+ str(horario_fim_am) +':59 horas.')
        # r = requests.get('http://127.0.0.1:8000/status_am/')
        # r = requests.get('doctraining.herokuapp.com')
        r = requests.get('https://doctraining.herokuapp.com')
        print(r)
        time.sleep(60)
        #espera 60 segundos



threading_do_aprendizado_maquina = threading.Thread(target=chamar_funcao_aprender)
def ativar_am(request):#Rodar Thread
    if not request.user.is_staff:#Se não for administrador
        messages.add_message(request, ERROR, 'Você não tem Permissão para acessar esta página.')#mensagem para o usuario
        return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg

    global stop_threads
    global threading_do_aprendizado_maquina
    stop_threads = False
    #se nao tiver ativo ativar
    if not threading_do_aprendizado_maquina.is_alive():
        threading_do_aprendizado_maquina = threading.Thread(target=chamar_funcao_aprender)
        threading_do_aprendizado_maquina.start()#o normal
        mensagem = 'Ativado.'+ ' Classificação entre '+ str(horario_inicio_am) +' e '+ str(horario_fim_am) +':59 horas.' + ' Taxa de Aprendizado: ' + taxa_aprendizado+"%"
    else:
        mensagem ='Já encontra-se ativo.' + ' Classificação entre '+ str(horario_inicio_am) +' e '+ str(horario_fim_am) +':59 horas.' + ' Taxa de Aprendizado: ' + taxa_aprendizado+"%"
        # print("APRENDIZADO DE MÁQUINA JÁ ENCONTRA-SE ATIVA")
        # return HttpResponse("APRENDIZADO DE MÁQUINA JÁ ENCONTRA-SE ATIVA")
    # threading_do_aprendizado_maquina.run()
    # print("APRENDIZADO DE MÁQUINA ATIVA")
    # return HttpResponse("APRENDIZADO DE MÁQUINA ATIVO")
    return render(request,'am.html',{'mensagem':mensagem})


def desativar_am(request):#Parar Thread
    if not request.user.is_staff:#Se não for administrador
        messages.add_message(request, ERROR, 'Você não tem Permissão para acessar esta página.')#mensagem para o usuario
        return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg
    try:
        global stop_threads
        global threading_do_aprendizado_maquina
        # stop_threads = True
        #se nao tiver ativo ativar
        # if not threading_do_aprendizado_maquina.is_alive():
        if not stop_threads:
            stop_threads = True
            threading_do_aprendizado_maquina.join()
            mensagem = 'Desativado'
        else:
            stop_threads = True
            # print("APRENDIZADO DE MÁQUINA JÁ ENCONTRA-SE PARADA")
            # return HttpResponse("APRENDIZADO DE MÁQUINA JÁ ENCONTRA-SE PARADA")
            mensagem =  'Já encontra-se desativado'
    except Exception as e:
        mensagem = 'Erro: Não foi possível parar o Aprendizado de Máquina ou já encontra-se desativado'
        # print('ERRO: Não foi possivel parar Thread')
        # return HttpResponse('ERRO: NÃO FOI POSSIVEL PARAR O APRENDIZADO DE MÁQUINA')
    return render(request,'am.html',{'mensagem':mensagem})
    # print('APRENDIZADO DE MÁQUINA PARADO')
    # return HttpResponse('APRENDIZADO DE MÁQUINA PARADO')

def status_am(request):
    if not request.user.is_staff:#Se não for administrador
        messages.add_message(request, ERROR, 'Você não tem Permissão para acessar esta página.')#mensagem para o usuario
        return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg
    if threading_do_aprendizado_maquina.is_alive():
        # return HttpResponse('ATIVO')
        mensagem = 'Ativo: Classificação entre '+ str(horario_inicio_am) +' e '+ str(horario_fim_am) +':59 horas.' + ' Taxa de Aprendizado: ' + taxa_aprendizado+"%"
    else:
        # return HttpResponse('PARADO')
        mensagem = 'Desativado'
    return render(request,'am.html',{'mensagem':mensagem})


def am_agora(request):
    global stop_threads
    global threading_do_aprendizado_maquina
    if not request.user.is_staff:#Se não for administrador
        messages.add_message(request, ERROR, 'Você não tem Permissão para acessar esta página.')#mensagem para o usuario
        return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg
    if not threading_do_aprendizado_maquina.is_alive():
        stop_threads = False
        aprender()
        stop_threads = True
        # return HttpResponse("CLASSIFICAÇÃO DO APRENDIZADO DE MÁQUINA CONCLUIDO")
        mensagem = 'Classificação do Aprendizado de Máquina concluído.'+ ' Taxa de Aprendizado: ' + taxa_aprendizado+"%"
    elif not ( int(time.strftime('%H')) >= horario_inicio_am and int(time.strftime('%H')) <= horario_fim_am ):
        print("Horario")
        aprender()
        mensagem = 'Classificação do Aprendizado de Máquina concluído.' + ' Taxa de Aprendizado: ' + taxa_aprendizado+"%"
    else:
        # return HttpResponse("CLASSIFICAÇÃO EM USO PELO APRENDIZADO DE MÁQUINA")
        print("AM em uso")
        mensagem = 'Classificação em uso pelo Aprendizado de Máquina.'+ ' Taxa de Aprendizado: ' + taxa_aprendizado+"%"
    return render(request,'am.html',{'mensagem':mensagem})








#
