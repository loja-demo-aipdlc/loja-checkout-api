# loja-checkout-api

API de carrinho e preço da Loja Demo, um varejo fictício. Código de demonstração.

```bash
python3 -m unittest discover -s tests -t .
```

Todo PR pertence a uma UoW: o id vai no nome do branch (`uow-loja-2026-0201/cupom`) ou no trailer
`Correlation-Id` dos commits. Commits feitos com agente levam o trailer `Agent-Session`.

## Testes do cupom

`python3 -m unittest discover -s tests -t .` roda os testes, inclusive os do cupom.

## Build e verificação

No merge para a main, `.github/workflows/build.yml` chama o builder confiável da organização
(`aipdlc-checks`), que publica `ghcr.io/loja-demo-aipdlc/loja-checkout-api@sha256:...` com proveniência
assinada. Os testes rodam sobre a imagem publicada, e o motor do AI-PDLC publica o check `aipdlc-artefato` no
commit: o commit de origem lido da proveniência entrou por PR com o check `aipdlc` aprovado.

```bash
docker run --rm -p 8080:8080 ghcr.io/loja-demo-aipdlc/loja-checkout-api@sha256:...
curl localhost:8080/health
```
