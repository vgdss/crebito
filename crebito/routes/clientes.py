from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from crebito.database import get_db_session
from crebito.models import Cliente, Transacao
from crebito.schemas import ExtratoSchema, Saldo


router = APIRouter()

@router.get("/clientes/{cliente_id}/extrato", status_code=status.HTTP_200_OK, response_model=ExtratoSchema)
async def get_extrato(cliente_id: PositiveInt, session: AsyncSession = Depends(get_db_session)):
    # Consulta o cliente pelo ID de forma assíncrona
    cliente = await session.get(Cliente, cliente_id, with_for_update=True)

    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado!")

    # Consulta as 10 últimas transações do cliente de forma assíncrona
    ultimas_transacoes = await session.execute(
        select(
            Transacao.valor,
            Transacao.tipo,
            Transacao.descricao,
            Transacao.realizada_em
        ).where(Transacao.cliente_id == cliente_id)
        .order_by(desc(Transacao.realizada_em))
        .limit(10)
    )
    
    # Monta o extrato completo
    return ExtratoSchema(
        saldo = Saldo(total=cliente.saldo, limite=cliente.limite), 
        ultimas_transacoes = ultimas_transacoes.mappings().all(),
    )