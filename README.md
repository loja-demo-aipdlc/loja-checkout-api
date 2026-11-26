# loja-checkout-api

API de carrinho e preço da Loja Demo, um varejo fictício. Código de demonstração.

```bash
python3 -m unittest discover -s tests -t .
```

Todo PR pertence a uma UoW: o id vai no nome do branch (`uow-loja-2026-0201/cupom`) ou no trailer
`Correlation-Id` dos commits. Commits feitos com agente levam o trailer `Agent-Session`.

## Testes do cupom

`python3 -m unittest discover -s tests -t .` roda os testes, inclusive os do cupom.
