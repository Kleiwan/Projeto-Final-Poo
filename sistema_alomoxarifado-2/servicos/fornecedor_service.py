"""Serviço responsável pelas operações relacionadas a fornecedores."""

from typing import List, Optional

from almoxarifado import Almoxarifado
from modelos.fornecedor import Fornecedor
from excecoes.almoxarifado__error import (
    FornecedorComMateriaisError,
    FornecedorJaCadastradoError,
    FornecedorNaoEncontradoError,
)


class FornecedorService:
    """Coordena o cadastro, a consulta, a edição e a remoção de fornecedores."""

    def __init__(self, almoxarifado: Almoxarifado) -> None:
        self.__almoxarifado = almoxarifado

    def cadastrar(self, id_fornecedor: int, nome: str, contato: str) -> Fornecedor:
        """
        Cadastra um novo fornecedor.

        Levanta FornecedorJaCadastradoError caso o ID já exista.
        """
        if self.buscar(id_fornecedor) is not None:
            raise FornecedorJaCadastradoError(
                f"Já existe um fornecedor cadastrado com o ID {id_fornecedor}."
            )

        fornecedor = Fornecedor(id_fornecedor, nome, contato)
        self.__almoxarifado.adicionar_fornecedor(fornecedor)
        self.__almoxarifado.salvar_fornecedores()
        return fornecedor

    def buscar(self, id_fornecedor: int) -> Optional[Fornecedor]:
        """Localiza um fornecedor pelo ID. Retorna None caso não exista."""
        for fornecedor in self.__almoxarifado.fornecedores:
            if fornecedor.id == id_fornecedor:
                return fornecedor
        return None

    def consultar(self, id_fornecedor: int) -> Fornecedor:
        """
        Consulta um fornecedor pelo ID.

        Levanta FornecedorNaoEncontradoError caso não seja localizado.
        """
        fornecedor = self.buscar(id_fornecedor)
        if fornecedor is None:
            raise FornecedorNaoEncontradoError(
                f"Fornecedor com ID {id_fornecedor} não encontrado."
            )
        return fornecedor

    def listar(self) -> List[Fornecedor]:
        """Retorna a lista de todos os fornecedores cadastrados."""
        return self.__almoxarifado.fornecedores

    def editar(
        self,
        id_fornecedor: int,
        nome: Optional[str] = None,
        contato: Optional[str] = None,
    ) -> Fornecedor:
        """
        Altera o nome e/ou o contato de um fornecedor.

        Parâmetros None mantêm o valor atual. Levanta
        FornecedorNaoEncontradoError caso o ID não exista.
        """
        fornecedor = self.consultar(id_fornecedor)
        fornecedor.atualizar(
            nome if nome is not None else fornecedor.nome,
            contato if contato is not None else fornecedor.contato,
        )
        self.__almoxarifado.salvar_fornecedores()
        return fornecedor

    def remover(self, id_fornecedor: int) -> None:
        """
        Remove um fornecedor.

        Levanta FornecedorNaoEncontradoError caso não exista e
        FornecedorComMateriaisError caso ainda haja materiais vinculados
        a ele (para que nenhum material fique apontando para um
        fornecedor inexistente).
        """
        fornecedor = self.consultar(id_fornecedor)

        if any(
            material.fornecedor is not None and material.fornecedor.id == id_fornecedor
            for material in self.__almoxarifado.materiais
        ):
            raise FornecedorComMateriaisError(
                f"O fornecedor {id_fornecedor} possui materiais vinculados e não pode ser removido."
            )

        self.__almoxarifado.remover_fornecedor(fornecedor)
        self.__almoxarifado.salvar_fornecedores()
