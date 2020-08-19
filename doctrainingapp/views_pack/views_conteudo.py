
from doctrainingapp.views import *
#DECORATORS
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required



@login_required(login_url='')
@staff_member_required
def conteudo_list(request, template_name='conteudo-list.html'):
    conteudos = Conteudo.objects.all()

    return render(request, template_name, {'conteudos': conteudos})

@login_required(login_url='')
@staff_member_required
def conteudo_view(request, pk, template_name='conteudo-view.html'):
    conteudo = get_object_or_404(Conteudo, pk=pk)
    return render(request, template_name, {'conteudo':conteudo})


@login_required(login_url='')
@staff_member_required
def conteudo_add(request, template_name='conteudo-add.html'):
    form = ConteudoForm(request.POST, request.FILES or None)
    if form.is_valid():
        try:
            conteudo_aux = Conteudo.objects.get(titulo=request.POST['titulo'])

            if conteudo_aux:
                messages.error(request, 'Erro! Conteudo ja existe.')
                return redirect('/doctraining/conteudos')
        except:
            form.save()
            return redirect('/doctraining/conteudos')
    return render(request, template_name, {'form':form})


@login_required(login_url='')
@staff_member_required
def conteudo_edit(request, pk, template_name='conteudo-edit.html'):
    conteudo= get_object_or_404(Conteudo, pk=pk)
    form = ConteudoForm(request.POST or None, instance=conteudo)
    if form.is_valid():
        form.save()
        return redirect('/doctraining/conteudos')
    return render(request, template_name, {'form':form})


@login_required(login_url='')
@staff_member_required
def conteudo_delete(request, pk, template_name='conteudo-delete.html'):
    conteudo = get_object_or_404(Conteudo, pk=pk)
    if request.method=='POST':
        conteudo.delete()
        return redirect('/doctraining/conteudos')
    return render(request, template_name, {'object':conteudo})
