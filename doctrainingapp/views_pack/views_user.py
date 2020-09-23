from doctrainingapp.views import *


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
    success_url = reverse_lazy("doctrainingapp:doctraining")
    template_name = 'update_generico.html'

    def get(self, request, *args, **kwargs):
        if (self.get_object().pk != self.request.user.pk):
            messages.add_message(request, ERROR, 'Você não tem Permissão para editar este usuário.')#mensagem para o usuario
            return redirect(reverse_lazy("doctrainingapp:doctraining"))
        # messages.add_message(request, WARNING, 'Atualizar Usuário.')#mensagem para o usuario
        return super(UserUpdate, self).get(request, *args, **kwargs)



class UserCreate(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("doctrainingapp:doctraining")
    template_name = 'create_generico.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_staff:#Se não for administrador
            messages.add_message(request, ERROR, 'Você não tem Permissão para adicionar usuários.')#mensagem para o usuario
            return redirect(reverse_lazy("doctrainingapp:doctraining"))

        messages.add_message(request, WARNING, 'Novo Usuário do Tipo Professor/Profissional.')#mensagem para o usuario
        return super(UserCreate, self).get(request, *args, **kwargs)





class PerfilUpdate(UpdateView):
    model = Perfil
    success_url = reverse_lazy("doctrainingapp:doctraining")
    template_name = 'update_generico.html'
    fields = ['apelido','instituicao','idade']

    def get(self, request, *args, **kwargs):
        if (self.get_object().user.pk != self.request.user.pk):
            messages.add_message(request, ERROR, 'Você não tem Permissão para editar este perfil.')#mensagem para o usuario
            # return redirect('/doctraining/')
            return redirect(reverse_lazy("doctrainingapp:doctraining"))
        messages.add_message(request, WARNING, 'Atualizar Perfil.')#mensagem para o usuario
        return super(PerfilUpdate, self).get(request, *args, **kwargs)