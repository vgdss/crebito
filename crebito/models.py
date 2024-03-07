from datetime import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Index, Integer, String,
                        desc)
from sqlalchemy.orm import Mapped

from .database import Base


class Transacao(Base):
    __tablename__ = "transacoes"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    valor: Mapped[int] = Column(Integer, nullable=False)
    tipo: Mapped[str] = Column(String, nullable=False)
    descricao: Mapped[str] = Column(String(10), nullable=False)
    realizada_em: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    cliente_id: Mapped[int] = Column(Integer, ForeignKey('clientes.id'), nullable=False)

    __table_args__ = (
        Index('idx_transacoes_cliente_id_id_desc', cliente_id, desc(id)),
    )    


class Cliente(Base):
    __tablename__ = "clientes"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    limite: Mapped[int] = Column(Integer, nullable=False)
    saldo: Mapped[int] = Column(Integer, nullable=False, default=0)
