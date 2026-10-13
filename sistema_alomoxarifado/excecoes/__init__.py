"""Pacote de exceções personalizadas do sistema de almoxarifado."""

from excecoes.almoxarifado__error import (
    AlmoxarifadoError,
    FuncionarioJaCadastradoError,
    FuncionarioNaoEncontradoError,
    MaterialJaCadastradoError,
    MaterialNaoEncontradoError,
    EstoqueInsuficienteError,
    QuantidadeInvalidaError,
    PersistenciaError,
    ArquivoPersistenciaError,
    JsonInvalidoError,
    DadosIncompativeisError,
    RelacionamentoInvalidoError,
)

__all__ = [
    "AlmoxarifadoError",
    "FuncionarioJaCadastradoError",
    "FuncionarioNaoEncontradoError",
    "MaterialJaCadastradoError",
    "MaterialNaoEncontradoError",
    "EstoqueInsuficienteError",
    "QuantidadeInvalidaError",
    "PersistenciaError",
    "ArquivoPersistenciaError",
    "JsonInvalidoError",
    "DadosIncompativeisError",
    "RelacionamentoInvalidoError",
]
