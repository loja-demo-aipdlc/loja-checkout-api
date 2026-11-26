FROM python:3.12-slim

# Lambda Web Adapter (extensão): no Lambda, repassa as requisições para o uvicorn na porta 8080. Fora do Lambda
# não faz nada, e a mesma imagem (mesmo digest) roda em docker, nos testes e no Lambda.
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    AWS_LWA_PORT=8080 AWS_LWA_READINESS_CHECK_PATH=/health
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
RUN useradd --uid 10001 --no-create-home app
USER app

EXPOSE 8080
CMD ["uvicorn", "checkout.app:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8080"]
