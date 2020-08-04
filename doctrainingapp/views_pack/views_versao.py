from doctrainingapp.forms import *
from django.shortcuts import render, get_object_or_404
from doctrainingapp.models import *
from django.shortcuts import redirect
from django.contrib import messages
from doctrainingapp.views import *
#DECORATORS
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required



@login_required(login_url='')
@staff_member_required
def versao_list(request, template_name='versao-list.html'):
    versao = Versao.objects.all()

    return render(request, template_name, {'versao': versao})
'''
def versao_view(request, pk, template_name='books/book_detail.html'):
    versao = get_object_or_404(Versao, pk=pk)
    return render(request, template_name, {'object':versao})'''


@login_required(login_url='')
@staff_member_required
def versao_add(request, template_name='versao-add.html'):
    form = VersaoForm(request.POST or None)
    if form.is_valid():
        try:
            versao_aux = Versao.objects.get(versao=request.POST['versao'])

            if versao_aux:
                messages.error(request, 'Erro! Versão ja existe.')
                return redirect('/versao')
        except:
            form.save()
            return redirect('/versao')
    return render(request, template_name, {'form':form})


@login_required(login_url='')
@staff_member_required
def versao_edit(request, pk, template_name='versao-edit.html'):
    versao= get_object_or_404(Versao, pk=pk)
    form = VersaoForm(request.POST or None, instance=versao)
    if form.is_valid():
        form.save()
        return redirect('/versao')
    return render(request, template_name, {'form':form})


@login_required(login_url='')
@staff_member_required
def versao_delete(request, pk, template_name='versao-delete.html'):
    versao = get_object_or_404(Versao, pk=pk)
    if request.method=='POST':
        versao.delete()
        return redirect('/versao')
    return render(request, template_name, {'object':versao})
