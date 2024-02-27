from fastapi import APIRouter, HTTPException
from pydantic import ValidationError, PositiveInt
from sqlalchemy.exc import NoResultFound

from crebito.repository import obter_extrato
from crebito.schemas import ExtratoSchema

router = APIRouter()


@router.get("/clientes/{cliente_id}/extrato", status_code=200, response_model=ExtratoSchema)
async def get_extrato(cliente_id: PositiveInt):
    try:
        return await obter_extrato(cliente_id=cliente_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Cliente não encontrado!")
    except ValidationError:
        raise HTTPException(status_code=400, detail="Dados de entrada inválidos")
    except Exception as e:
        print('EXTRATO', e)
        #logger.exception("[EXTRATO] [500] [ERRO AO PROCESSAR O EXTRATO]")
        raise HTTPException(status_code=500, detail="Erro ao processar a transação")