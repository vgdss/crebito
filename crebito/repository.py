from datetime import datetime

from sqlalchemy import desc, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from .database import SessionLocal
from .models import Cliente, Transacao
from .schemas import (ExtratoSchema, RespostaClienteTransacaoSchema, Saldo,
                      TransacaoExtratoSchema, TransacaoSchema)


class ViolacaoLimiteError(Exception):
    pass


async def processar_transacao(cliente_id: int, transacao: TransacaoSchema) -> RespostaClienteTransacaoSchema:
    async with SessionLocal() as session:
        async with session.begin():
            # Busca o cliente e bloqueia para atualização
            stmt = select(Cliente).where(Cliente.id == cliente_id).with_for_update()
            result = await session.execute(stmt)
            cliente = result.scalars().first()

            if not cliente:
                raise NoResultFound(f"Cliente com ID {cliente_id} não encontrado.")

            # Atualiza o saldo do cliente com base no tipo de transação
            novo_saldo = cliente.saldo + transacao.valor if transacao.tipo == 'c' else cliente.saldo - transacao.valor
            
            if novo_saldo < -cliente.limite:
                raise ViolacaoLimiteError('Transação excede o limite de crédito do cliente.')

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
        
        return RespostaClienteTransacaoSchema(limite=cliente.limite, saldo=cliente.saldo)


async def obter_extrato_raw(cliente_id: int):
    async with SessionLocal() as session:
        # Busca o cliente
        stmt = select(Cliente)\
            .options(joinedload(Cliente.transacoes))\
            .where(Cliente.id == cliente_id)        
        
        result = await session.execute(stmt)
        cliente = result.scalars().first()

        if not cliente:
            raise NoResultFound(f"Cliente com ID {cliente_id} não encontrado.")
    
        # Estruturando o retorno conforme solicitado
        retorno = {
            "saldo": {
                "total": cliente.saldo,
                "data_extrato": datetime.now().isoformat(),
                "limite": cliente.limite,
            },
            "ultimas_transacoes": [
                {
                    "valor": transacao.valor,
                    "tipo": transacao.tipo,
                    "descricao": transacao.descricao,
                    "realizada_em": transacao.realizada_em
                } for transacao in cliente.transacoes[:10]
            ]
        }

        return retorno


async def obter_extrato(cliente_id: int) -> ExtratoSchema:
    async with SessionLocal() as session:
        # Consulta o cliente pelo ID de forma assíncrona
        resultado_cliente = await session.execute(select(Cliente).where(Cliente.id == cliente_id))
        cliente = resultado_cliente.scalars().first()

        if not cliente:
            raise NoResultFound(f"Cliente com ID {cliente_id} não encontrado.")

        # Consulta as 10 últimas transações do cliente de forma assíncrona
        resultado_transacoes = await session.execute(
            select(Transacao)
            .where(Transacao.id_cliente == cliente_id)
            .order_by(desc(Transacao.realizada_em))
            .limit(10)
        )

        transacoes = resultado_transacoes.scalars().all()
        saldo = Saldo(total = cliente.saldo, limite = cliente.limite)

        # Monta a lista de transações para o Pydantic Schema
        transacoes_schema = [TransacaoExtratoSchema(
            valor=t.valor,
            tipo=t.tipo,
            descricao=t.descricao,
            realizada_em=t.realizada_em
        ) for t in transacoes]

        # Monta o extrato completo
        extrato = ExtratoSchema(
            saldo = saldo,
            ultimas_transacoes = transacoes_schema
        )

        return extrato
