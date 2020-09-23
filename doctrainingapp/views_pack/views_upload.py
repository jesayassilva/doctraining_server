from doctrainingapp.views import *
#DECORATORS
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

import csv, io
from django.shortcuts import render
from django.contrib import messages
# Create your views here.
# one parameter named request

def upload(request):
    return render(request,'upload.html')

def area_upload(request):
    data = Area.objects.all()

    prompt = {
        'order': 'A ordem do CSV deve ser area, nome da area ex.:',
        'Area': data
              }

    if request.method == "GET":
        return render(request, 'upload_csv_area.html', prompt)
    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'O arquivo não é .csv')
    data_set = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Area.objects.update_or_create(
            nome=column[0],

        )
    context = {}
    return redirect(reverse_lazy("doctrainingapp:upload"))



def sala_upload(request):

    data = Sala.objects.all()

    prompt = {
        'order': 'A ordem do CSV deve ser area, nome da sala, descrição; ex.:',
        'Sala': data
              }

    if request.method == "GET":
        return render(request, 'upload_csv_sala.html', prompt)
    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'O arquivo não é .csv')
    data_set = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Sala.objects.update_or_create(
            area=Area.objects.get(nome=column[0]),
            nome_sala=column[1],
            descricao=column[2],
            responsavel_sala=request.user,

        )
    context = {}
    return redirect(reverse_lazy("doctrainingapp:upload"))

def pergunta_sala_upload(request):

    data = Pergunta.objects.all()

    prompt = {
        'order': 'A ordem do CSV deve ser sala, pergunta, opção correta, opções incorretas, dificuldade(1 à 5); ex.:',
        'Pergunta': data
              }

    if request.method == "GET":
        return render(request, 'upload_csv_pergunta_sala.html', prompt)
    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'O arquivo não é .csv')
    data_set = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Pergunta.objects.update_or_create(
            sala=Sala.objects.get(nome_sala=column[0]),
            pergunta=column[1],
            opcao_correta=column[2],
            opcao_incorreta_1=column[3],
            opcao_incorreta_2=column[4],
            opcao_incorreta_3=column[5],
            dificuldade=column[6],

        )
    context = {}
    return redirect(reverse_lazy("doctrainingapp:upload"))

def fase_upload(request):

    data = Fase.objects.all()

    prompt = {
        'order': 'A ordem do CSV deve ser area, nome da fase, descrição, dificuldade(1 à 5); ex.:',
        'Fase': data
              }

    if request.method == "GET":
        return render(request, 'upload_csv_fase.html', prompt)
    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'O arquivo não é .csv')
    data_set = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Fase.objects.update_or_create(
            area=Area.objects.get(nome=column[0]),
            nome_fase=column[1],
            descricao=column[2],
            responsavel_fase=request.user,
            dificuldade=column[3],

        )
    context = {}
    return redirect(reverse_lazy("doctrainingapp:upload"))

def pergunta_fase_upload(request):

    data = PerguntaFase.objects.all()

    prompt = {
        'order': 'A ordem do CSV deve ser sala, pergunta, opção correta, opções incorretas, dificuldade(1 à 5); ex.:',
        'Pergunta': data
              }

    if request.method == "GET":
        return render(request, 'upload_csv_pergunta_fase.html', prompt)
    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'O arquivo não é .csv')
    data_set = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = PerguntaFase.objects.update_or_create(
            fase=Fase.objects.get(nome_fase=column[0]),
            pergunta=column[1],
            opcao_correta=column[2],
            opcao_incorreta_1=column[3],
            opcao_incorreta_2=column[4],
            opcao_incorreta_3=column[5],

        )
    context = {}
    return redirect(reverse_lazy("doctrainingapp:upload"))