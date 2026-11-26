"""Testes da API sobre o artefato publicado: rodam contra a imagem em execução (CHECKOUT_URL).

O workflow de build sobe a imagem pelo digest e roda estes testes de fora dela, sem escrita no registro
(CORE-14, CORE-35). Sem CHECKOUT_URL, ficam de fora.
"""
import json
import os
import unittest
import urllib.error
import urllib.request

URL = os.environ.get('CHECKOUT_URL')


def call(path, body=None):
    req = urllib.request.Request(URL + path, method='POST' if body is not None else 'GET',
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, json.load(e)


@unittest.skipUnless(URL, 'CHECKOUT_URL não definido: testes da imagem em execução')
class Api(unittest.TestCase):
    def test_health_com_a_flag_do_cupom_desligada(self):
        status, body = call('/health')
        self.assertEqual(status, 200)
        self.assertEqual(body['flags'], {'cupom-primeira-compra': False})

    def test_total_sem_cupom(self):
        status, body = call('/carrinho/total', {'customer_id': 'c-1', 'items': [
            {'sku': 'sku-1', 'unit_cents': 1990, 'quantity': 2}, {'sku': 'sku-2', 'unit_cents': 500}]})
        self.assertEqual((status, body['total_cents']), (200, 4480))

    def test_cupom_de_primeira_compra_nao_existe_com_a_flag_desligada(self):
        status, _ = call('/carrinho/total', {'customer_id': 'c-1', 'coupons': ['PRIMEIRA10'], 'first_purchase': True,
                                             'items': [{'sku': 'sku-1', 'unit_cents': 10000}]})
        self.assertEqual(status, 422)


if __name__ == '__main__':
    unittest.main()
