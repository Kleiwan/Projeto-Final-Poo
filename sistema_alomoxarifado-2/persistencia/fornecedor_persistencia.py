"""Persistência dos fornecedores em arquivo JSON."""

from pathlib import Path
from typing import Any, Dict, List, Sequence, Set, TypedDict, Union

from excecoes.almoxarifado__error import DadosIncompativeisError
from modelos.fornecedor import Fornecedor
from persistencia.arquivo_json import ArquivoJson
from persistencia.validacao import exigir_registro, ler_campo


class FornecedorDados(TypedDict):
    """Dados simples de um fornecedor, como gravados no JSON."""

    id: int
    nome: str
    contato: str


class FornecedorPersistencia:
    """Converte fornecedores em dados simples/JSON e reconstrói os objetos."""

    def __init__(self, caminho: Union[str, Path]) -> None:
        self.__arquivo: ArquivoJson = ArquivoJson(caminho)

    def salvar(self, fornecedores: Sequence[Fornecedor]) -> None:
        """Grava todos os fornecedores no arquivo JSON."""
        dados: List[FornecedorDados] = [self.__para_dados(f) for f in fornecedores]
        self.__arquivo.gravar_lista(list(dados))

    def carregar(self) -> List[Fornecedor]:
        """Lê o arquivo JSON e reconstrói a lista de fornecedores."""
        nome_arquivo: str = self.__arquivo.caminho.name
        fornecedores: List[Fornecedor] = []
        ids_vistos: Set[int] = set()

        for posicao, item in enumerate(self.__arquivo.ler_lista(), start=1):
            fornecedor: Fornecedor = self.__para_objeto(item, f"{nome_arquivo}, item {posicao}")
            if fornecedor.id in ids_vistos:
                raise DadosIncompativeisError(
                    f"{nome_arquivo}: o ID de fornecedor {fornecedor.id} aparece mais de uma vez."
                )
            ids_vistos.add(fornecedor.id)
            fornecedores.append(fornecedor)
        return fornecedores

    @staticmethod
    def __para_dados(fornecedor: Fornecedor) -> FornecedorDados:
        """Objeto -> dados simples."""
        return {"id": fornecedor.id, "nome": fornecedor.nome, "contato": fornecedor.contato}

    @staticmethod
    def __para_objeto(item: Any, contexto: str) -> Fornecedor:
        """Dados simples -> objeto."""
        registro: Dict[str, Any] = exigir_registro(item, contexto)
        return Fornecedor(
            id=ler_campo(registro, "id", int, contexto),
            nome=ler_campo(registro, "nome", str, contexto),
            contato=ler_campo(registro, "contato", str, contexto),
        )
