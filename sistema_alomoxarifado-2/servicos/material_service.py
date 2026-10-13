"""Serviço responsável pelas operações relacionadas a materiais."""

from typing import List, Optional

from almoxarifado import Almoxarifado
from modelos.fornecedor import Fornecedor
from modelos.material import Material
from servicos.fornecedor_service import FornecedorService
from excecoes.almoxarifado__error import (
    MaterialComRetiradasError,
    MaterialJaCadastradoError,
    MaterialNaoEncontradoError,
)


class MaterialService:
    """Coordena o cadastro, a busca, a edição, a remoção e a movimentação de estoque de materiais."""

    def __init__(
        self,
        almoxarifado: Almoxarifado,
        fornecedor_service: FornecedorService,
    ) -> None:
        self.__almoxarifado = almoxarifado
        self.__fornecedor_service = fornecedor_service

    def cadastrar(
        self,
        codigo: str,
        nome: str,
        quantidade: float,
        id_fornecedor: Optional[int] = None,
    ) -> Material:
        """
        Cadastra um novo material, opcionalmente vinculado a um fornecedor.

        Levanta MaterialJaCadastradoError caso já exista um material
        com o mesmo código e FornecedorNaoEncontradoError caso o
        fornecedor informado não exista.
        """
        if self.buscar(codigo) is not None:
            raise MaterialJaCadastradoError(
                f"Já existe um material cadastrado com o código {codigo}."
            )

        fornecedor: Optional[Fornecedor] = None
        if id_fornecedor is not None:
            fornecedor = self.__fornecedor_service.consultar(id_fornecedor)

        material = Material(codigo, nome, quantidade, fornecedor)
        self.__almoxarifado.adicionar_material(material)
        self.__almoxarifado.salvar_materiais()
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
        self.__almoxarifado.salvar_materiais()
        return material

    def editar(
        self,
        codigo: str,
        nome: Optional[str] = None,
        id_fornecedor: Optional[int] = None,
        desvincular_fornecedor: bool = False,
    ) -> Material:
        """
        Altera o nome e/ou o fornecedor de um material.

        Parâmetros None mantêm o valor atual; ``desvincular_fornecedor``
        remove o vínculo com o fornecedor. O código não pode ser alterado.
        Levanta MaterialNaoEncontradoError ou FornecedorNaoEncontradoError.
        """
        material = self.consultar(codigo)

        fornecedor: Optional[Fornecedor] = material.fornecedor
        if desvincular_fornecedor:
            fornecedor = None
        elif id_fornecedor is not None:
            fornecedor = self.__fornecedor_service.consultar(id_fornecedor)

        material.atualizar(nome if nome is not None else material.nome, fornecedor)
        self.__almoxarifado.salvar_materiais()
        return material

    def remover(self, codigo: str) -> None:
        """
        Remove um material.

        Levanta MaterialNaoEncontradoError caso não exista e
        MaterialComRetiradasError caso ele possua retiradas registradas.
        """
        material = self.consultar(codigo)

        if any(
            retirada.material.codigo == codigo
            for retirada in self.__almoxarifado.retiradas
        ):
            raise MaterialComRetiradasError(
                f"O material {codigo} possui retiradas registradas e não pode ser removido."
            )

        self.__almoxarifado.remover_material(material)
        self.__almoxarifado.salvar_materiais()
