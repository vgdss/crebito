from contextlib import asynccontextmanager

# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from fastapi import FastAPI

from sqlalchemy import delete, update

from crebito.routes import clientes, transacoes
from .database import async_session
from .models import Cliente, Transacao
from .schemas import TransacaoSchema


# # Configurar o provedor de tracer
# trace.set_tracer_provider(TracerProvider())

# # Configurar o exportador OTLP
# otlp_exporter = OTLPSpanExporter(endpoint="0.0.0.0:4317", insecure=True)

# # Adicionar o processador de span ao provedor de tracer
# trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session() as session:
        for _ in range(25):
            await transacoes.criar_transacao(
                cliente_id=1, 
                session=session,
                transacao=TransacaoSchema(
                    valor=1, tipo='c', descricao='credito!!')
            )
        
        for _ in range(25):
            await transacoes.criar_transacao(
                cliente_id=1,
                session=session,
                transacao=TransacaoSchema(
                    valor=1, tipo='d', descricao='debito!!'),
            )
        
        for _ in range(50):
            await clientes.get_extrato(cliente_id=1, session=session)

        # Limpeza retornando ao estado padrao
        await session.execute(delete(Transacao))
        await session.execute(update(Cliente).values(saldo=0))
        await session.commit()
    yield # Após essa linha, a aplicação está pronta para servir requisições


app = FastAPI(
    title="Crebito",
    version="0.1.0",
    description="Rinha de Backend - 2024/Q1",
    lifespan=lifespan # WARMUP
)

# # Instrumentar FastAPI
# FastAPIInstrumentor.instrument_app(app)

app.include_router(clientes.router)
app.include_router(transacoes.router)
