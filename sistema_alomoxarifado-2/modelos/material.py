from typing import Optional

from excecoes.almoxarifado__error import EstoqueInsuficienteError, QuantidadeInvalidaError
from modelos.fornecedor import Fornecedor


class Material:
    """
    Representa um material do almoxarifado.

    O modelo é responsável por controlar sua própria quantidade em
    estoque, garantindo que ela nunca fique negativa e que apenas
    quantidades válidas sejam movimentadas.
    """

    def __init__(
        self,
        codigo: str,
        nome: str,
        quantidade: float,
        fornecedor: Optional[Fornecedor] = None,
    ) -> None:
        self.__codigo = codigo
        self.__nome = nome
        self.__quantidade = quantidade
        self.__fornecedor: Optional[Fornecedor] = fornecedor

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
    def fornecedor(self) -> Optional[Fornecedor]:
        """Fornecedor do material, ou None quando não há fornecedor vinculado."""
        return self.__fornecedor

    def atualizar(self, nome: str, fornecedor: Optional[Fornecedor]) -> None:
        """Altera o nome e o fornecedor do material (o código nunca muda)."""
        self.__nome = nome
        self.__fornecedor = fornecedor

    def adicionar_estoque(self, quantidade: float) -> None:
        """Aumenta a quantidade em estoque do material."""
        if quantidade <= 0:
            raise QuantidadeInvalidaError(
                "A quantidade a ser adicionada deve ser maior que zero."
            )
        self.__quantidade += quantidade

    def retirar_estoque(self, quantidade: float) -> None:
        """
        Diminui a quantidade em estoque do material.

        Levanta EstoqueInsuficienteError caso a quantidade solicitada
        seja maior do que a quantidade disponível.
        """
        if quantidade <= 0:
            raise QuantidadeInvalidaError(
                "A quantidade a ser retirada deve ser maior que zero."
            )
        if quantidade > self.__quantidade:
            raise EstoqueInsuficienteError(
                "Quantidade solicitada superior ao estoque disponível."
            )
        self.__quantidade -= quantidade

    def printar(self) -> None:
        """Exibe os dados do material formatados no console."""
        fornecedor = self.fornecedor.nome if self.fornecedor is not None else "-"
        print(
            f"Código: {self.codigo} | Nome: {self.nome} | "
            f"Quantidade: {self.quantidade} | Fornecedor: {fornecedor}"
        )
