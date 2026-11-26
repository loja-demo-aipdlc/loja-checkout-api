"""API HTTP da checkout. Só expõe o carrinho: a regra de preço continua em pricing/ (uow-loja-2026-0201).

Flags vêm do ambiente (CHECKOUT_FLAGS, separadas por vírgula) e, em produção, só mudam pelo plano de release
aprovado no G4 (CORE-20). Sem a variável, todas ficam desligadas.
"""
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .cart import Cart
from .pricing.discount import FLAGS


def flags_from_env():
    on = {f.strip() for f in os.environ.get('CHECKOUT_FLAGS', '').split(',') if f.strip()}
    return {name: name in on for name in FLAGS}


class ItemIn(BaseModel):
    sku: str
    unit_cents: int
    quantity: int = 1


class CartIn(BaseModel):
    customer_id: str
    items: list[ItemIn] = Field(default_factory=list)
    coupons: list[str] = Field(default_factory=list)
    first_purchase: bool = False


app = FastAPI(title='loja-checkout-api')


@app.get('/health')
def health():
    return {'status': 'ok', 'flags': flags_from_env()}


@app.post('/carrinho/total')
def total(body: CartIn):
    cart = Cart(body.customer_id)
    try:
        for i in body.items:
            cart.add(i.sku, i.unit_cents, i.quantity)
        total_cents = cart.total_cents(body.coupons, body.first_purchase, flags_from_env())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return {'subtotal_cents': cart.subtotal_cents(), 'total_cents': total_cents}
