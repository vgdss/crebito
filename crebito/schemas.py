from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class RespostaTransacaoSchema(BaseModel):
    limite: PositiveInt
    saldo: int = 0


class TransacaoSchema(BaseModel):
    valor: PositiveInt
    tipo: Literal["c", "d"]
    descricao: str = Field(min_length=1, max_length=10)


class TransacaoExtratoSchema(TransacaoSchema):
    model_config = ConfigDict(extra='ignore')
    realizada_em: datetime


class Saldo(BaseModel):
    total: int
    limite: PositiveInt
    data_extrato: Optional[datetime] = Field(default_factory=datetime.utcnow)


class ExtratoSchema(BaseModel):
    saldo: Saldo
    ultimas_transacoes: list[TransacaoExtratoSchema] = []