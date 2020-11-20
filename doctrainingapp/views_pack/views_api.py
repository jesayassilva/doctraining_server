from django.http import HttpResponse, JsonResponse
from doctrainingapp.models import *
import random
from django.shortcuts import render
from doctrainingapp.views import *
from doctrainingapp.views_pack import views_ia
from datetime import datetime


def api(request):
    usuario = request.user#usuario logado
    return render(request,'api.html',{'usuario':usuario})

def nome_doencas_casos_clinicos_api(request):
    usuario = request.user
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
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return JsonResponse({"Erro":str(e)}, status = 400)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 400)

#API
def nome_sintomas_casos_clinicos_api(request):
    usuario = request.user
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
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return JsonResponse({"Erro":str(e)}, status = 400)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 400)

#API
def nome_sintomas_casos_clinicos_api(request):
    usuario = request.user
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
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return JsonResponse({"Erro":str(e)}, status = 400)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 400)

#API
def todos_casos_clinicos_doencas_sintomas_api(request):
    usuario = request.user
    if request.method == 'GET':#Mostra todos os objetos
        print(views_ia.tentar_ativar_am() )
        try:
            json_lista_casos_clinicos = []
            casos_clinicos = Caso_Clinico.objects.exclude(doenca = None).order_by('doenca__nome_doenca')
            for caso_clinico in casos_clinicos:#todas as Linhas
                lista_sintomas = []
                falsa_doenca = ''
                if caso_clinico.falsa_doenca is None:
                    falsa_doenca = random.choice(Doenca.objects.exclude(pk = caso_clinico.doenca.pk))
                    falsa_doenca = falsa_doenca.nome_doenca
                else:
                    falsa_doenca = caso_clinico.falsa_doenca.nome_doenca

                for sintoma in caso_clinico.sintomas.order_by('nome_sintoma'):
                    lista_sintomas.append(sintoma.nome_sintoma)
                linha_caso_clinico = {
                'id':caso_clinico.pk,
                'doenca': caso_clinico.doenca.nome_doenca,
                'falsa_doenca': falsa_doenca,
                'sintomas': lista_sintomas
                }
                json_lista_casos_clinicos.append(linha_caso_clinico)
            return JsonResponse(json_lista_casos_clinicos,safe=False)
        except Exception as e:
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return JsonResponse({"Erro":str(e)}, status = 400)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 400)

#API
def um_caso_clinico_doenca_sintomas_api(request):
    usuario = request.user
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
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return JsonResponse({"Erro":str(e)}, status = 400)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 400)



def perguntas_de_uma_sala_api(request,pk_sala):
    usuario = request.user
    if request.method == 'GET':#Mostra todos os objetos
        print(views_ia.tentar_ativar_am() )
        try:
            json_lista_perguntas_de_uma_sala = []
            sala = Sala.objects.get(pk = pk_sala)
            perguntas = Pergunta.objects.filter(sala=sala).order_by('pergunta')
            for pergunta in perguntas:#todas as Linhas
                lista = []
                linha_pergunta = {
                'id':pergunta.pk,
                'difficulty': pergunta.dificuldade,
                'mainQuestion':pergunta.pergunta,
                'rightOp': pergunta.opcao_correta,
                'wrongOp01': pergunta.opcao_incorreta_1,
                'wrongOp02': pergunta.opcao_incorreta_2,
                'wrongOp03': pergunta.opcao_incorreta_3,
                'imageList': lista,

                }

                json_lista_perguntas_de_uma_sala.append(linha_pergunta)
                ima1 = ''
                ima2 = ''
                ima3 = ''
                if pergunta.imagem1:
                    ima1 = pergunta.imagem1.url

                if pergunta.imagem2:
                    ima2 = pergunta.imagem2.url

                if pergunta.imagem3:
                    ima3 = pergunta.imagem3.url

                linha_ima = {
                    'image1': ima1,
                    'image2': ima2,
                    'image3': ima3
                }
                linha_pergunta['imageList'].append(linha_ima)

            return JsonResponse(json_lista_perguntas_de_uma_sala,safe=False)
        except Exception as e:
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return JsonResponse({"Erro":str(e)}, status = 406)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 404)



def todos_salas_api(request):
    usuario = request.user
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
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return JsonResponse({"Erro":str(e)}, status = 406)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 404)


def versao_api(request, versao_versao):
    usuario = request.user
    if request.method == 'GET':#Mostra todos os objetos
        try:
            json_versao = []
            versoes = Versao.objects.filter(versao__gt=versao_versao).order_by('versao')
            lista_informações = []
            lista_atualizações = []
            versao_aux = 0
            critica = False
            for versao in versoes:#todas as Linhas
                lista_informações.append(versao.informacao)
                versao_aux = versao.versao
                lista_atualizações.append(versao.atualizacao_critica)
            if True in lista_atualizações :
                critica = True
            if versao_aux == 0:
                versao_aux = versao_versao
            linha_versao = {
            'versao':versao_aux,
            'informacoes':lista_informações,
            'atualizacao_critica':critica
             }
            json_versao.append(linha_versao)

            return JsonResponse(json_versao,safe=False)
        except Exception as e:
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return JsonResponse({"Erro":str(e)}, status = 406)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 404)


