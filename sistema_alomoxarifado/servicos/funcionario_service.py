"""Serviço responsável pelas operações relacionadas a funcionários."""

from typing import List, Optional

from almoxarifado import Almoxarifado
from modelos.funcionario import Funcionario
from excecoes.almoxarifado__error import (
    FuncionarioJaCadastradoError,
    FuncionarioNaoEncontradoError,
)


class FuncionarioService:
    """Coordena o cadastro, a busca e a listagem de funcionários."""

    def __init__(self, almoxarifado: Almoxarifado) -> None:
        self.__almoxarifado = almoxarifado

    def cadastrar(self, nome: str, id_funcionario: int, setor: str) -> Funcionario:
        """
        Cadastra um novo funcionário.

        Levanta FuncionarioJaCadastradoError caso já exista um
        funcionário cadastrado com o mesmo ID.
        """
        if self.buscar(id_funcionario) is not None:
            raise FuncionarioJaCadastradoError(
                f"Já existe um funcionário cadastrado com o ID {id_funcionario}."
            )

        funcionario = Funcionario(nome, id_funcionario, setor)
        self.__almoxarifado.adicionar_funcionario(funcionario)
        return funcionario

    def buscar(self, id_funcionario: int) -> Optional[Funcionario]:
        """Localiza um funcionário pelo ID. Retorna None caso não exista."""
        for funcionario in self.__almoxarifado.funcionarios:
            if funcionario.id == id_funcionario:
                return funcionario
        return None

    def consultar(self, id_funcionario: int) -> Funcionario:
        """
        Consulta um funcionário pelo ID.

        Levanta FuncionarioNaoEncontradoError caso não seja localizado.
        """
        funcionario = self.buscar(id_funcionario)
        if funcionario is None:
            raise FuncionarioNaoEncontradoError(
                f"Funcionário com ID {id_funcionario} não encontrado."
            )
        return funcionario

    def listar(self) -> List[Funcionario]:
        """Retorna a lista de todos os funcionários cadastrados."""
        return self.__almoxarifado.funcionarios
