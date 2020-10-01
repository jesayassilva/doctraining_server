from doctrainingapp.views import *
import firebase_admin
from firebase_admin import credentials, db
from collections import OrderedDict

def data_firebase(request):
    usuario = request.user#usuario logado
    try:
        if not firebase_admin._apps:#credenciamento
            cred = credentials.Certificate("doctraining-cbc4a-firebase-adminsdk-4p4wy-8d1d68b114.json")#carrega credencial
            firebase_admin.initialize_app(cred, {'databaseURL': 'https://doctraining-cbc4a.firebaseio.com/'})#inicializa credencial
        ref = db.reference('/usuarios')#busca o banco
        snapshot = ref.order_by_key().get()#ordena pelo usuarios id do firebase
        return render(request,'data_firebase.html',{'snapshot': snapshot,'usuario':usuario})
    except Exception as e:
        mandar_email_error(str(e),usuario,request.resolver_match.url_name)
        messages.add_message(request, ERROR, 'Ocorreu um erro. Tente novamente mais tarde.')#mensagem para o usuario
        # return redirect('/doctraining/')
        return redirect(reverse_lazy('doctrainingapp:doctraining'))