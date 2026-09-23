"""
Camada de aplicação do sistema de almoxarifado.
"""

from typing import List

from modelos.funcionario import Funcionario
from modelos.material import Material
from modelos.retirada import Retirada


class Almoxarifado:
    """
    Mantém os dados do sistema em memória.

    A classe principal não implementa mais regras de negócio: ela apenas
    guarda as coleções de funcionários, materiais e retiradas e fornece
    acesso controlado a elas para a camada de serviços.
    """

    def __init__(self) -> None:
        self.__funcionarios: List[Funcionario] = []
        self.__materiais: List[Material] = []
        self.__retiradas: List[Retirada] = []

    @property
    def funcionarios(self) -> List[Funcionario]:
        """Retorna uma cópia da lista de funcionários cadastrados."""
        return list(self.__funcionarios)

    def adicionar_funcionario(self, funcionario: Funcionario) -> None:
        """Adiciona um funcionário à coleção mantida em memória."""
        self.__funcionarios.append(funcionario)

    @property
    def materiais(self) -> List[Material]:
        """Retorna uma cópia da lista de materiais cadastrados."""
        return list(self.__materiais)

    def adicionar_material(self, material: Material) -> None:
        """Adiciona um material à coleção mantida em memória."""
        self.__materiais.append(material)

    @property
    def retiradas(self) -> List[Retirada]:
        """Retorna uma cópia da lista de retiradas registradas."""
        return list(self.__retiradas)

    def adicionar_retirada(self, retirada: Retirada) -> None:
        """Adiciona uma retirada à coleção mantida em memória."""
        self.__retiradas.append(retirada)
