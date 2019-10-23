from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.views.generic.edit import DeleteView,CreateView,UpdateView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
import random
import pandas as pd
import numpy as np

from django.db import models

# Create your views here.
# DEBUG=10
# INFO=20
SUCCESS=25
WARNING=30
ERROR=40


def index(request):
    usuario = request.user#usuario logado
    return render(request,'index.html',{'usuario':usuario})

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


def casos_clinicos(request):
    usuario = request.user#usuario logado
    try:
        casos_clinicos = Caso_Clinico.objects.filter().order_by('doenca__nome_doenca')#todos os casos clinicos
        return render(request,'casos_clinicos.html',{'casos_clinicos':casos_clinicos,'usuario':usuario})
    except Exception as e:
         return HttpResponse('Erro: '+ str(e))

#solicitação de edicão de caso clinico
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



def solicitacoes_alteracao_casos_clinicos(request):
    usuario = request.user
    try:
        #todas as solicitações ordenadas pel data
        solicitacao_alterar_caso_clinico = Solicitacao_Alterar_Caso_Clinico.objects.filter().order_by('data_solicitacao')
        return render(request,'solicitacao_alterar_caso_clinico.html',{'solicitacao_alterar_caso_clinico':solicitacao_alterar_caso_clinico,'usuario':usuario})
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
        return redirect('/casos_clinicos/solicitacoes/')


def aceitar_solicitacao_alteracao_caso_clinico(request,pk):
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
            log.solicitante = solicitacao_alterar_caso_clinico.solicitante_DEF()#string
            #Antigos
            log.doenca = solicitacao_alterar_caso_clinico.nome_doenca_antigo_DEF()#string
            log.sintomas = solicitacao_alterar_caso_clinico.sintomas_antigo_DEF()#string
            #Novos
            log.nova_doenca = solicitacao_alterar_caso_clinico.nome_doenca_novo_DEF()#string
            log.novos_sintomas = solicitacao_alterar_caso_clinico.sintomas_novos_DEF()#string

            log.doenca_classificada = solicitacao_alterar_caso_clinico.doenca_classificada#boolena
            log.tipo_alteracao = solicitacao_alterar_caso_clinico.tipo_alteracao#inteiro -> 0-DELETE; 1-CREATE; ou (2)-UPDATE
            log.acao = solicitacao_alterar_caso_clinico.acao#inteiro -> 0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            log.avaliado_por = usuario.username#string
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
            log.solicitante = solicitacao_alterar_caso_clinico.solicitante_DEF()#string
            #Antigos
            log.doenca = solicitacao_alterar_caso_clinico.nome_doenca_antigo_DEF()#string
            log.sintomas = solicitacao_alterar_caso_clinico.sintomas_antigo_DEF()#string
            #Novos
            log.nova_doenca = solicitacao_alterar_caso_clinico.nome_doenca_novo_DEF()#string
            log.novos_sintomas = solicitacao_alterar_caso_clinico.sintomas_novos_DEF()#string

            log.doenca_classificada = solicitacao_alterar_caso_clinico.doenca_classificada#boolena
            log.tipo_alteracao = solicitacao_alterar_caso_clinico.tipo_alteracao#inteiro -> 0-DELETE; 1-CREATE; ou (2)-UPDATE
            log.acao = solicitacao_alterar_caso_clinico.acao#inteiro -> 0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            log.avaliado_por = usuario.username#string
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
            log.solicitante = solicitacao_alterar_caso_clinico.solicitante_DEF()#string
            #Antigos
            log.doenca = solicitacao_alterar_caso_clinico.nome_doenca_antigo_DEF()#string
            log.sintomas = solicitacao_alterar_caso_clinico.sintomas_antigo_DEF()#string
            #Novos
            log.nova_doenca = solicitacao_alterar_caso_clinico.nome_doenca_novo_DEF()#string
            log.novos_sintomas = solicitacao_alterar_caso_clinico.sintomas_novos_DEF()#string

            log.doenca_classificada = solicitacao_alterar_caso_clinico.doenca_classificada#boolena
            log.tipo_alteracao = solicitacao_alterar_caso_clinico.tipo_alteracao#inteiro -> 0-DELETE; 1-CREATE; ou (2)-UPDATE
            log.acao = solicitacao_alterar_caso_clinico.acao#inteiro -> 0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            log.avaliado_por = usuario.username#string
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
        return redirect('/casos_clinicos/solicitacoes/')
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde. '+ str(e))#mensagem para o usuario
        return redirect('/casos_clinicos/solicitacoes/')





