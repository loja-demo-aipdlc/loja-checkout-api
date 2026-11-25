"""Regra de desconto. O cupom de primeira compra fica atrás da flag cupom-primeira-compra (uow-loja-2026-0201)."""

# Desligada em produção; liga só pelo plano de release (G4)
FLAGS = {'cupom-primeira-compra': False}
FIRST_PURCHASE = 'PRIMEIRA10'


def apply_discounts(subtotal_cents, coupons=(), first_purchase=False, flags=None):
    flags = FLAGS if flags is None else flags
    coupons = list(coupons)
    if not coupons:
        return subtotal_cents
    if len(coupons) > 1:
        raise ValueError('cupons não acumulam')
    code = coupons[0]
    if code == FIRST_PURCHASE and flags.get('cupom-primeira-compra'):
        if not first_purchase:
            raise ValueError('cupom de primeira compra só vale para quem não comprou antes')
        return subtotal_cents - subtotal_cents * 10 // 100
    raise ValueError(f'cupom desconhecido: {code}')
