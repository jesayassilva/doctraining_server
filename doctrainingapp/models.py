from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
from datetime import datetime
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save





class Doenca(models.Model):
    nome_doenca = models.CharField(max_length=100,unique=True)
    descricao = models.TextField(blank=True)
    def __str__(self):
        return str(self.nome_doenca)
    #funcao que faz com que os campos sejam Maiusculo automaticamente
    def save(self, force_insert=False, force_update=False):
        self.nome_doenca = self.nome_doenca.upper()
        super(Doenca, self).save(force_insert, force_update)


class Sintoma(models.Model):
    nome_sintoma = models.CharField(max_length=100,unique=True)
    #descricao = models.TextField(blank=True)
    def __str__(self):
        return str(self.nome_sintoma)
    #funcao que faz com que os campos sejam Maiusculo automaticamente
    def save(self, force_insert=False, force_update=False):
        self.nome_sintoma = self.nome_sintoma.upper()
        super(Sintoma, self).save(force_insert, force_update)

    def delete(self,force_insert=False, force_update=False):
        # sort instance collections
        if Caso_Clinico.objects.filter(pk = self.pk):
            raise ValidationError("Sintoma está ligado a doenças")
        else:
            super(Sintoma, self).delete(force_insert, force_update)



class Caso_Clinico(models.Model):
    doenca = models.ForeignKey(Doenca, on_delete=models.PROTECT, blank=True, null=True)
    sintomas = models.ManyToManyField(Sintoma, blank=False)
    doenca_classificada = models.BooleanField(default = True)

    def __str__(self):
        lista_sintomas = []
        for item in self.sintomas.all():
            lista_sintomas.append(item.nome_sintoma)
        if self.doenca_classificada:
            return 'Doença: ' + str(self.doenca)+', Sintomas:'+str(lista_sintomas)
        else:
            return 'Doença: Classificação Automática [' + str(self.doenca)+'], Sintomas:'+str(lista_sintomas)

    # def save(self, force_insert=False, force_update=False):
    #     if ( not self.doenca):
    #         self.doenca_classificada = False
    #     else:
    #         self.doenca_classificada = True
    #     super(Caso_Clinico, self).save(force_insert, force_update)




