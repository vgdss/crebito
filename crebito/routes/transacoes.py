from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crebito.database import get_db_session
from crebito.models import Cliente, Transacao
from crebito.schemas import RespostaTransacaoSchema, TransacaoSchema

router = APIRouter()


@router.post('/clientes/{cliente_id}/transacoes', status_code=status.HTTP_200_OK, response_model=RespostaTransacaoSchema)
async def criar_transacao(cliente_id: PositiveInt, transacao: TransacaoSchema, session: AsyncSession = Depends(get_db_session)):
    async with session.begin():
        # Busca o cliente e bloqueia para atualização
        cliente = await session.execute(select(Cliente).where(Cliente.id == cliente_id).with_for_update())
        cliente = cliente.scalars().first()

        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado!")

        # Atualiza o saldo do cliente com base no tipo de transação
        novo_saldo = cliente.saldo + transacao.valor if transacao.tipo == 'c' else cliente.saldo - transacao.valor
        # Verifica se a transacao de debito ultrapassa o limite do cliente
        if transacao.tipo == 'd' and (novo_saldo < -cliente.limite):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="A transacao ultrapassa o limite do cliente!")

        cliente.saldo = novo_saldo

        # Cria e adiciona a nova transação
        nova_transacao = Transacao(
            valor=transacao.valor, 
            tipo=transacao.tipo, 
            descricao=transacao.descricao, 
            id_cliente=cliente_id,
            realizada_em=datetime.utcnow()
        )

        session.add(nova_transacao)
        await session.commit()
    
    return RespostaTransacaoSchema(limite=cliente.limite, saldo=cliente.saldo)
