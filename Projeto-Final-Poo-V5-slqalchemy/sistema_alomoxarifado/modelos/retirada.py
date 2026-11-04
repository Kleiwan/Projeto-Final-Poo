"""Modelo ORM de retirada."""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from modelos.base import Base


class Retirada(Base):
    """
    Retirada de uma quantidade de material por um funcionário
    (tabela ``retiradas``).

    Possui duas chaves estrangeiras (``funcionario_id`` e
    ``material_codigo``) e os relacionamentos ``funcionario`` e ``material``.
    """

    __tablename__ = "retiradas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    funcionario_id: Mapped[int] = mapped_column(ForeignKey("funcionarios.id"))
    material_codigo: Mapped[str] = mapped_column(ForeignKey("materiais.codigo"))
    quantidade: Mapped[float] = mapped_column(Float)
    momento: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    funcionario: Mapped["Funcionario"] = relationship(back_populates="retiradas")
    material: Mapped["Material"] = relationship(back_populates="retiradas")

    def __str__(self) -> str:
        return (
            f"Funcionário: {self.funcionario.nome} | "
            f"Material: {self.material.nome} | "
            f"Quantidade: {self.quantidade} | "
            f"Momento: {self.momento.strftime('%d/%m/%Y %H:%M:%S')}"
        )
