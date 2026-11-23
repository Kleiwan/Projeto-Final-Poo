"""Serviço responsável pelas operações relacionadas a materiais."""
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from excecoes.almoxarifado__error import (
    MaterialJaCadastradoError,
    MaterialNaoEncontradoError,
    RemocaoNaoPermitidaError,
)
from modelos.material import Material
from modelos.retirada import Retirada
from modelos.entrada import Entrada


class MaterialService:
    """Coordena cadastro, busca, listagem, estoque, bloqueio e remoção de materiais."""

    def __init__(self, sessao: Session) -> None:
        self.__sessao = sessao

    def cadastrar(self, codigo: str, nome: str, quantidade: float,
                  categoria: str = "Geral", unidade_medida: str = "unidade",
                  estoque_minimo: float = 0) -> Material:
        """
        Cadastra um novo material.

        Levanta ValueError se a quantidade inicial for menor ou igual a zero e
        MaterialJaCadastradoError se o código já existir.
        """
        if quantidade <= 0:
            raise ValueError("A quantidade inicial do material deve ser maior que zero.")
        if estoque_minimo < 0:
            raise ValueError("O estoque mínimo não pode ser negativo.")
        if not nome.strip() or not categoria.strip() or not unidade_medida.strip():
            raise ValueError("Nome, categoria e unidade de medida são obrigatórios.")

        if self.buscar(codigo) is not None:
            raise MaterialJaCadastradoError(
                f"Já existe um material cadastrado com o código {codigo}."
            )

        saldo_inicial = Decimal(str(quantidade))
        material = Material(
            codigo=codigo.strip(), nome=nome.strip(), quantidade=saldo_inicial,
            estoque_inicial=saldo_inicial, categoria=categoria.strip(),
            unidade_medida=unidade_medida.strip(),
            estoque_minimo=Decimal(str(estoque_minimo))
        )

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


    def editar(self, codigo: str, nome: str, categoria: str = "Geral",
               unidade_medida: str = "unidade", estoque_minimo: float = 0) -> Material:
        """Atualiza dados cadastrais; não altera saldo nem histórico."""
        material = self.consultar(codigo)
        nome, categoria, unidade_medida = nome.strip(), categoria.strip(), unidade_medida.strip()
        if not nome or not categoria or not unidade_medida:
            raise ValueError("Nome, categoria e unidade de medida são obrigatórios.")
        if estoque_minimo < 0:
            raise ValueError("O estoque mínimo não pode ser negativo.")
        try:
            material.nome = nome
            material.categoria = categoria
            material.unidade_medida = unidade_medida
            material.estoque_minimo = Decimal(str(estoque_minimo))
            self.__sessao.commit()
            return material
        except Exception:
            self.__sessao.rollback()
            raise

    def alterar_situacao(self, codigo: str, ativo: bool) -> Material:
        material = self.consultar(codigo)
        try:
            material.ativo = bool(ativo)
            self.__sessao.commit()
            return material
        except Exception:
            self.__sessao.rollback()
            raise

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
        tem_retirada = self.__sessao.scalars(comando).first() is not None
        tem_entrada = self.__sessao.scalars(
            select(Entrada.id).where(Entrada.material_codigo == material.codigo)
        ).first() is not None
        if tem_retirada or tem_entrada:
            raise RemocaoNaoPermitidaError(
                f"O material '{material.nome}' (código {material.codigo}) "
                "possui movimentações e não pode ser removido."
            )

        try:
            self.__sessao.delete(material)
            self.__sessao.commit()
        except Exception:
            self.__sessao.rollback()
            raise
