from doctrainingapp.views import *
from doctrainingapp.models import Fase, AreaFase
'''
class Nova_Fase(LoginRequiredMixin, CreateView):
    id_area = 0
    model = Fase
    success_url = reverse_lazy("doctrainingapp:todas_fases")
    # success_url = reverse_lazy('todas_salas')
    template_name = 'create_generico.html'
    fields = ['nome_fase','descricao',  'dificuldade']
    # fields = '__all__'
    # exclude = ['user']
    # success_url = reverse_lazy('author-list')
    # from django.urls import reverse_lazy
    def form_valid(self, form):
        form.instance.area = Area.objects.get(pk=self.id_area)
        form.instance.responsavel_fase = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        messages.add_message(request, WARNING, 'Nova Fase.')#mensagem para o usuario
        return super(Nova_Fase, self).get(request, *args, **kwargs)
'''
@login_required(login_url='')

def fase_add(request, area_pk, template_name='fase-add.html'):
    area = AreaFase.objects.get(pk=area_pk)
    form = FaseForm(request.POST, request.FILES or None)
    if form.is_valid():
        try:
            fase_aux = Fase.objects.get(nome_fase=request.POST['nome_fase'])

            if fase_aux:
                messages.error(request, 'Erro! Fase ja existe.')
                # return redirect('/conteudos')
                return redirect(reverse_lazy("doctrainingapp:areas_fase_list"))
        except:
            fase = form.save(commit=False)
            fase.area = area
            fase.responsavel_fase = request.user
            fase.save()
            # return redirect('/conteudos')
            return redirect(reverse_lazy("doctrainingapp:areas_fase_list"))
    return render(request, template_name, {'form':form})


class Editar_Fase(UpdateView):
    model = Fase
    success_url = reverse_lazy("doctrainingapp:areas_fase_list")
    template_name = 'update_generico.html'#
    fields = ['nome_fase','descricao', 'dificuldade']

    def get(self, request, *args, **kwargs):
        if (self.get_object().responsavel_fase != self.request.user):
            messages.add_message(request, ERROR, 'Você não tem Permissão para editar esta Fase.')#mensagem para o usuario
            # return redirect('/fases/todas/')
            return redirect(reverse_lazy("doctrainingapp:todas_fases"))
        messages.add_message(request, WARNING, 'Fase Virtual .')#mensagem para o usuario
        return super(Editar_Fase, self).get(request, *args, **kwargs)

class Deletar_Fase(DeleteView):
    model = Fase
    success_url = reverse_lazy("doctrainingapp:areas_fase_list")
    # '/fases/todas/'
    template_name = 'delete.html'

    def get(self, request, *args, **kwargs):
        if ((self.get_object().responsavel_fase != self.request.user) and not request.user.is_staff):
            messages.add_message(request, ERROR, 'Você não tem Permissão para deletar esta fase.')#mensagem para o usuario
            # return redirect('/fases/todas/')
            return redirect(reverse_lazy("doctrainingapp:todas_fases"))
        messages.add_message(request, WARNING, 'Fase "' + self.get_object().nome_fase + '" será excluida.')#mensagem para o usuario
        messages.add_message(request, WARNING, 'Todas perguntas nesta Fase serão excluidas.')#mensagem para o usuario
        return super(Deletar_Fase, self).get(request, *args, **kwargs)

def todas_fases(request, pk_area):
    usuario = request.user
    try:
        #todas as solicitações ordenadas pel data
        fases = Fase.objects.filter(area=pk_area).extra(select={'nome_fase_QS': 'lower(nome_fase)'}).order_by('nome_fase_QS')
        return render(request,'fases_todas.html',{'fases':fases, 'pk_area': pk_area} )
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro ao abrir fases. Tente novamente mais tarde.')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        # return redirect('/doctraining/')
        return redirect(reverse_lazy("doctrainingapp:doctraining"))


