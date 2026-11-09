"""Serviço responsável pelas operações relacionadas a materiais."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from excecoes.almoxarifado__error import (
    MaterialJaCadastradoError,
    MaterialNaoEncontradoError,
    RemocaoNaoPermitidaError,
)
from modelos.material import Material
from modelos.retirada import Retirada


class MaterialService:
    """Coordena cadastro, busca, listagem, estoque, bloqueio e remoção de materiais."""

    def __init__(self, sessao: Session) -> None:
        self.__sessao = sessao

    def cadastrar(self, codigo: str, nome: str, quantidade: float) -> Material:
        """
        Cadastra um novo material.

        Levanta ValueError se a quantidade inicial for menor ou igual a zero e
        MaterialJaCadastradoError se o código já existir.
        """
        if quantidade <= 0:
            raise ValueError(
                "A quantidade inicial do material deve ser maior que zero."
            )

        if self.buscar(codigo) is not None:
            raise MaterialJaCadastradoError(
                f"Já existe um material cadastrado com o código {codigo}."
            )

        material = Material(codigo=codigo, nome=nome, quantidade=quantidade)

        try:
            self.__sessao.add(material)
            self.__sessao.commit()
            self.__sessao.refresh(material)
        except Exception:
            self.__sessao.rollback()
            raise

        return material

    def buscar(self, codigo: str) -> Material | None:
        """Localiza um material pelo código. Retorna None se não existir."""
        return self.__sessao.get(Material, codigo)

    def consultar(self, codigo: str) -> Material:
        """
        Consulta um material pelo código.

        Levanta MaterialNaoEncontradoError se não for localizado.
        """
        material = self.buscar(codigo)
        if material is None:
            raise MaterialNaoEncontradoError(
                f"Material com código {codigo} não encontrado."
            )
        return material

    def listar(self) -> list[Material]:
        """Retorna todos os materiais cadastrados."""
        comando = select(Material).order_by(Material.codigo)
        return list(self.__sessao.scalars(comando).all())

    def bloquear(self, codigo: str, motivo: str) -> Material:
        """Bloqueia um material e persiste a situação e o motivo."""
        material = self.consultar(codigo)

        try:
            material.bloquear(motivo)
            self.__sessao.commit()
        except Exception:
            self.__sessao.rollback()
            raise

        return material

    def desbloquear(self, codigo: str) -> Material:
        """Desbloqueia um material e persiste a nova situação."""
        material = self.consultar(codigo)

        try:
            material.desbloquear()
            self.__sessao.commit()
        except Exception:
            self.__sessao.rollback()
            raise

        return material

    def adicionar_estoque(self, codigo: str, quantidade: float) -> Material:
        """Adiciona uma quantidade ao estoque de um material."""
        material = self.consultar(codigo)

        try:
            material.adicionar_estoque(quantidade)
            self.__sessao.commit()
        except Exception:
            self.__sessao.rollback()
            raise

        return material

    def remover(self, codigo: str) -> None:
        """
        Remove o cadastro de um material.

        Levanta RemocaoNaoPermitidaError se ele já constar em retiradas
        (o histórico é preservado).
        """
        material = self.consultar(codigo)

        comando = select(Retirada.id).where(
            Retirada.material_codigo == material.codigo
        )
        if self.__sessao.scalars(comando).first() is not None:
            raise RemocaoNaoPermitidaError(
                f"O material '{material.nome}' (código {material.codigo}) "
                f"consta em retiradas e não pode ser removido."
            )

        try:
            self.__sessao.delete(material)
            self.__sessao.commit()
        except Exception:
            self.__sessao.rollback()
            raise