class Solicitacao_Alterar_Caso_Clinico(models.Model):
    caso_clinico_a_modificar = models.ForeignKey(Caso_Clinico, on_delete=models.CASCADE, blank=True, null=True)
    # caso_clinico_a_modificar = models.ForeignKey(Caso_Clinico, on_delete=models.PROTECT, blank=True, null=True)
    nova_doenca = models.ForeignKey(Doenca, on_delete=models.CASCADE, blank=True, null=True)
    novos_sintomas = models.ManyToManyField(Sintoma, blank=False)
    doenca_classificada = models.BooleanField(default = True)
    # solicitante = models.CharField(max_length=100,unique=True)
    tipo_alteracao = models.PositiveIntegerField()#0-DELETE; 1-CREATE; ou (2)-UPDATE
    acao = models.PositiveIntegerField(default= 2)#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
    data_solicitacao = models.DateTimeField(default=datetime.now)

    def __str__(self):
        lista_sintomas = []
        for item in self.novos_sintomas.all():
            lista_sintomas.append(item.nome_sintoma)
        if self.tipo_alteracao == 2:#Se editar
            if self.doenca_classificada:
                return 'ALTERAR DE '+str(self.caso_clinico_a_modificar) +' PARA Doença: ' + str(self.nova_doenca)+', Sintomas:'+str(lista_sintomas)
            else:
                return 'ALTERAR DE '+str(self.caso_clinico_a_modificar) +' PARA Doença: Classificação Automática [' + str(self.nova_doenca)+'], Sintomas:'+str(lista_sintomas)
        elif self.tipo_alteracao == 0:#se deletar
            return 'DELETAR: '+str(self.caso_clinico_a_modificar)
        else:#se for novo
            if self.doenca_classificada:
                return 'NOVO: Doença: ' + str(self.nova_doenca)+', Sintomas:'+str(lista_sintomas)
            else:
                return 'NOVO: Doença: Classificação Automática [' + str(self.nova_doenca)+'], Sintomas:'+str(lista_sintomas)


    def save(self, force_insert=False, force_update=False):
        if ( not self.nova_doenca):
            self.doenca_classificada = False
        else:
            self.doenca_classificada = True
        super(Solicitacao_Alterar_Caso_Clinico, self).save(force_insert, force_update)


    #As demais Def são usadas no template puxando os dadas formatados
    def solicitante_DEF(self):#Nome do usuario que solicitou a alteração
        return 'Fulano'

    def tipo_alteracao_DEF(self):#retorna nome da alteração
        if self.tipo_alteracao == 0:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'Deletar'
        elif self.tipo_alteracao == 1:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'Novo'
        else:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'Editar'

    def cor_DEF(self):#Cor usada na pagina de solicitações dos adm
        if self.tipo_alteracao == 0:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'red'
        elif self.tipo_alteracao == 1:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'green'
        else:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'yellow'

    def nome_doenca_antigo_DEF(self):#retorna nome da doenca antigo formatado, ou nome
        #0-DELETE; 1-CREATE; ou (2)-UPDATE
        if self.tipo_alteracao == 1:#se for novo não tem doenca antiga
            return '-'
        elif self.caso_clinico_a_modificar.doenca == None:#se doenca for nula retorna Classificação Automática[]
            return 'Classificação Automática[]'
        else:# se tiver doenca retorna o nome
            return self.caso_clinico_a_modificar.doenca

    def sintomas_antigo_DEF(self):
        #0-DELETE; 1-CREATE; ou (2)-UPDATE
        if self.tipo_alteracao == 1:#se for novo caso clinico não tem sintomas
            return '-'
        else:#se não for novo caso clinico
            lista_sintomas = ''#lista de sintomas string
            for item in self.caso_clinico_a_modificar.sintomas.all():#enquanto tiver sintoma em sintomas
                if item == self.caso_clinico_a_modificar.sintomas.last():#se o sintoma for o ultimo
                    lista_sintomas = lista_sintomas + item.nome_sintoma+'.'#adicinar com ponto final
                else:# se não for o ultimo
                    lista_sintomas = lista_sintomas + item.nome_sintoma+', '#adicionar com virgula
            return lista_sintomas

    def nome_doenca_novo_DEF(self):
        #0-DELETE; 1-CREATE; ou (2)-UPDATE
        if self.tipo_alteracao == 0:#se for deletar então não tem doenca nova
            return '-'
        elif self.nova_doenca == None:#se doenca for nula retorna Classificação Automática[]
            return 'Classificação Automática[]'
        else:# se tiver doenca retorna o nome
            return self.nova_doenca

    def sintomas_novos_DEF(self):
        #0-DELETE; 1-CREATE; ou (2)-UPDATE
        if self.tipo_alteracao == 0:#se for deletar caso clinico então não tem sintomas
            return '-'
        else:#se for editar ou novo caso clinico
            lista_sintomas = ''#lista de sintomas string
            for item in self.novos_sintomas.all():#enquanto tiver sintoma em sintomas
                if item == self.novos_sintomas.last():#se o sintoma for o ultimo
                    lista_sintomas = lista_sintomas + item.nome_sintoma+'.'#adicinar com ponto final
                else:# se não for o ultimo
                    lista_sintomas = lista_sintomas + item.nome_sintoma+', '#adicionar com virgula
            return lista_sintomas


    # def salvar_log(self,usuario):
    #     #----------------------------------Salvar aqui nessa linha na tabela de log------------------------------------------------
    #     log = Log()
    #     log.data_solicitacao = self.data_solicitacao
    #     log.solicitante = self.solicitante_DEF()
    #     #Antigos
    #     log.doenca = self.nome_doenca_antigo_DEF()
    #     log.sintomas = self.sintomas_antigo_DEF()
    #     #Novos
    #     log.nova_doenca = self.nome_doenca_novo_DEF()
    #     log.novos_sintomas = self.sintomas_novos_DEF()
    #
    #     log.doenca_classificada = self.doenca_classificada
    #     log.tipo_alteracao = self.tipo_alteracao#0-DELETE; 1-CREATE; ou (2)-UPDATE
    #     log.acao = self.acao#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
    #     log.avaliado_por = usuario.username
    #     log.save()

#alterar apenas o campo doença ou o campo sintoma
class Solicitacao_Alterar_Sintoma_Ou_Doenca(models.Model):
    sintoma_a_modificar = models.ForeignKey(Sintoma, on_delete=models.PROTECT, blank=True, null=True)
    nova_sintoma = models.CharField(max_length=100,blank=True, null=True)
    #OU
    doenca_a_modificar = models.ForeignKey(Doenca, on_delete=models.PROTECT, blank=True, null=True)
    nova_doenca = models.CharField(max_length=100,blank=True, null=True)

    # solicitante = models.CharField(max_length=100,unique=True)
    tipo_alteracao = models.PositiveIntegerField()#0-DELETE; 1-CREATE; ou (2)-UPDATE
    acao = models.PositiveIntegerField(default= 2)#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE

    def __str__(self):
        if (self.sintoma_a_modificar) or (self.nova_sintoma):
            if (self.tipo_alteracao == 0):
                return 'REMOVER SINTOMA: '+str(self.sintoma_a_modificar.nome_sintoma)
            elif (self.tipo_alteracao == 1):
                return 'NOVO SINTOMA: '+str(self.nova_sintoma)
            else:#(self.tipo_alteracao == 2:
                return 'EDITAR SINTOMA: '+str(self.sintoma_a_modificar.nome_sintoma)+ ' PARA: '+str(self.nova_sintoma)
        else:
            if (self.tipo_alteracao == 0):
                return 'REMOVER DOENÇA: '+str(self.doenca_a_modificar.nome_doenca)
            elif (self.tipo_alteracao == 1):
                return 'NOVO DOENÇA: '+str(self.nova_doenca)
            else:#(self.tipo_alteracao == 2:
                return 'EDITAR DOENÇA: '+str(self.doenca_a_modificar.nome_doenca)+ ' PARA: '+str(self.nova_doenca)

    def save(self, force_insert=False, force_update=False):
        if (self.nova_sintoma):
            self.nova_sintoma = self.nova_sintoma.upper()
        if (self.nova_doenca):
            self.nova_doenca = self.nova_doenca.upper()
        super(Solicitacao_Alterar_Sintoma_Ou_Doenca, self).save(force_insert, force_update)



