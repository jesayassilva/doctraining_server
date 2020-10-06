from django.shortcuts import render, get_object_or_404
from doctrainingapp.models import *
from django.shortcuts import redirect
from django.contrib import messages
import pandas as pd
import requests
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split#Importar divisão
from sklearn.metrics import classification_report, confusion_matrix # importar metodo de avaliação
from sklearn.linear_model import LogisticRegression #Importar regressão logistica
from doctrainingapp.views import *

###### Threading
import logging#Mostra logs neste caso de horario
import threading
import time

# redirecionar_sem_permissao = '/doctraining/'
redirecionar_sem_permissao = 'doctrainingapp:doctraining'
SUCCESS=25
WARNING=30
ERROR=40

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

stop_threads = False

nome_class_DF_casos_clinicos = 'class'
taxa_aprendizado = ''
# def aprender(request):
def aprender():
    try:
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
        gerados = 0
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
            gerados = gerados+1
            print(str(gerados)+' Linhas geradas do Data Frame')
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
        classificados = 0
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

            #  Segunda Maior
            ordenada = sorted(logmodel.predict_proba(df_classificar)[0], reverse=True)
            probabilidade_e_classes = zip(logmodel.predict_proba(df_classificar)[0],logmodel.classes_)
            for probabilidade_, classe_ in probabilidade_e_classes:
                if probabilidade_ == ordenada[0]:
                    print("Maior " + str(probabilidade_) + " - " + str(classe_) )
                if probabilidade_ == ordenada[1]:
                    print("Segunda Maior " + str(probabilidade_) + " - " + str(classe_) )
            # Segunda Maior

            try:
                nova_doenca = Doenca.objects.get(nome_doenca = resultado[0])#pegar doenca selecionada no formulario
                caso_clinico.doenca = nova_doenca#adicinando doenca
                caso_clinico.doenca_classificada = False#variavel indica que a doenca não foi classificada pelo usuario
                caso_clinico.save()#salvando o caso clinico
                classificados = classificados+1
            except Exception as e:
                mandar_email_error('Erro ao classificar dados no Aprendizado de Máquina '+str(e))
                print('ERRO: '+str(e))
            print(str(classificados)+' Exemplos Classificados \n')
        # '''
        print('TOTAL' +str(classificados)+ 'Exemplos Classificados \n')
        print("Classificação Dados: OK")


        #Só para Falsa Doença agora, esses dados aboixo já possuem classificação, mas será inserido também a segunda possivel doença para aumentar complexidade
        print("Classificação Falsa Doença nos Dados Classificados...")
        classificados = 0
        for caso_clinico in casos_clinicos:
            valor_linha_classificar = []

            for sintoma in sintomas:
                if sintoma in caso_clinico.sintomas.all():
                    valor_linha_classificar.append(1)
                else:
                    valor_linha_classificar.append(0)
            df_classificar = pd.DataFrame([valor_linha_classificar], columns=lista_sintomas_sem_class)
            print(df_classificar)
            print(".............................. Já é classificado como: " + caso_clinico.doenca.nome_doenca)

            #  Segunda Maior
            ordenada = sorted(logmodel.predict_proba(df_classificar)[0], reverse=True)
            probabilidade_e_classes = zip(logmodel.predict_proba(df_classificar)[0],logmodel.classes_)
            for probabilidade_, classe_ in probabilidade_e_classes:
                if probabilidade_ == ordenada[0]:
                    print("Classe com Maior Probabilidade" + str(probabilidade_) + " - " + str(classe_) )
                if probabilidade_ == ordenada[1]:
                    segunda_maior_probabilidade_doenca_ser_classificada = classe_
                    print(".......... Segunda Maior Classe com Probabilidade " + str(probabilidade_) + " - " + str(classe_) )
            # Segunda Maior

            try:
                if segunda_maior_probabilidade_doenca_ser_classificada != caso_clinico.doenca.nome_doenca:
                    print("Falsa Doença Classificada: OK")
                    falsa_doenca = Doenca.objects.get(nome_doenca = segunda_maior_probabilidade_doenca_ser_classificada)#pegar segunda maior probabilidade
                    caso_clinico.falsa_doenca = falsa_doenca#adicinando falsa doenca
                    caso_clinico.save()#salvando o caso clinico com falsa doença, o resto dos dados não é alterado
                    classificados = classificados+1
                else:
                    print("Algo de errado, são iguais ................................................ Erro \n\n")

            except Exception as e:
                mandar_email_error('Erro ao classificar Falsa doença no Aprendizado de Máquina '+str(e))
                print('ERRO: '+str(e))


            print(str(classificados)+' Exemplos para Falsa Doença Classificados \n')
        # '''
        print('TOTAL' +str(classificados)+ 'Exemplos para Falsa doença Classificados \n')
        print("Classificação Falsa Doença nos Dados Classificados: OK")






        print('Fim Função aprender')
    except Exception as e:
        mandar_email_error(msg_erro=str(e), url_erro="Thread AM")



