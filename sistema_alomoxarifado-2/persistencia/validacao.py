"""Funções auxiliares para validar os dados simples lidos dos arquivos JSON."""

from typing import Any, Dict

from excecoes.almoxarifado__error import DadosIncompativeisError


def exigir_registro(item: Any, contexto: str) -> Dict[str, Any]:
    """Garante que o item lido do JSON é um objeto (dicionário)."""
    if not isinstance(item, dict):
        raise DadosIncompativeisError(f"{contexto}: o registro deveria ser um objeto JSON.")
    return item


def ler_campo(registro: Dict[str, Any], campo: str, tipo: type, contexto: str) -> Any:
    """
    Lê um campo obrigatório do registro, conferindo o seu tipo.

    ``tipo`` pode ser ``int``, ``float`` ou ``str``. Valores booleanos não
    são aceitos como números, e inteiros são aceitos como ``float``.
    """
    if campo not in registro:
        raise DadosIncompativeisError(f"{contexto}: o campo '{campo}' está ausente.")

    valor: Any = registro[campo]
    eh_bool: bool = isinstance(valor, bool)

    if tipo is float:
        valido: bool = isinstance(valor, (int, float)) and not eh_bool
        if valido:
            return float(valor)
    elif tipo is int:
        valido = isinstance(valor, int) and not eh_bool
    else:
        valido = isinstance(valor, tipo)

    if not valido:
        raise DadosIncompativeisError(
            f"{contexto}: o campo '{campo}' deveria ser do tipo {tipo.__name__}."
        )
    return valor


def ler_campo_opcional(registro: Dict[str, Any], campo: str, tipo: type, contexto: str) -> Any:
    """
    Lê um campo que pode estar ausente ou ser ``null``.

    Retorna None nesses dois casos; se houver valor, ele é validado como
    em ``ler_campo``. Isso mantém compatibilidade com arquivos JSON
    gravados antes de o campo existir.
    """
    if campo not in registro or registro[campo] is None:
        return None
    return ler_campo(registro, campo, tipo, contexto)
