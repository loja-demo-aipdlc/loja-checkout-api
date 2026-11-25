"""Critérios de cupom.feature (uow-loja-2026-0201), com a flag ligada e desligada."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from checkout.cart import Cart  # noqa: E402

ON = {'cupom-primeira-compra': True}


def cart_100():
    c = Cart('c-1')
    c.add('sku-1', 10000)
    return c


class CupomPrimeiraCompra(unittest.TestCase):
    def test_primeira_compra_recebe_10_por_cento(self):
        self.assertEqual(cart_100().total_cents(['PRIMEIRA10'], first_purchase=True, flags=ON), 9000)

    def test_cupom_nao_vale_para_quem_ja_comprou(self):
        with self.assertRaises(ValueError):
            cart_100().total_cents(['PRIMEIRA10'], first_purchase=False, flags=ON)

    def test_cupom_nao_acumula(self):
        with self.assertRaises(ValueError):
            cart_100().total_cents(['PRIMEIRA10', 'OUTRO'], first_purchase=True, flags=ON)

    def test_com_a_flag_desligada_o_cupom_nao_existe(self):
        with self.assertRaises(ValueError):
            cart_100().total_cents(['PRIMEIRA10'], first_purchase=True)


if __name__ == '__main__':
    unittest.main()
