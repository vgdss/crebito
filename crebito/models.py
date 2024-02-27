from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, desc, Index
from sqlalchemy.orm import relationship

from datetime import datetime

from database import Base


class Transacao(Base):
    __tablename__ = "transacoes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)
    descricao = Column(String(10), nullable=False)
    realizada_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False, index=True)
    cliente = relationship("Cliente", back_populates="transacoes")

    __table_args__ = (
        Index('idx_transacoes_id_cliente_realizada_em', id_cliente, desc(realizada_em)),
    )


class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    limite = Column(Integer, nullable=False)
    saldo = Column(Integer, nullable=False, default=0)
    transacoes = relationship("Transacao", back_populates="cliente")