horario_tarde = 12
horario_inicio_am = 2
horario_fim_am = 3
tempo_espera_segundos = 5
def chamar_funcao_aprender():
    while True:
        global stop_threads
        if stop_threads:
            break#parar thread
        if ( int(time.strftime('%H')) >= horario_inicio_am and int(time.strftime('%H')) <= horario_fim_am ) or ( int(time.strftime('%H')) == horario_tarde and int(time.strftime('%M')) <= 29 ):
            print('CHAMA FUNÇÃO APRENDER')
            aprender()
            time.sleep(300)#5 min de espera após classificações
        else:
            print("FORA DO HORARIO. Classificação: "+ str(horario_inicio_am) +' - '+ str(horario_fim_am) +':59 Horas e ' + str(horario_tarde) +' - '+ str(horario_tarde) + ':30 Horas')
        r = requests.get('https://doctraining.herokuapp.com')
        print(r)
        time.sleep(tempo_espera_segundos)

threading_do_aprendizado_maquina = threading.Thread(target=chamar_funcao_aprender)
def ativar_am(request):#Rodar Thread
    if not request.user.is_staff:#Se não for administrador
        messages.add_message(request, ERROR, 'Você não tem Permissão para acessar esta página.')#mensagem para o usuario
        # return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg
        return redirect(reverse_lazy(redirecionar_sem_permissao))#voltar para pagina que pode acessar e ver a msg
    mensagem = tentar_ativar_am()
    return render(request,'am.html',{'mensagem':mensagem})


def desativar_am(request):#Parar Thread
    if not request.user.is_staff:#Se não for administrador
        messages.add_message(request, ERROR, 'Você não tem Permissão para acessar esta página.')#mensagem para o usuario
        # return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg
        return redirect(reverse_lazy(redirecionar_sem_permissao))#voltar para pagina que pode acessar e ver a msg
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
        # return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg
        return redirect(reverse_lazy(redirecionar_sem_permissao))#voltar para pagina que pode acessar e ver a msg
    if threading_do_aprendizado_maquina.is_alive():
        # return HttpResponse('ATIVO')
        mensagem = 'Ativo: Classificação: '+ str(horario_inicio_am) +' - '+ str(horario_fim_am) +':59 Horas e ' + str(horario_tarde) +' - '+ str(horario_tarde) + ':30 Horas. Taxa de Aprendizado: ' + taxa_aprendizado+"%"
    else:
        # return HttpResponse('PARADO')
        mensagem = 'Desativado'
    return render(request,'am.html',{'mensagem':mensagem})


def am_agora(request):
    global stop_threads
    global threading_do_aprendizado_maquina
    if not request.user.is_staff:#Se não for administrador
        messages.add_message(request, ERROR, 'Você não tem Permissão para acessar esta página.')#mensagem para o usuario
        # return redirect(redirecionar_sem_permissao)#voltar para pagina que pode acessar e ver a msg
        return redirect(reverse_lazy(redirecionar_sem_permissao))#voltar para pagina que pode acessar e ver a msg
    if not threading_do_aprendizado_maquina.is_alive():
        stop_threads = False
        aprender()
        stop_threads = True
        # return HttpResponse("CLASSIFICAÇÃO DO APRENDIZADO DE MÁQUINA CONCLUIDO")
        mensagem = 'Classificação do Aprendizado de Máquina concluído.'+ ' Taxa de Aprendizado: ' + taxa_aprendizado+"%"
    elif not( ( int(time.strftime('%H')) >= horario_inicio_am and int(time.strftime('%H')) <= horario_fim_am ) and ( int(time.strftime('%H')) == horario_tarde and int(time.strftime('%M')) <= 29 ) ):
        print("Horario")
        aprender()
        mensagem = 'Classificação do Aprendizado de Máquina concluído.' + ' Taxa de Aprendizado: ' + taxa_aprendizado+"%"
    else:
        # return HttpResponse("CLASSIFICAÇÃO EM USO PELO APRENDIZADO DE MÁQUINA")
        print("AM em uso")
        mensagem = 'Classificação em uso pelo Aprendizado de Máquina.'+ ' Taxa de Aprendizado: ' + taxa_aprendizado+"%"
    return render(request,'am.html',{'mensagem':mensagem})



def tentar_ativar_am():
    global stop_threads
    global threading_do_aprendizado_maquina
    stop_threads = False
    #se nao tiver ativo ativar
    if not threading_do_aprendizado_maquina.is_alive():
        threading_do_aprendizado_maquina = threading.Thread(target=chamar_funcao_aprender)
        threading_do_aprendizado_maquina.start()#o normal
        mensagem = 'Ativado. Classificação: '+ str(horario_inicio_am) +' - '+ str(horario_fim_am) +':59 Horas e ' + str(horario_tarde) +' - '+ str(horario_tarde) + ':30 Horas. Taxa de Aprendizado: ' + taxa_aprendizado+"%"
    else:
        mensagem ='Já encontra-se ativo. Classificação: '+ str(horario_inicio_am) +' - '+ str(horario_fim_am) +':59 Horas e ' + str(horario_tarde) +' - '+ str(horario_tarde) + ':30 Horas' + ' Taxa de Aprendizado: ' + taxa_aprendizado+"%"
        # print("APRENDIZADO DE MÁQUINA JÁ ENCONTRA-SE ATIVA")
        # return HttpResponse("APRENDIZADO DE MÁQUINA JÁ ENCONTRA-SE ATIVA")
    # threading_do_aprendizado_maquina.run()
    # print("APRENDIZADO DE MÁQUINA ATIVA")
    # return HttpResponse("APRENDIZADO DE MÁQUINA ATIVO")
    return mensagem
