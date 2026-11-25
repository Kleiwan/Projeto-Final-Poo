"""Modelo ORM de funcionário."""
from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from modelos.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modelos.retirada import Retirada
    from modelos.entrada import Entrada
    
class Funcionario(Base):
    """Funcionário que pode solicitar movimentações do almoxarifado."""
    __tablename__ = "funcionarios"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    setor: Mapped[str] = mapped_column(String(120), nullable=False)
    pode_retirar: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=text("1"))
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=text("1"))
    data_cadastro: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    retiradas: Mapped[list["Retirada"]] = relationship(back_populates="funcionario")
    entradas: Mapped[list["Entrada"]] = relationship(back_populates="funcionario")
    def conceder_permissao(self): self.pode_retirar = True
    def retirar_permissao(self): self.pode_retirar = False
    def printar(self):
        print(f"Nome: {self.nome} | ID: {self.id} | Setor: {self.setor} | "
              f"Permissão: {'AUTORIZADO' if self.pode_retirar else 'NÃO AUTORIZADO'} | "
              f"Situação: {'ATIVO' if self.ativo else 'INATIVO'}")
