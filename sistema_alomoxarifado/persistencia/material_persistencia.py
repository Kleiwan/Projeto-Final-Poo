"""Persistência dos materiais em arquivo JSON."""

from pathlib import Path
from typing import Any, Dict, List, Sequence, Set, TypedDict, Union

from excecoes.almoxarifado__error import DadosIncompativeisError
from modelos.material import Material
from persistencia.arquivo_json import ArquivoJson
from persistencia.validacao import exigir_registro, ler_campo


class MaterialDados(TypedDict):
    """Dados simples de um material, como gravados no JSON."""

    codigo: str
    nome: str
    quantidade: float


class MaterialPersistencia:
    """Converte materiais em dados simples/JSON e reconstrói os objetos."""

    def __init__(self, caminho: Union[str, Path]) -> None:
        self.__arquivo: ArquivoJson = ArquivoJson(caminho)

    def salvar(self, materiais: Sequence[Material]) -> None:
        """Grava todos os materiais no arquivo JSON."""
        dados: List[MaterialDados] = [self.__para_dados(m) for m in materiais]
        self.__arquivo.gravar_lista(list(dados))

    def carregar(self) -> List[Material]:
        """Lê o arquivo JSON e reconstrói a lista de materiais."""
        nome_arquivo: str = self.__arquivo.caminho.name
        materiais: List[Material] = []
        codigos_vistos: Set[str] = set()

        for posicao, item in enumerate(self.__arquivo.ler_lista(), start=1):
            material: Material = self.__para_objeto(item, f"{nome_arquivo}, item {posicao}")
            if material.codigo in codigos_vistos:
                raise DadosIncompativeisError(
                    f"{nome_arquivo}: o código de material '{material.codigo}' aparece mais de uma vez."
                )
            codigos_vistos.add(material.codigo)
            materiais.append(material)
        return materiais

    @staticmethod
    def __para_dados(material: Material) -> MaterialDados:
        """Objeto -> dados simples."""
        return {
            "codigo": material.codigo,
            "nome": material.nome,
            "quantidade": material.quantidade,
        }

    @staticmethod
    def __para_objeto(item: Any, contexto: str) -> Material:
        """Dados simples -> objeto."""
        registro: Dict[str, Any] = exigir_registro(item, contexto)
        quantidade: float = ler_campo(registro, "quantidade", float, contexto)
        if quantidade < 0:
            raise DadosIncompativeisError(
                f"{contexto}: a quantidade em estoque não pode ser negativa."
            )
        return Material(
            codigo=ler_campo(registro, "codigo", str, contexto),
            nome=ler_campo(registro, "nome", str, contexto),
            quantidade=quantidade,
        )