def nova_pergunta(request,pk_fase):
    usuario = request.user
    try:
        fase = Fase.objects.get(pk=pk_fase)
        if(fase.responsavel_fase.pk != request.user.pk) :
            messages.add_message(request, ERROR, 'Você não tem Permissão para entrar nesta fase.')#mensagem para o usuario
            # return redirect('/fases/todas/')
            return redirect(reverse_lazy("doctrainingapp:areas_list"))
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro ao abrir perguntas. Tente novamente mais tarde.')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        # return redirect('/fases/todas/')
        return redirect(reverse_lazy("doctrainingapp:areas_list"))

    if  request.method == "POST":#se tiver sido eviado os dados no formulario
        continuar = request.POST.get('post')#Qual botão foi presionado
        try:#tente
            pergunta = request.POST.get('pergunta')
            #dificuldade = request.POST.get('selecao')
            opcao_correta = request.POST.get('opcao_correta')
            opcao_incorreta_1 = request.POST.get('opcao_incorreta_1')
            opcao_incorreta_2 = request.POST.get('opcao_incorreta_2')
            opcao_incorreta_3 = request.POST.get('opcao_incorreta_3')
            imagem1 = request.FILES.get('imagem1')
            imagem2 = request.FILES.get('imagem2')
            imagem3 = request.FILES.get('imagem3')


            # print(dificuldade)
            #se os dados forem muito pequenos
            #if dificuldade == None:
                #messages.add_message(request, ERROR, 'Porfavor adicione uma dificuldade')  # mensagem para o usuario
               # return render(request, 'pergunta_na_fase_nova.html', {'fase': fase})

            if( len(pergunta) < 10 or len(opcao_correta) <1 or len(opcao_incorreta_1) <1 or len(opcao_incorreta_2) <1 or len(opcao_incorreta_3) <1):
                messages.add_message(request, ERROR, 'Os dados são muito pequenos')#mensagem para o usuario
                return render(request,'pergunta_na_fase_nova.html',{'fase':fase})
            #se os dados forem muito grandes
            if( len(pergunta) > 1500 or len(opcao_correta) > 600 or len(opcao_incorreta_1) >600 or len(opcao_incorreta_2) >600 or len(opcao_incorreta_3) > 600):
                messages.add_message(request, ERROR, 'Os dados são muito grandes')#mensagem para o usuario
                return render(request,'pergunta_na_fase_nova.html',{'fase':fase})
            PerguntaFase(fase=fase, pergunta=pergunta, opcao_correta=opcao_correta, opcao_incorreta_1=opcao_incorreta_1, opcao_incorreta_2=opcao_incorreta_2, opcao_incorreta_3=opcao_incorreta_3, imagem1=imagem1, imagem2=imagem2, imagem3=imagem3  ).save()
            messages.add_message(request, SUCCESS, 'Foi adicionada uma pergunta na sala '+ str(fase.nome_fase) )
            if ( continuar == 'Salvar'):#Salvar apenas esse
                # return redirect('/fases/'+str(pk_fase)+'/perguntas/')
                return redirect(reverse_lazy("doctrainingapp:todas_perguntasfase", args=(pk_fase, )))
                # return reverse("doctrainingapp:todas_perguntas", args=[pk_sala])
            else:#Continuar
                return render(request,'pergunta_na_fase_nova.html',{'fase':fase})
        except Exception as e:
            messages.add_message(request, ERROR, 'Ocorreu um erro ao salvar pergunta. Tente novamente mais tarde.')#mensagem para o usuario
            mandar_email_error(str(e),usuario,request.resolver_match.url_name)
            # return redirect('/fases/todas/')
            return redirect(reverse_lazy("doctrainingapp:areas_list"))
    else:#Abrir tela
        return render(request,'pergunta_na_fase_nova.html',{'fase':fase})
    #fields = ['pergunta','opcao_correta','opcao_incorreta_1','opcao_incorreta_2','opcao_incorreta_3']


class Editar_PerguntaFase(UpdateView):
    model = PerguntaFase
    # success_url = '/salas/todas/'
    # success_url = reverse_lazy("doctrainingapp:todas_salas")
    template_name = 'update_generico.html'#
    fields = ['pergunta','opcao_correta','opcao_incorreta_1','opcao_incorreta_2','opcao_incorreta_3', 'imagem1','imagem2','imagem3']

    def get(self, request, *args, **kwargs):
        if (self.get_object().fase.responsavel_fase != self.request.user):
            messages.add_message(request, ERROR, 'Você não tem Permissão para editar esta pergunta.')#mensagem para o usuario
            # return redirect('/fases/todas/')
            return redirect(reverse_lazy("doctrainingapp:areas_list"))
        # self.success_url = '/salas/'+ str(self.get_object().sala.pk) +'/perguntas/'
        # self.success_url = '/'
        messages.add_message(request, WARNING, 'Editar Pergunta.')#mensagem para o usuario
        return super(Editar_PerguntaFase, self).get(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        # return '/salas/'+ str(self.get_object().sala.pk) +'/perguntas/'
        return reverse_lazy("doctrainingapp:todas_perguntasfase", args=(self.get_object().fase.pk, ))

class Deletar_PerguntaFase(DeleteView):
    model = PerguntaFase
    template_name = 'delete.html'

    def get(self, request, *args, **kwargs):
        if (self.get_object().fase.responsavel_fase != self.request.user):
            messages.add_message(request, ERROR, 'Você não tem Permissão para deletar esta pergunta.')#mensagem para o usuario
            # return redirect('/fases/todas/')
            return redirect(reverse_lazy("doctrainingapp:areas_list"))
        messages.add_message(request, WARNING, 'Pergunta "' + self.get_object().pergunta + '" da Fase "'+self.get_object().fase.nome_fase+' "será excluida.')#mensagem para o usuario
        return super(Deletar_PerguntaFase, self).get(request, *args, **kwargs)
    def get_success_url(self, **kwargs):
        # return '/salas/'+ str(self.get_object().sala.pk) +'/perguntas/'
        return reverse_lazy("doctrainingapp:todas_perguntasfase", args=(self.get_object().fase.pk, ))

def todas_perguntas(request,pk_fase):
    usuario = request.user
    try:
        fase = Fase.objects.get(pk=pk_fase)
        if((fase.responsavel_fase.pk != request.user.pk) and not request.user.is_staff):
            messages.add_message(request, ERROR, 'Você não tem Permissão para entrar nesta fase.')#mensagem para o usuario
            # return redirect('/fases/todas/')
            return redirect(reverse_lazy("doctrainingapp:areas_list"))
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro ao abriar perguntas. Tente novamente mais tarde.')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        # return redirect('/fases/todas/')
        return redirect(reverse_lazy("doctrainingapp:areas_list"))

    try:
        # perguntas = Pergunta.objects.filter(sala=sala).order_by('pergunta')
        perguntas = PerguntaFase.objects.filter(fase=fase).extra( select={'pergunta_QS': 'lower(pergunta)'}).order_by('pergunta_QS')
        # return HttpResponse(perguntas)
        return render(request,'perguntas_fase_todas.html',{'fase':fase,'perguntas':perguntas})
    except Exception as e:
        messages.add_message(request, ERROR, 'Ocorreu um erro ao abriar a fase. Tente novamente mais tarde.')#mensagem para o usuario
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        # return redirect('/doctraining/')
        return redirect(reverse_lazy("doctrainingapp:doctraining"))