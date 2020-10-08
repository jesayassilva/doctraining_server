from django.views.generic import ListView, CreateView, UpdateView
from doctrainingapp.views import *
#DECORATORS
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
import json


@login_required(login_url='')
def conteudo_list(request, template_name='conteudo-list.html'):
    conteudos = Conteudo.objects.all()

    return render(request, template_name, {'conteudos': conteudos})

@login_required(login_url='')
def conteudo_view(request, pk, template_name='conteudo-view.html'):
    conteudo = get_object_or_404(Conteudo, pk=pk)
    return render(request, template_name, {'conteudo':conteudo})

'''
@login_required(login_url='')
def conteudo_add(request, template_name='conteudo-add.html'):
    form = ConteudoForm(request.POST, request.FILES or None)
    areas = Area.objects.all()
    salas = Sala.objects.all()

    if form.is_valid():

        try:
            conteudo_aux = Conteudo.objects.get(titulo=request.POST['titulo'])

            if conteudo_aux:
                messages.error(request, 'Erro! Conteudo ja existe.')
                # return redirect('/conteudos')
                return redirect(reverse_lazy("doctrainingapp:list-conteudo"))
        except:
            salaselect = Sala.objects.get(pk=request.POST.get('selecao'))
            print(salaselect)

            conteudo = form.save(commit=False)
            conteudo.sala = salaselect
            conteudo.save()
            # return redirect('/conteudos')
            return redirect(reverse_lazy("doctrainingapp:list-conteudo"))
    return render(request, template_name, {'form':form, 'salas': salas, 'areas': areas })


@login_required(login_url='')
def conteudo_edit(request, pk, template_name='conteudo-edit.html'):
    conteudo= get_object_or_404(Conteudo, pk=pk)
    form = ConteudoForm(request.POST or None, instance=conteudo)
    if form.is_valid():
        form.save()
        # return redirect('/conteudos')
        return redirect(reverse_lazy("doctrainingapp:list-conteudo"))
    return render(request, template_name, {'form':form})
'''

@login_required(login_url='')
def conteudo_delete(request, pk, template_name='conteudo-delete.html'):
    conteudo = get_object_or_404(Conteudo, pk=pk)
    if request.method=='POST':
        conteudo.delete()
        # return redirect('/conteudos')
        return redirect(reverse_lazy("doctrainingapp:list-conteudo"))
    return render(request, template_name, {'object':conteudo})


########################################################################
class ConteudoListView(ListView):
    model = Conteudo
    context_object_name = 'conteudo'

class ConteudoCreateView(CreateView):
    model = Conteudo
    form_class = ConteudoForm
    template_name = 'conteudo_form.html'
    #fields = ('area','sala','titulo', 'descricao', 'conteudo', 'link', 'referencia', 'imagem1', 'imagem2', 'imagem3')
    success_url = reverse_lazy('doctrainingapp:list-conteudo')

class ConteudoUpdateView(UpdateView):
    model = Conteudo
    form_class = ConteudoForm
    template_name = 'conteudo_form.html'
    #fields = ('area','sala','titulo', 'descricao', 'conteudo', 'link', 'referencia', 'imagem1', 'imagem2', 'imagem3')
    success_url = reverse_lazy('doctrainingapp:list-conteudo')

def load_cities(request):
    area_id = request.GET.get('area')
    salas = Sala.objects.filter(area_id=area_id).order_by('nome_sala')
    return render(request, 'dropdown_list_options.html', {'salas': salas})