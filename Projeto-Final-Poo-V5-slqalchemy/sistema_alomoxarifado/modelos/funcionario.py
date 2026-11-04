"""Modelo ORM de funcionário."""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from modelos.base import Base


class Funcionario(Base):
    """
    Funcionário do almoxarifado (tabela ``funcionarios``).

    Sabe se está autorizado a retirar materiais e é responsável por
    alterar essa permissão.
    """

    __tablename__ = "funcionarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    nome: Mapped[str] = mapped_column(String(100))
    setor: Mapped[str] = mapped_column(String(100))
    pode_retirar: Mapped[bool] = mapped_column(Boolean, default=True)

    retiradas: Mapped[list["Retirada"]] = relationship(
        back_populates="funcionario"
    )

    def conceder_permissao(self) -> None:
        """Autoriza o funcionário a retirar materiais."""
        self.pode_retirar = True

    def retirar_permissao(self) -> None:
        """Remove a autorização do funcionário para retirar materiais."""
        self.pode_retirar = False

    def printar(self) -> None:
        """Exibe os dados do funcionário no console."""
        situacao = "AUTORIZADO" if self.pode_retirar else "NAO AUTORIZADO"
        print(
            f"Nome: {self.nome} | ID: {self.id} | Setor: {self.setor} "
            f"| Permissao de retirada: {situacao}"
        )
