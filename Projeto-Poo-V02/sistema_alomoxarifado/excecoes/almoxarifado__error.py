"""
Exceções personalizadas do sistema de almoxarifado.

Todas as situações que representam violações das regras de negócio
(cadastros duplicados, registros inexistentes, estoque insuficiente,
quantidades inválidas etc.) devem ser comunicadas através destas
exceções, e não por meio de simples prints/return.
"""


class AlmoxarifadoError(Exception):
    """Classe base para todas as exceções de regras de negócio do almoxarifado."""


class FuncionarioJaCadastradoError(AlmoxarifadoError):
    """Levantada ao tentar cadastrar um funcionário com um ID já existente."""


class FuncionarioNaoEncontradoError(AlmoxarifadoError):
    """Levantada quando um funcionário não é localizado pelo ID informado."""


class MaterialJaCadastradoError(AlmoxarifadoError):
    """Levantada ao tentar cadastrar um material com um código já existente."""


class MaterialNaoEncontradoError(AlmoxarifadoError):
    """Levantada quando um material não é localizado pelo código informado."""


class EstoqueInsuficienteError(AlmoxarifadoError):
    """Levantada quando a quantidade retirada é maior que o estoque disponível."""


class QuantidadeInvalidaError(AlmoxarifadoError):
    """Levantada quando é informada uma quantidade menor ou igual a zero."""