def rejeitar_solicitacao_alteracao_caso_clinico(request,pk):
    usuario = request.user#usuario logado, se tiver
    try:
        #Solicitação de alteração em casos clinicos
        solicitacao_alterar_caso_clinico = Solicitacao_Alterar_Caso_Clinico.objects.get(pk=pk)
        solicitacao_alterar_caso_clinico.acao =0#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE

        #Inicio ----------------------------------Salvar aqui nessa linha na tabela de log ------------------------------------------------
        log = Log()#cria objeto de log, linhas a seguir são de adicionar os dados
        log.data_solicitacao = solicitacao_alterar_caso_clinico.data_solicitacao#data e hora
        log.solicitante = solicitacao_alterar_caso_clinico.solicitante_DEF()#string
        #Antigos
        log.doenca = solicitacao_alterar_caso_clinico.nome_doenca_antigo_DEF()#string
        log.sintomas = solicitacao_alterar_caso_clinico.sintomas_antigo_DEF()#string
        #Novos
        log.nova_doenca = solicitacao_alterar_caso_clinico.nome_doenca_novo_DEF()#string
        log.novos_sintomas = solicitacao_alterar_caso_clinico.sintomas_novos_DEF()#string

        log.doenca_classificada = solicitacao_alterar_caso_clinico.doenca_classificada#boolena
        log.tipo_alteracao = solicitacao_alterar_caso_clinico.tipo_alteracao#inteiro -> 0-DELETE; 1-CREATE; ou (2)-UPDATE
        log.acao = solicitacao_alterar_caso_clinico.acao#inteiro -> 0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
        log.avaliado_por = usuario.username#string
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





def log_solicitacoes_alteracao_casos_clinicos(request):
    usuario = request.user
    try:
        #todas as solicitações ordenadas pel data
        logs = Log.objects.filter().order_by('-data_alteracao')
        return render(request,'log_caso_clinico.html',{'logs':logs,'usuario':usuario})
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
        return redirect('/casos_clinicos/solicitacoes/')






###################################################################### WEB SERVICE ##############################################################################

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

'''
classe_casos_clinicos = 'class'
def ler_dados_salvar(request):
    df = pd.read_csv('casos_clinicos.csv') #lendo os dados
    print(' -------- Data Frame --------')
    print(df)

    print(' -------- Salvando Doenças --------')
    lista_doencas = df[classe_casos_clinicos].unique()
    for item in lista_doencas:
        try:
            doenca = Doenca.objects.get(nome_doenca=item.upper())
        except Exception as e:
            doenca = Doenca(nome_doenca=item.upper())
            doenca.save()
            print(item.upper())

    print(' -------- Salvando Sintomas --------')
    lista_sintomas = df.columns
    for item in lista_sintomas:
        if item != classe_casos_clinicos:
            try:
                sintoma = Sintoma.objects.get(nome_sintoma=item.upper())
            except Exception as e:
                sintoma = Sintoma(nome_sintoma=item.upper())
                sintoma.save()
                print(item.upper())

    print(' -------- Salvando Casos Clínicos --------')
    for linha in df.values:#todas as Linhas do DataFrame
        lista_sintomas_caso_clinico = []
        doenca_caso_clinico = None
        linhas_e_colunas = zip(linha,df.columns) #Zipar as duas variaveis em uma só ou seja Uma linhas com as colunas respectivas
        for valor,coluna in linhas_e_colunas:#Rodar laço com nome da coluna e valor
            if coluna != classe_casos_clinicos:#se aquela coluna não for do nome da doença
                    if valor == 1:#Se tiver o sintoma
                        # lista_sintomas_caso_clinico.append(coluna)
                        lista_sintomas_caso_clinico.append(Sintoma.objects.get(nome_sintoma=coluna.upper()))
            else:
                doenca_caso_clinico = Doenca.objects.get(nome_doenca=valor.upper())

        caso_clinico = Caso_Clinico()#Novo objeto de caso clinico
        caso_clinico.doenca = doenca_caso_clinico#adicinando doenca
        caso_clinico.doenca_classificada = True#adicionando se doença é classificada ou não
        caso_clinico.save()#salvando o caso clinico
        caso_clinico.sintomas.set(lista_sintomas_caso_clinico)#Adicionando os sintomas após objeto ser salvo pelo metodo get()
        print(caso_clinico)




    print(' -------- Todos os Dados Salvos --------')
    return HttpResponse('Salvo com sucesso')
    # return redirect('/')#voltar para tela inicial
'''


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






#