class Log(models.Model):
    data_solicitacao = data_solicitacao = models.DateTimeField()
    solicitante = models.CharField(max_length=100,blank=False, null=False)
    #Antigos
    doenca = models.CharField(max_length=100,blank=False, null=False)
    sintomas = models.TextField(blank=True)
    #Novos
    nova_doenca = models.CharField(max_length=100,blank=False, null=False)
    novos_sintomas = models.TextField(blank=False)

    doenca_classificada = models.BooleanField(default = False)
    tipo_alteracao = models.PositiveIntegerField()#0-DELETE; 1-CREATE; ou (2)-UPDATE
    acao = models.PositiveIntegerField()#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE

    data_alteracao = models.DateTimeField(default=datetime.now)
    avaliado_por = models.CharField(max_length=100,blank=False, null=False)

    def __str__(self):
        return '{ "Data Solicitação": "'+ str(self.data_solicitacao)+'", '+ '"Solicitante": "'+ self.solicitante +'", '+'"Doenca": "' + self.doenca +'", '+'"Sintomas": "'+ self.sintomas +'", '+'"Nova doenca": "'+ self.nova_doenca +'", '+'"Novos sintomas": "'+ self.novos_sintomas +'", '+'"Doenca classificada": "'+ str(self.doenca_classificada) +'", '+'"Tipo alteracao": "'+ str(self.tipo_alteracao_DEF()) +'", '+'"Acao": "'+ str(self.acaoDEF()) +'", '+'"Data alteracao": "'+ str(self.data_alteracao) +'", '+'"Avaliado por": "'+ str(self.avaliado_por) +'" }'



    def tipo_alteracao_DEF(self):#retorna nome da alteração
        if self.tipo_alteracao == 0:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'Deletar'
        elif self.tipo_alteracao == 1:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'Novo'
        else:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'Editar'

    def cor_DEF(self):#Cor usada na pagina de solicitações dos adm
        if self.tipo_alteracao == 0:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'red'
        elif self.tipo_alteracao == 1:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'green'
        else:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'yellow'

    def acaoDEF(self):#retorna nome da alteração
        if self.acao == 0:#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            return 'RECUSADO'
        elif self.acao == 1:#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            return 'ACEITO'
        else:#0-RECUSADO; 1-ACEITO; ou (2)-PENDENTE
            return 'PENDENTE'

    def cor_acao_DEF(self):#Cor usada na pagina de solicitações dos adm
        if self.acao == 0:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'red'
        elif self.acao == 1:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'green'
        else:#0-DELETE; 1-CREATE; ou (2)-UPDATE
            return 'yellow'




class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100,null=True)
    apelido = models.CharField(max_length=100,null=True)
    instituicao = models.CharField(max_length=100,null=True)
    # curso = models.CharField(max_length=100, blank=True,null=True)
    idade = models.PositiveIntegerField(null=True)

    # email = models.EmailField(max_length=254,blank=True,null=True)
    def __str__(self):
        return self.user.username

#usar isso para criar automaticamente um perfil
@receiver(post_save, sender=User)
def create_user_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
#usar isso para criar automaticamente um perfil
@receiver(post_save, sender=User)
def save_user_perfil(sender, instance, **kwargs):
    instance.perfil.save()




class Sala(models.Model):
    responsavel_sala = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_sala = models.CharField(max_length=50, blank=False,null=False,unique=True)
    descricao = models.CharField(max_length=100, blank=True,null=True)
    data_criacao = models.DateTimeField(default=datetime.now)
    # email = models.EmailField(max_length=254,blank=True,null=True)
    def __str__(self):
        return self.nome_sala


class Pergunta(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    pergunta = models.TextField()
    opcao_correta = models.CharField(max_length=100)
    opcao_incorreta_1 = models.CharField(max_length=100)
    opcao_incorreta_2 = models.CharField(max_length=100)
    opcao_incorreta_3 = models.CharField(max_length=100)
    # email = models.EmailField(max_length=254,blank=True,null=True)
    def __str__(self):
        return self.pergunta











#