def areas_salas_api(request):
    usuario = request.user
    if request.method == 'GET':#Mostra todos os objetos
        try:
            json_lista_salas = []
            areas = Area.objects.all()
            salas = Sala.objects.all().order_by('area')
            for area in areas:
                lista = []
                linha_area = {
                    'id': area.pk,
                    'area_nome': area.nome,
                    'salas_list': lista }
                for sala in salas:#todas as Linhas
                    if sala.area == area:
                        linha_sala = {
                        'id':sala.pk,
                        'sala_nome': sala.nome_sala,
                        'quantidade_perguntas':sala.quantidade_perguntas()
                        }
                        linha_area['salas_list'].append(linha_sala)
                json_lista_salas.append(linha_area)
            return JsonResponse(json_lista_salas,safe=False)
        except Exception as e:
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return JsonResponse({"Erro":str(e)}, status = 406)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 404)


def conteudos_api(request):
    usuario = request.user
    if request.method == 'GET':#Mostra todos os objetos
        try:
            json_lista_conteudos = []

            conteudos = Conteudo.objects.all().order_by('titulo')
            for conteudo in conteudos:#todas as Linhas
                lista = []
                linha_conteudo = {
                'area': conteudo.area.nome,
                'sala': conteudo.sala.nome_sala,
                'id':conteudo.pk,
                'title': conteudo.titulo,
                'description':conteudo.descricao,
                'content': conteudo.conteudo,
                'link': conteudo.link,
                'reference': conteudo.referencia,
                'imageList':lista,
                'creationDate': conteudo.data_criacao
                }


                ima1 = ''
                ima2 = ''
                ima3 = ''
                if conteudo.imagem1:
                    ima1 = conteudo.imagem1.url

                if conteudo.imagem2:
                    ima2 = conteudo.imagem2.url

                if conteudo.imagem3:
                    ima3 = conteudo.imagem3.url

                linha_ima = {
                    'image1': ima1,
                    'image2': ima2,
                    'image3': ima3
                }
                linha_conteudo['imageList'].append(linha_ima)
                json_lista_conteudos.append(linha_conteudo)

            return JsonResponse(json_lista_conteudos,safe=False)
        except Exception as e:
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return JsonResponse({"Erro":str(e)}, status = 406)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 404)

def fases_api(request, pk_area):
    usuario = request.user
    if request.method == 'GET':#Mostra todos os objetos
        try:
            json_lista_fases = []
            fases = Fase.objects.filter(area=pk_area).order_by('dificuldade')
            perguntas = PerguntaFase.objects.all()
            for fase in fases:
                lista = []
                lista_ima = []
                linha_caso = {
                    'id': fase.pk ,
                    'description': fase.descricao,
                    'difficulty': fase.dificuldade,
                    'questionList': lista,
                    "imageList": lista_ima }

                ima1 = ''
                ima2 = ''
                ima3 = ''
                if fase.imagem1:
                    ima1 = fase.imagem1.url

                if fase.imagem2:
                    ima2 = fase.imagem2.url

                if fase.imagem3:
                    ima3 = fase.imagem3.url

                linha_ima = {
                    'image1': ima1,
                    'image2': ima2,
                    'image3': ima3
                }
                linha_caso['imageList'].append(linha_ima)
                for pergunta in perguntas:#todas as Linhas
                    if pergunta.fase == fase:

                        linha_pergunta = {
                        'questionId':pergunta.pk,
                        'mainQuestion': pergunta.pergunta,
                        'rightOp': pergunta.opcao_correta,
                        "wrongOp01": pergunta.opcao_incorreta_1 ,
                        "wrongOp02":pergunta.opcao_incorreta_2 ,
                        "wrongOp03":pergunta.opcao_incorreta_3,

                        }



                        linha_caso['questionList'].append(linha_pergunta)
                json_lista_fases.append(linha_caso)
            return JsonResponse(json_lista_fases,safe=False)
        except Exception as e:
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return JsonResponse({"Erro":str(e)}, status = 406)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 404)

def areasFase(request):
    usuario = request.user
    if request.method == 'GET':#Mostra todos os objetos
        try:
            json_lista_fases = []
            areas = AreaFase.objects.all()
            for area in areas:
                linha_area = {
                    'id': area.pk,
                    'areaName': area.nome,
                    'fasesCount': area.quantidade_fases(),
                    }
                json_lista_fases.append(linha_area)
            return JsonResponse(json_lista_fases,safe=False)
        except Exception as e:
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return JsonResponse({"Erro":str(e)}, status = 406)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 404)

def getdatatime(request):
    usuario = request.user
    if request.method == 'GET':#Mostra todos os objetos
        try:
            json_lista_datatime = []
            now = datetime.now()
            print("now =", now)
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print("date and time =", dt_string)
            json_lista_datatime.append(dt_string)
            return JsonResponse(json_lista_datatime,safe=False)
        except Exception as e:
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            return JsonResponse({"Erro":str(e)}, status = 406)
    return JsonResponse({"Erro":"Somente Metodo GET"}, status = 404)