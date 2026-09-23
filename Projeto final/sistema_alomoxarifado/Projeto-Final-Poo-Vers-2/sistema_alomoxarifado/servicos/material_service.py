"""Serviço responsável pelas operações relacionadas a materiais."""

from typing import List, Optional

from almoxarifado import Almoxarifado
from modelos.material import Material
from excecoes.almoxarifado__error import (
    MaterialJaCadastradoError,
    MaterialNaoEncontradoError,
)


class MaterialService:
    """Coordena o cadastro, a busca, a listagem e a movimentação de estoque de materiais."""

    def __init__(self, almoxarifado: Almoxarifado) -> None:
        self.__almoxarifado = almoxarifado

    def cadastrar(self, codigo: str, nome: str, quantidade: float) -> Material:
        """
        Cadastra um novo material.

        Levanta MaterialJaCadastradoError caso já exista um material
        cadastrado com o mesmo código.
        """
        if self.buscar(codigo) is not None:
            raise MaterialJaCadastradoError(
                f"Já existe um material cadastrado com o código {codigo}."
            )

        material = Material(codigo, nome, quantidade)
        self.__almoxarifado.adicionar_material(material)
        return material

    def buscar(self, codigo: str) -> Optional[Material]:
        """Localiza um material pelo código. Retorna None caso não exista."""
        for material in self.__almoxarifado.materiais:
            if material.codigo == codigo:
                return material
        return None

    def consultar(self, codigo: str) -> Material:
        """
        Consulta um material pelo código.

        Levanta MaterialNaoEncontradoError caso não seja localizado.
        """
        material = self.buscar(codigo)
        if material is None:
            raise MaterialNaoEncontradoError(
                f"Material com código {codigo} não encontrado."
            )
        return material

    def listar(self) -> List[Material]:
        """Retorna a lista de todos os materiais cadastrados."""
        return self.__almoxarifado.materiais

    def adicionar_estoque(self, codigo: str, quantidade: float) -> Material:
        """Localiza um material e adiciona uma quantidade ao seu estoque."""
        material = self.consultar(codigo)
        material.adicionar_estoque(quantidade)
        return material
