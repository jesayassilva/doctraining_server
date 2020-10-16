from django.test import TestCase
import requests

URL = 'http://les.ufersa.edu.br/doctraining/api'

def test_todas_salas():
    r = requests.get(URL+'/salas')

    for object in r.json():
        assert (type(object['id']) == int and
                type(object['sala_nome']) == str and
                type(object['quantidade_perguntas']) == int)

    assert r.status_code == 200, 'STATUS CODE DIFERENTE DE 200'


def test_salas_por_area():
    r = requests.get(URL + '/area/salas')

    for object in r.json():
        assert (type(object['id']) == int and type(object['area_nome']) == str)
        for sala in object['salas_list']:
            assert (type(sala['id']) == int and
                    type(sala['sala_nome']) == str and
                    type(sala['quantidade_perguntas']) == int)

    assert r.status_code == 200, 'STATUS CODE DIFERENTE DE 200'


def test_perguntas_sala():
    r = requests.get(URL + '/salas/7/perguntas')

    for object in r.json():
        assert (type(object['id']) == int and
                type(object['difficulty']) == int and
                type(object['rightOp']) == str and
                type(object['wrongOp01']) == str and
                type(object['wrongOp02']) == str and
                type(object['wrongOp03']) == str )
        for imagem in object['imageList']:
            assert (type(imagem['image1']) == str and
                    type(imagem['image2']) == str and
                    type(imagem['image3']) == str )

    assert r.status_code == 200, 'STATUS CODE DIFERENTE DE 200'