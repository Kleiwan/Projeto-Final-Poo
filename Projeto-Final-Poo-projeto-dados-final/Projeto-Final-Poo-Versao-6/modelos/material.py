"""Modelo ORM de material."""
from decimal import Decimal
from sqlalchemy import Boolean, CheckConstraint, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from excecoes.almoxarifado__error import (
    EstoqueInsuficienteError, MaterialBloqueadoError, MaterialJaBloqueadoError,
    MaterialNaoBloqueadoError, QuantidadeInvalidaError
)
from modelos.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modelos.retirada import Retirada
    from modelos.entrada import Entrada

class Material(Base):
    __tablename__ = "materiais"
    __table_args__ = (
        CheckConstraint("quantidade >= 0", name="ck_material_quantidade"),
        CheckConstraint("estoque_inicial >= 0", name="ck_material_estoque_inicial"),
        CheckConstraint("estoque_minimo >= 0", name="ck_material_estoque_minimo"),
    )
    codigo: Mapped[str] = mapped_column(String(50), primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    quantidade: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    estoque_inicial: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0, server_default=text("0"))
    bloqueado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("0"))
    motivo_bloqueio: Mapped[str] = mapped_column(String(255), nullable=False, default="", server_default="")
    categoria: Mapped[str] = mapped_column(String(80), nullable=False, default="Geral", server_default="Geral")
    unidade_medida: Mapped[str] = mapped_column(String(20), nullable=False, default="unidade", server_default="unidade")
    estoque_minimo: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0, server_default=text("0"))
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=text("1"))
    retiradas: Mapped[list["Retirada"]] = relationship(back_populates="material")
    entradas: Mapped[list["Entrada"]] = relationship(back_populates="material")

    def bloquear(self, motivo):
        if self.bloqueado:
            raise MaterialJaBloqueadoError(f"O material '{self.nome}' já está bloqueado.")
        motivo = motivo.strip()
        if not motivo:
            raise ValueError("O motivo do bloqueio não pode ficar vazio.")
        self.bloqueado, self.motivo_bloqueio = True, motivo

    def desbloquear(self):
        if not self.bloqueado:
            raise MaterialNaoBloqueadoError(f"O material '{self.nome}' não está bloqueado.")
        self.bloqueado, self.motivo_bloqueio = False, ""

    def adicionar_estoque(self, quantidade):
        quantidade = Decimal(str(quantidade))
        if quantidade <= 0:
            raise QuantidadeInvalidaError("A quantidade deve ser maior que zero.")
        self.quantidade += quantidade

    def retirar_estoque(self, quantidade):
        quantidade = Decimal(str(quantidade))
        if self.bloqueado:
            raise MaterialBloqueadoError(f"Material bloqueado: {self.motivo_bloqueio}")
        if not self.ativo:
            raise ValueError("Material inativo não pode ser movimentado.")
        if quantidade <= 0:
            raise QuantidadeInvalidaError("A quantidade deve ser maior que zero.")
        if quantidade > self.quantidade:
            raise EstoqueInsuficienteError("Quantidade solicitada superior ao estoque disponível.")
        self.quantidade -= quantidade

    def printar(self):
        situacao = "Bloqueado" if self.bloqueado else "Desbloqueado"
        print(f"Código: {self.codigo} | Nome: {self.nome} | Categoria: {self.categoria} | "
              f"Estoque: {self.quantidade} {self.unidade_medida} | Mínimo: {self.estoque_minimo} | "
              f"{situacao} | {'Ativo' if self.ativo else 'Inativo'}")
