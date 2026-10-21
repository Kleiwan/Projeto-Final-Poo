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




class MaterialBloqueadoError(AlmoxarifadoError):
    """Levantada quando se tenta retirar um material bloqueado."""


class MaterialJaBloqueadoError(AlmoxarifadoError):
    """Levantada ao tentar bloquear novamente um material bloqueado."""


class MaterialNaoBloqueadoError(AlmoxarifadoError):
    """Levantada ao tentar desbloquear um material já desbloqueado."""


class EstoqueInsuficienteError(AlmoxarifadoError):
    """Levantada quando a quantidade retirada é maior que o estoque disponível."""


class QuantidadeInvalidaError(AlmoxarifadoError):
    """Levantada quando é informada uma quantidade menor ou igual a zero."""


class FuncionarioSemPermissaoError(AlmoxarifadoError):
    """Levantada quando um funcionário sem permissão tenta retirar materiais."""


# ---------------------------------------------------------------------------
# Exceções da camada de persistência
# ---------------------------------------------------------------------------
# A camada de persistência não exibe mensagens ao usuário: ela apenas levanta
# estas exceções, e a interface decide como apresentá-las.


class PersistenciaError(AlmoxarifadoError):
    """Classe base para os erros relacionados à persistência dos dados."""


class ArquivoPersistenciaError(PersistenciaError):
    """Levantada quando um arquivo JSON não pode ser lido ou gravado."""


class JsonInvalidoError(PersistenciaError):
    """Levantada quando o conteúdo de um arquivo não é um JSON válido."""


class DadosIncompativeisError(PersistenciaError):
    """Levantada quando os dados lidos não são compatíveis com o modelo."""


class RelacionamentoInvalidoError(PersistenciaError):
    """Levantada quando um registro referencia um objeto que não existe."""
