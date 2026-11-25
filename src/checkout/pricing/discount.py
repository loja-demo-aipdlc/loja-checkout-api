"""Regra de desconto: hoje não há cupom ativo; o total é o subtotal."""


def apply_discounts(subtotal_cents, coupons=()):
    if coupons:
        raise ValueError(f'cupom desconhecido: {coupons[0]}')
    return subtotal_cents
