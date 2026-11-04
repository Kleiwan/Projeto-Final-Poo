"""Serviço responsável pelas operações relacionadas a funcionários."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from excecoes.almoxarifado__error import (
    FuncionarioJaCadastradoError,
    FuncionarioNaoEncontradoError,
    RemocaoNaoPermitidaError,
)
from modelos.funcionario import Funcionario
from modelos.retirada import Retirada


class FuncionarioService:
    """Coordena cadastro, busca, listagem, permissão e remoção de funcionários."""

    def __init__(self, sessao: Session) -> None:
        self.__sessao = sessao

    def cadastrar(self, nome: str, id_funcionario: int, setor: str) -> Funcionario:
        """
        Cadastra um novo funcionário.

        Levanta FuncionarioJaCadastradoError se o ID já existir.
        """
        if self.buscar(id_funcionario) is not None:
            raise FuncionarioJaCadastradoError(
                f"Já existe um funcionário cadastrado com o ID {id_funcionario}."
            )

        funcionario = Funcionario(id=id_funcionario, nome=nome, setor=setor)

        try:
            self.__sessao.add(funcionario)
            self.__sessao.commit()
            self.__sessao.refresh(funcionario)
        except Exception:
            self.__sessao.rollback()
            raise

        return funcionario

    def buscar(self, id_funcionario: int) -> Funcionario | None:
        """Localiza um funcionário pelo ID. Retorna None se não existir."""
        return self.__sessao.get(Funcionario, id_funcionario)

    def consultar(self, id_funcionario: int) -> Funcionario:
        """
        Consulta um funcionário pelo ID.

        Levanta FuncionarioNaoEncontradoError se não for localizado.
        """
        funcionario = self.buscar(id_funcionario)
        if funcionario is None:
            raise FuncionarioNaoEncontradoError(
                f"Funcionário com ID {id_funcionario} não encontrado."
            )
        return funcionario

    def listar(self) -> list[Funcionario]:
        """Retorna todos os funcionários cadastrados."""
        comando = select(Funcionario).order_by(Funcionario.id)
        return list(self.__sessao.scalars(comando).all())

    def conceder_permissao(self, id_funcionario: int) -> Funcionario:
        """Autoriza um funcionário a retirar materiais e grava a alteração."""
        funcionario = self.consultar(id_funcionario)

        try:
            funcionario.conceder_permissao()
            self.__sessao.commit()
        except Exception:
            self.__sessao.rollback()
            raise

        return funcionario

    def retirar_permissao(self, id_funcionario: int) -> Funcionario:
        """
        Remove a autorização de retirada de um funcionário.

        O cadastro e as retiradas já registradas são preservados.
        """
        funcionario = self.consultar(id_funcionario)

        try:
            funcionario.retirar_permissao()
            self.__sessao.commit()
        except Exception:
            self.__sessao.rollback()
            raise

        return funcionario

    def remover(self, id_funcionario: int) -> None:
        """
        Remove o cadastro de um funcionário.

        Levanta RemocaoNaoPermitidaError se ele já possuir retiradas
        (o histórico é preservado).
        """
        funcionario = self.consultar(id_funcionario)

        comando = select(Retirada.id).where(
            Retirada.funcionario_id == funcionario.id
        )
        if self.__sessao.scalars(comando).first() is not None:
            raise RemocaoNaoPermitidaError(
                f"O funcionário {funcionario.nome} (ID {funcionario.id}) possui "
                f"retiradas registradas e não pode ser removido."
            )

        try:
            self.__sessao.delete(funcionario)
            self.__sessao.commit()
        except Exception:
            self.__sessao.rollback()
            raise
