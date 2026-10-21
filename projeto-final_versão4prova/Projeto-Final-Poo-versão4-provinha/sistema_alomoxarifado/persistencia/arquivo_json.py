"""Acesso de baixo nível a um arquivo JSON que contém uma lista de registros."""

import json
import os
from pathlib import Path
from typing import Any, List, Union

from excecoes.almoxarifado__error import (
    ArquivoPersistenciaError,
    DadosIncompativeisError,
    JsonInvalidoError,
)


class ArquivoJson:
    """
    Lê e grava uma lista de registros em um arquivo ``.json``.

    - Se o arquivo (ou a pasta) não existir, ele é criado automaticamente
      com uma lista vazia.
    - Um arquivo vazio é tratado como uma lista vazia.
    - A gravação é feita em um arquivo temporário e depois renomeada, para
      que uma falha no meio da escrita não corrompa os dados já salvos.

    Esta classe nunca exibe mensagens: apenas levanta exceções.
    """

    def __init__(self, caminho: Union[str, Path]) -> None:
        self.__caminho: Path = Path(caminho)

    @property
    def caminho(self) -> Path:
        """Caminho do arquivo JSON."""
        return self.__caminho

    def ler_lista(self) -> List[Any]:
        """
        Lê o arquivo e devolve a lista de registros (ainda como dados simples).

        Levanta ArquivoPersistenciaError, JsonInvalidoError ou
        DadosIncompativeisError conforme o problema encontrado.
        """
        if not self.__caminho.exists():
            self.gravar_lista([])
            return []

        try:
            texto: str = self.__caminho.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError as erro:
            raise JsonInvalidoError(
                f"O arquivo '{self.__caminho.name}' não está em UTF-8 válido."
            ) from erro
        except OSError as erro:
            raise ArquivoPersistenciaError(
                f"Não foi possível ler o arquivo '{self.__caminho.name}': {erro}"
            ) from erro

        if not texto.strip():
            return []

        try:
            dados: Any = json.loads(texto)
        except json.JSONDecodeError as erro:
            raise JsonInvalidoError(
                f"O arquivo '{self.__caminho.name}' contém um JSON inválido "
                f"(linha {erro.lineno}, coluna {erro.colno})."
            ) from erro

        if not isinstance(dados, list):
            raise DadosIncompativeisError(
                f"O arquivo '{self.__caminho.name}' deveria conter uma lista de registros."
            )
        return dados

    def gravar_lista(self, registros: List[Any]) -> None:
        """Grava a lista de registros no arquivo, criando a pasta se necessário."""
        temporario: Path = self.__caminho.with_name(self.__caminho.name + ".tmp")
        try:
            self.__caminho.parent.mkdir(parents=True, exist_ok=True)
            with open(temporario, "w", encoding="utf-8") as arquivo:
                json.dump(registros, arquivo, ensure_ascii=False, indent=4)
            os.replace(temporario, self.__caminho)
        except OSError as erro:
            try:
                temporario.unlink()
            except OSError:
                pass
            raise ArquivoPersistenciaError(
                f"Não foi possível gravar o arquivo '{self.__caminho.name}': {erro}"
            ) from erro
