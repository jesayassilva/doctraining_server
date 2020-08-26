from doctrainingapp.views import *
import io
from ftplib import FTP

classe_casos_clinicos = 'class'
nome_class_DF_casos_clinicos = 'class'
def ler_dados_salvar(request):
    df = pd.read_csv('backup_casos_clinicos.csv') #lendo os dados
    # df = pd.read_csv('backup.csv') #lendo os dados
    # df = pd.read_csv('backup_casos_clinicos.csv') #lendo os dados do backup
    print(' -------- Data Frame --------')
    print(df)

    print(' -------- Salvando Doenças --------')
    lista_doencas = df[classe_casos_clinicos].unique()
    for item in lista_doencas:
        try:
            # doenca = Doenca.objects.get(nome_doenca=item.upper().replace("_", " "))
            doenca = Doenca.objects.get(nome_doenca=item.replace("_", " "))
        except Exception as e:
            # doenca = Doenca(nome_doenca=item.upper().replace("_", " "))
            doenca = Doenca(nome_doenca=item.replace("_", " "))
            doenca.save()
            print(item.replace("_", " "))

    print(' -------- Salvando Sintomas --------')
    lista_sintomas = df.columns
    for item in lista_sintomas:
        if item != classe_casos_clinicos:
            try:
                # sintoma = Sintoma.objects.get(nome_sintoma=item.upper().replace("_", " "))
                sintoma = Sintoma.objects.get(nome_sintoma=item.replace("_", " "))
            except Exception as e:
                # sintoma = Sintoma(nome_sintoma=item.upper().replace("_", " "))
                sintoma = Sintoma(nome_sintoma=item.replace("_", " "))
                sintoma.save()
                print(item.replace("_", " "))

    print(' -------- Salvando Casos Clínicos --------')
    salvos = 0
    for linha in df.values:#todas as Linhas do DataFrame
        lista_sintomas_caso_clinico = []
        doenca_caso_clinico = None
        linhas_e_colunas = zip(linha,df.columns) #Zipar as duas variaveis em uma só ou seja Uma linhas com as colunas respectivas
        for valor,coluna in linhas_e_colunas:#Rodar laço com nome da coluna e valor
            if coluna != classe_casos_clinicos:#se aquela coluna não for do nome da doença
                    if valor == 1:#Se tiver o sintoma
                        # lista_sintomas_caso_clinico.append(coluna)
                        # lista_sintomas_caso_clinico.append(Sintoma.objects.get(nome_sintoma=coluna.upper().replace("_", " ")))
                        lista_sintomas_caso_clinico.append(Sintoma.objects.get(nome_sintoma=coluna.replace("_", " ")))
            else:
                # doenca_caso_clinico = Doenca.objects.get(nome_doenca=valor.upper().replace("_", " "))
                doenca_caso_clinico = Doenca.objects.get(nome_doenca=valor.replace("_", " "))
        caso_clinico = Caso_Clinico()#Novo objeto de caso clinico
        caso_clinico.doenca = doenca_caso_clinico#adicinando doenca
        caso_clinico.doenca_classificada = True#adicionando se doença é classificada ou não
        caso_clinico.save()#salvando o caso clinico
        caso_clinico.sintomas.set(lista_sintomas_caso_clinico)#Adicionando os sintomas após objeto ser salvo pelo metodo get()
        print(caso_clinico)
        salvos = salvos+1
        print(str(salvos)+' Caso Clinico Salvo')




    print(' -------- Todos os Dados Salvos --------')
    return HttpResponse('Salvo com sucesso')
    # return redirect('/')#voltar para tela inicial

import threading
def gerar_csv(request):
    threading_do_bck_casos_clinicos = threading.Thread(target=bck_casos_clinicos)
    threading_do_bck_casos_clinicos.start()#o normal
    messages.add_message(request, SUCCESS, 'Gerando CSV de Backup...')#mensagem para o usuario
    # return redirect('/doctraining/')
    return redirect(reverse_lazy("doctrainingapp:doctraining"))


def bck_casos_clinicos():
    try:
        print('Inicio gerar csv')
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

        print("Savando CSV...")
        # #FTP
        # ftp = FTP()
        # ftp.connect('files.000webhost.com', 21)
        # ftp.login('jesaias','minha D N')
        # ftp.cwd ('/public_html/doctraining/')
        # buffer = io.StringIO()
        # df.to_csv(buffer,index=False)
        # text = buffer.getvalue()
        # bio = io.BytesIO(str.encode(text))
        # ftp.storbinary('STOR backup_casos_clinicos.csv', bio)
        # ftp.close()
        # #FTP

        df.to_csv('backup_casos_clinicos.csv',index=False) #Salvando dataframe em csv e usando
        print("Savando CSV: OK")
    except Exception as e:
        mandar_email_error(msg_erro=str(e), url_erro="BCK Casos Clinicos")
