"""Pacote de exceções personalizadas do sistema de almoxarifado."""

from excecoes.almoxarifado__error import (
    AlmoxarifadoError,
    FuncionarioJaCadastradoError,
    FuncionarioNaoEncontradoError,
    MaterialJaCadastradoError,
    MaterialNaoEncontradoError,
    MaterialBloqueadoError,
    MaterialJaBloqueadoError,
    MaterialNaoBloqueadoError,
    EstoqueInsuficienteError,
    QuantidadeInvalidaError,
    FuncionarioSemPermissaoError,
    RemocaoNaoPermitidaError,
)

__all__ = [
    "AlmoxarifadoError",
    "FuncionarioJaCadastradoError",
    "FuncionarioNaoEncontradoError",
    "MaterialJaCadastradoError",
    "MaterialNaoEncontradoError",
    "MaterialBloqueadoError",
    "MaterialJaBloqueadoError",
    "MaterialNaoBloqueadoError",
    "EstoqueInsuficienteError",
    "QuantidadeInvalidaError",
    "FuncionarioSemPermissaoError",
    "RemocaoNaoPermitidaError",
]
