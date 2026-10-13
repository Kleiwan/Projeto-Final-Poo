from datetime import datetime
from typing import Optional

from modelos.funcionario import Funcionario
from modelos.material import Material


class Retirada:
    """
    Representa a retirada de uma quantidade de determinado material
    por um funcionário, em um determinado momento.

    Cada retirada possui um identificador próprio (``id``), necessário
    para que ela possa ser persistida e reconstruída posteriormente.
    """

    def __init__(
        self,
        id: int,
        funcionario: Funcionario,
        material: Material,
        quantidade: float,
        momento: Optional[datetime] = None,
    ) -> None:
        self.__id = id
        self.__funcionario = funcionario
        self.__material = material
        self.__quantidade = quantidade
        self.__momento = momento if momento is not None else datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def funcionario(self) -> Funcionario:
        return self.__funcionario

    @property
    def material(self) -> Material:
        return self.__material

    @property
    def quantidade(self) -> float:
        return self.__quantidade

    @property
    def momento(self) -> datetime:
        return self.__momento

    def __str__(self) -> str:
        return (
            f"Funcionário: {self.funcionario.nome} | "
            f"Material: {self.material.nome} | "
            f"Quantidade: {self.quantidade} | "
            f"Momento: {self.momento.strftime('%d/%m/%Y %H:%M:%S')}"
        )
