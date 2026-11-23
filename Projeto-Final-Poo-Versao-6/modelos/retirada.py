"""Modelo ORM de retirada de material."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import CheckConstraint, DateTime, Numeric, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from modelos.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modelos.funcionario import Funcionario
    from modelos.material import Material

class Retirada(Base):
    __tablename__ = "retiradas"
    __table_args__ = (CheckConstraint("quantidade > 0", name="ck_retirada_quantidade"),)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    funcionario_id: Mapped[int] = mapped_column(ForeignKey("funcionarios.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    material_codigo: Mapped[str] = mapped_column(ForeignKey("materiais.codigo", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    quantidade: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    momento: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    observacao: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    funcionario: Mapped["Funcionario"] = relationship(back_populates="retiradas")
    material: Mapped["Material"] = relationship(back_populates="retiradas")
    def __str__(self):
        return (f"#{self.id} | {self.funcionario.nome} | {self.material.nome} | "
                f"{self.quantidade} {self.material.unidade_medida} | {self.momento:%d/%m/%Y %H:%M} | {self.observacao}")
