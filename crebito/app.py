import logging

from fastapi import FastAPI

from crebito.routes import clientes, transacoes

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Crebito",
    version="0.1.0",
    description="Rinha de Backend - 2024/Q1",
)

app.include_router(clientes.router)
app.include_router(transacoes.router)
