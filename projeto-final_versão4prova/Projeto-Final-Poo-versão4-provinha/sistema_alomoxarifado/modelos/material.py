from excecoes.almoxarifado__error import (
    EstoqueInsuficienteError,
    QuantidadeInvalidaError,
    MaterialBloqueadoError,
    MaterialJaBloqueadoError,
    MaterialNaoBloqueadoError,
)


class Material:
    """Representa um material e controla estoque e situação de bloqueio."""

    def __init__(
        self,
        codigo: str,
        nome: str,
        quantidade: float,
        bloqueado: bool = False,
        motivo_bloqueio: str = "",
    ) -> None:
        self.__codigo = codigo
        self.__nome = nome
        self.__quantidade = quantidade
        self.__bloqueado = bloqueado
        self.__motivo_bloqueio = motivo_bloqueio

    @property
    def codigo(self) -> str:
        return self.__codigo

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def quantidade(self) -> float:
        return self.__quantidade

    @property
    def bloqueado(self) -> bool:
        return self.__bloqueado

    @property
    def motivo_bloqueio(self) -> str:
        return self.__motivo_bloqueio

    def bloquear(self, motivo: str) -> None:
        """Bloqueia o material e registra o motivo."""
        if self.__bloqueado:
            raise MaterialJaBloqueadoError(
                f"O material '{self.nome}' já está bloqueado."
            )
        motivo = motivo.strip()
        if not motivo:
            raise ValueError("O motivo do bloqueio não pode ficar vazio.")
        self.__bloqueado = True
        self.__motivo_bloqueio = motivo

    def desbloquear(self) -> None:
        """Desbloqueia um material anteriormente bloqueado."""
        if not self.__bloqueado:
            raise MaterialNaoBloqueadoError(
                f"O material '{self.nome}' não está bloqueado."
            )
        self.__bloqueado = False
        self.__motivo_bloqueio = ""

    def adicionar_estoque(self, quantidade: float) -> None:
        if quantidade <= 0:
            raise QuantidadeInvalidaError("A quantidade a ser adicionada deve ser maior que zero.")
        self.__quantidade += quantidade

    def retirar_estoque(self, quantidade: float) -> None:
        if self.__bloqueado:
            raise MaterialBloqueadoError(
                f"Retirada recusada: o material '{self.nome}' está bloqueado. "
                f"Motivo: {self.__motivo_bloqueio}"
            )
        if quantidade <= 0:
            raise QuantidadeInvalidaError("A quantidade a ser retirada deve ser maior que zero.")
        if quantidade > self.__quantidade:
            raise EstoqueInsuficienteError("Quantidade solicitada superior ao estoque disponível.")
        self.__quantidade -= quantidade

    def printar(self) -> None:
        situacao = "Bloqueado" if self.bloqueado else "Desbloqueado"
        detalhe = f" | Motivo: {self.motivo_bloqueio}" if self.bloqueado else ""
        print(
            f"Código: {self.codigo} | Nome: {self.nome} | "
            f"Quantidade: {self.quantidade} | Situação: {situacao}{detalhe}"
        )
