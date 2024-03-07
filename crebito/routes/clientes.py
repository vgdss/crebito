from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from crebito.database import get_db_session
from crebito.models import Cliente, Transacao
from crebito.schemas import ExtratoSchema, Saldo, TransacaoExtratoSchema


router = APIRouter()

@router.get("/clientes/{cliente_id}/extrato", status_code=status.HTTP_200_OK, response_model=ExtratoSchema)
async def get_extrato(cliente_id: PositiveInt, session: AsyncSession = Depends(get_db_session)):
    # Consulta o cliente pelo ID de forma assíncrona
    cliente = await session.get(Cliente, cliente_id, with_for_update=True)

    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado!")

    ultimas_transacoes = await session.execute(
        select(
            Transacao
        ).where(Transacao.cliente_id == cliente_id)
        .order_by(desc(Transacao.id))
        .limit(10)
    )
    
    return ExtratoSchema.model_construct(
        saldo = Saldo.model_construct(total=cliente.saldo, limite=cliente.limite),
        ultimas_transacoes=[
            TransacaoExtratoSchema.model_construct(
                valor=t.valor,
                tipo=t.tipo,
                descricao=t.descricao,
                realizada_em=t.realizada_em
            ) for t in ultimas_transacoes.scalars().all()
        ]
    )