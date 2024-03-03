from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt, parse_obj_as
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crebito.database import get_db_session
from crebito.models import Cliente, Transacao
from crebito.schemas import ExtratoSchema, Saldo, TransacaoExtratoSchema

router = APIRouter()


'''
@router.get("/clientes/{cliente_id}/extrato", status_code=status.HTTP_200_OK, response_model=ExtratoSchema)
async def get_extrato(cliente_id: PositiveInt, session: AsyncSession = Depends(get_db_session)):
    # Consulta o cliente pelo ID de forma assíncrona
    cliente = await session.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente = cliente.scalars().first()

    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado!")

    # Consulta as 10 últimas transações do cliente de forma assíncrona
    ultimas_transacoes = await session.execute(
        select(
            Transacao.valor,
            Transacao.tipo,
            Transacao.descricao,
            Transacao.realizada_em
        ).where(Transacao.id_cliente == cliente_id)
        .order_by(desc(Transacao.realizada_em))
        .limit(10)
    )

    ultimas_transacoes = ultimas_transacoes.mappings().all()
    # Monta a lista de transações para o Pydantic Schema
    ultimas_transacoes = parse_obj_as(list[TransacaoExtratoSchema], ultimas_transacoes)
    # Monta o Saldo
    saldo = Saldo(total=cliente.saldo, limite=cliente.limite)
    
    # Monta o extrato completo
    return ExtratoSchema(saldo=saldo, ultimas_transacoes=ultimas_transacoes)
'''


@router.get("/clientes/{cliente_id}/extrato", status_code=status.HTTP_200_OK, response_model=ExtratoSchema)
async def get_extrato(cliente_id: PositiveInt, session: AsyncSession = Depends(get_db_session)):
    # Consulta as 10 últimas transações do cliente E os dados do cliente em uma única consulta
    resultado = await session.execute(
        select(
            Cliente, 
            Transacao
        ).outerjoin(Transacao, Cliente.id == Transacao.id_cliente)
         .where(Cliente.id == cliente_id)
         .order_by(desc(Transacao.realizada_em))
         .limit(10)
    )

    resultado = resultado.all()

    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado!")

    # A primeira transação contém o objeto do cliente, extraia-o
    cliente = resultado[0][0]

    # Processa o resultado para extrair apenas os dados das transações
    ultimas_transacoes = [
        TransacaoExtratoSchema(
            valor=t.valor, 
            tipo=t.tipo, 
            descricao=t.descricao, 
            realizada_em=t.realizada_em
        ) for cliente, t in resultado if t
    ]

    # Monta o Saldo
    saldo = Saldo(total=cliente.saldo, limite=cliente.limite)
    
    # Monta o extrato completo
    return ExtratoSchema(saldo=saldo, ultimas_transacoes=ultimas_transacoes)
