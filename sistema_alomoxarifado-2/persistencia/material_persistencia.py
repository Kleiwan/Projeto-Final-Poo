"""Persistência dos materiais em arquivo JSON."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, TypedDict, Union

from excecoes.almoxarifado__error import DadosIncompativeisError, RelacionamentoInvalidoError
from modelos.fornecedor import Fornecedor
from modelos.material import Material
from persistencia.arquivo_json import ArquivoJson
from persistencia.validacao import exigir_registro, ler_campo, ler_campo_opcional


class MaterialDados(TypedDict):
    """
    Dados simples de um material, como gravados no JSON.

    O fornecedor não é copiado: guarda-se apenas o ``fornecedor_id``
    (ou ``null`` quando o material não tem fornecedor).
    """

    codigo: str
    nome: str
    quantidade: float
    fornecedor_id: Optional[int]


class MaterialPersistencia:
    """Converte materiais em dados simples/JSON e reconstrói os objetos."""

    def __init__(self, caminho: Union[str, Path]) -> None:
        self.__arquivo: ArquivoJson = ArquivoJson(caminho)

    def salvar(self, materiais: Sequence[Material]) -> None:
        """Grava todos os materiais no arquivo JSON."""
        dados: List[MaterialDados] = [self.__para_dados(m) for m in materiais]
        self.__arquivo.gravar_lista(list(dados))

    def carregar(self, fornecedores: Sequence[Fornecedor]) -> List[Material]:
        """
        Lê o arquivo JSON e reconstrói a lista de materiais.

        Os fornecedores já carregados são recebidos como parâmetro para
        que o relacionamento (``fornecedor_id``) seja reconstruído.
        Levanta RelacionamentoInvalidoError se um material referenciar
        um fornecedor inexistente.
        """
        nome_arquivo: str = self.__arquivo.caminho.name
        fornecedores_por_id: Dict[int, Fornecedor] = {f.id: f for f in fornecedores}
        materiais: List[Material] = []
        codigos_vistos: Set[str] = set()

        for posicao, item in enumerate(self.__arquivo.ler_lista(), start=1):
            material: Material = self.__para_objeto(
                item, f"{nome_arquivo}, item {posicao}", fornecedores_por_id
            )
            if material.codigo in codigos_vistos:
                raise DadosIncompativeisError(
                    f"{nome_arquivo}: o código de material '{material.codigo}' aparece mais de uma vez."
                )
            codigos_vistos.add(material.codigo)
            materiais.append(material)
        return materiais

    @staticmethod
    def __para_dados(material: Material) -> MaterialDados:
        """Objeto -> dados simples (o relacionamento vira um identificador)."""
        return {
            "codigo": material.codigo,
            "nome": material.nome,
            "quantidade": material.quantidade,
            "fornecedor_id": material.fornecedor.id if material.fornecedor is not None else None,
        }

    @staticmethod
    def __para_objeto(
        item: Any,
        contexto: str,
        fornecedores_por_id: Dict[int, Fornecedor],
    ) -> Material:
        """Dados simples -> objeto, reconstruindo o relacionamento pelo ID."""
        registro: Dict[str, Any] = exigir_registro(item, contexto)
        quantidade: float = ler_campo(registro, "quantidade", float, contexto)
        if quantidade < 0:
            raise DadosIncompativeisError(
                f"{contexto}: a quantidade em estoque não pode ser negativa."
            )

        fornecedor: Optional[Fornecedor] = None
        fornecedor_id: Optional[int] = ler_campo_opcional(registro, "fornecedor_id", int, contexto)
        if fornecedor_id is not None:
            fornecedor = fornecedores_por_id.get(fornecedor_id)
            if fornecedor is None:
                raise RelacionamentoInvalidoError(
                    f"{contexto}: o material referencia o fornecedor {fornecedor_id}, "
                    f"que não existe."
                )

        return Material(
            codigo=ler_campo(registro, "codigo", str, contexto),
            nome=ler_campo(registro, "nome", str, contexto),
            quantidade=quantidade,
            fornecedor=fornecedor,
        )
