"""Modelo ORM de material."""

from sqlalchemy import Boolean, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from excecoes.almoxarifado__error import (
    EstoqueInsuficienteError,
    MaterialBloqueadoError,
    MaterialJaBloqueadoError,
    MaterialNaoBloqueadoError,
    QuantidadeInvalidaError,
)
from modelos.base import Base


class Material(Base):
    """
    Material do almoxarifado (tabela ``materiais``).

    Controla o próprio estoque e a situação de bloqueio.
    """

    __tablename__ = "materiais"

    codigo: Mapped[str] = mapped_column(String(50), primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    quantidade: Mapped[float] = mapped_column(Float)
    bloqueado: Mapped[bool] = mapped_column(Boolean, default=False)
    motivo_bloqueio: Mapped[str] = mapped_column(String(255), default="")

    retiradas: Mapped[list["Retirada"]] = relationship(
        back_populates="material"
    )

    def bloquear(self, motivo: str) -> None:
        """Bloqueia o material e registra o motivo."""
        if self.bloqueado:
            raise MaterialJaBloqueadoError(
                f"O material '{self.nome}' já está bloqueado."
            )
        motivo = motivo.strip()
        if not motivo:
            raise ValueError("O motivo do bloqueio não pode ficar vazio.")
        self.bloqueado = True
        self.motivo_bloqueio = motivo

    def desbloquear(self) -> None:
        """Desbloqueia um material anteriormente bloqueado."""
        if not self.bloqueado:
            raise MaterialNaoBloqueadoError(
                f"O material '{self.nome}' não está bloqueado."
            )
        self.bloqueado = False
        self.motivo_bloqueio = ""

    def adicionar_estoque(self, quantidade: float) -> None:
        """Adiciona uma quantidade positiva ao estoque."""
        if quantidade <= 0:
            raise QuantidadeInvalidaError("A quantidade a ser adicionada deve ser maior que zero.")
        self.quantidade += quantidade

    def retirar_estoque(self, quantidade: float) -> None:
        """Retira uma quantidade do estoque respeitando as regras de negócio."""
        if self.bloqueado:
            raise MaterialBloqueadoError(
                f"Retirada recusada: o material '{self.nome}' está bloqueado. "
                f"Motivo: {self.motivo_bloqueio}"
            )
        if quantidade <= 0:
            raise QuantidadeInvalidaError("A quantidade a ser retirada deve ser maior que zero.")
        if quantidade > self.quantidade:
            raise EstoqueInsuficienteError("Quantidade solicitada superior ao estoque disponível.")
        self.quantidade -= quantidade

    def printar(self) -> None:
        """Exibe os dados do material no console."""
        situacao = "Bloqueado" if self.bloqueado else "Desbloqueado"
        detalhe = f" | Motivo: {self.motivo_bloqueio}" if self.bloqueado else ""
        print(
            f"Código: {self.codigo} | Nome: {self.nome} | "
            f"Quantidade: {self.quantidade} | Situação: {situacao}{detalhe}"
        )
