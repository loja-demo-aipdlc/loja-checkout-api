"""Carrinho: itens e total, em centavos."""
from dataclasses import dataclass, field

from .pricing.discount import apply_discounts


@dataclass
class Item:
    sku: str
    unit_cents: int
    quantity: int = 1


@dataclass
class Cart:
    customer_id: str
    items: list[Item] = field(default_factory=list)

    def add(self, sku, unit_cents, quantity=1):
        if unit_cents < 0 or quantity < 1:
            raise ValueError('preço negativo ou quantidade menor que 1')
        self.items.append(Item(sku, unit_cents, quantity))

    def subtotal_cents(self):
        return sum(i.unit_cents * i.quantity for i in self.items)

    def total_cents(self, coupons=()):
        return apply_discounts(self.subtotal_cents(), coupons)
