from fastapi import APIRouter, HTTPException
from pydantic import ValidationError, PositiveInt
from sqlalchemy.exc import NoResultFound

from crebito.repository import processar_transacao, ViolacaoLimiteError
from crebito.schemas import RespostaClienteTransacaoSchema, TransacaoSchema

router = APIRouter()


@router.post('/clientes/{cliente_id}/transacoes', status_code=200, response_model=RespostaClienteTransacaoSchema)
async def criar_transacao(cliente_id: PositiveInt, transacao: TransacaoSchema):
    try:
        return await processar_transacao(cliente_id, transacao)
    except ViolacaoLimiteError:
        raise HTTPException(status_code=422, detail="A transacao ultrapassa o limite do cliente!")
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Cliente não encontrado!")
    except ValidationError:
        raise HTTPException(status_code=400, detail="Dados de entrada inválidos")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao processar a transação")