import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from checkout.cart import Cart  # noqa: E402


class CartTest(unittest.TestCase):
    def test_total_sem_cupom_e_o_subtotal(self):
        cart = Cart('c-1')
        cart.add('sku-1', 1990, 2)
        cart.add('sku-2', 500)
        self.assertEqual(cart.total_cents(), 4480)

    def test_rejeita_quantidade_invalida(self):
        with self.assertRaises(ValueError):
            Cart('c-1').add('sku-1', 100, 0)

    def test_cupom_desconhecido(self):
        cart = Cart('c-1')
        cart.add('sku-1', 1000)
        with self.assertRaises(ValueError):
            cart.total_cents(coupons=['NAOEXISTE'])


if __name__ == '__main__':
    unittest.main()
