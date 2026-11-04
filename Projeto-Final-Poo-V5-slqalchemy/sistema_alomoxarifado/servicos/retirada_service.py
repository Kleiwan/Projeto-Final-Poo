"""Serviço responsável por coordenar o registro e a consulta de retiradas."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from excecoes.almoxarifado__error import (
    FuncionarioNaoEncontradoError,
    FuncionarioSemPermissaoError,
    MaterialNaoEncontradoError,
    QuantidadeInvalidaError,
)
from modelos.funcionario import Funcionario
from modelos.material import Material
from modelos.retirada import Retirada


class RetiradaService:
    """
    Coordena a operação de retirada de materiais.

    Verifica as condições (quantidade válida, funcionário autorizado,
    material desbloqueado e estoque disponível) e, se tudo estiver
    correto, atualiza o estoque e registra a retirada no mesmo ``commit``.
    """

    def __init__(self, sessao: Session) -> None:
        self.__sessao = sessao

    def registrar(self, id_funcionario: int, codigo_material: str, quantidade: float) -> Retirada:
        """
        Registra a retirada de uma quantidade de material por um funcionário.

        Levanta FuncionarioNaoEncontradoError, FuncionarioSemPermissaoError,
        MaterialNaoEncontradoError, MaterialBloqueadoError,
        QuantidadeInvalidaError ou EstoqueInsuficienteError, conforme o caso.
        """
        if quantidade <= 0:
            raise QuantidadeInvalidaError("A quantidade retirada deve ser maior que zero.")

        funcionario = self.__sessao.get(Funcionario, id_funcionario)
        if funcionario is None:
            raise FuncionarioNaoEncontradoError(
                f"Funcionário com ID {id_funcionario} não encontrado."
            )

        # A permissão é verificada antes de qualquer alteração de estoque.
        if not funcionario.pode_retirar:
            raise FuncionarioSemPermissaoError(
                f"O funcionário {funcionario.nome} (ID {funcionario.id}) não tem "
                f"permissão para retirar materiais."
            )

        material = self.consultar_material(codigo_material)

        try:
            material.retirar_estoque(quantidade)
            retirada = Retirada(
                funcionario=funcionario,
                material=material,
                quantidade=quantidade,
            )
            self.__sessao.add(retirada)
            self.__sessao.commit()
            self.__sessao.refresh(retirada)
        except Exception:
            self.__sessao.rollback()
            raise

        return retirada

    def listar(self) -> list[Retirada]:
        """Retorna todas as retiradas registradas."""
        comando = select(Retirada).order_by(Retirada.id)
        return list(self.__sessao.scalars(comando).all())

    def consultar_por_funcionario(self, id_funcionario: int) -> list[Retirada]:
        """Retorna as retiradas realizadas por um funcionário."""
        comando = (
            select(Retirada)
            .where(Retirada.funcionario_id == id_funcionario)
            .order_by(Retirada.id)
        )
        return list(self.__sessao.scalars(comando).all())

    def consultar_por_material(self, codigo_material: str) -> list[Retirada]:
        """Retorna as retiradas realizadas de um material."""
        comando = (
            select(Retirada)
            .where(Retirada.material_codigo == codigo_material)
            .order_by(Retirada.id)
        )
        return list(self.__sessao.scalars(comando).all())

    def consultar_material(self, codigo_material: str) -> Material:
        """
        Retorna o material para consultar estoque e situação.

        Levanta MaterialNaoEncontradoError se não for localizado.
        """
        material = self.__sessao.get(Material, codigo_material)
        if material is None:
            raise MaterialNaoEncontradoError(
                f"Material com código {codigo_material} não encontrado."
            )
        return material

    def consultar_estoque(self, codigo_material: str) -> float:
        """Retorna a quantidade em estoque de um material."""
        return self.consultar_material(codigo_material).quantidade
