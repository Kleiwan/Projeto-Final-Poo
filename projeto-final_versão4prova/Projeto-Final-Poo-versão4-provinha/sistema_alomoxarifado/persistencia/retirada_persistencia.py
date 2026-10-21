"""Persistência das retiradas em arquivo JSON."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Sequence, Set, TypedDict, Union

from excecoes.almoxarifado__error import DadosIncompativeisError, RelacionamentoInvalidoError
from modelos.funcionario import Funcionario
from modelos.material import Material
from modelos.retirada import Retirada
from persistencia.arquivo_json import ArquivoJson
from persistencia.validacao import exigir_registro, ler_campo


class RetiradaDados(TypedDict):
    """
    Dados simples de uma retirada, como gravados no JSON.

    A retirada não guarda uma cópia do funcionário nem do material: apenas
    os identificadores necessários para localizá-los ao carregar os dados.
    """

    id: int
    funcionario_id: int
    material_codigo: str
    quantidade: float
    momento: str


class RetiradaPersistencia:
    """Converte retiradas em dados simples/JSON e reconstrói os relacionamentos."""

    def __init__(self, caminho: Union[str, Path]) -> None:
        self.__arquivo: ArquivoJson = ArquivoJson(caminho)

    def salvar(self, retiradas: Sequence[Retirada]) -> None:
        """Grava todas as retiradas no arquivo JSON."""
        dados: List[RetiradaDados] = [self.__para_dados(r) for r in retiradas]
        self.__arquivo.gravar_lista(list(dados))

    def carregar(
        self,
        funcionarios: Sequence[Funcionario],
        materiais: Sequence[Material],
    ) -> List[Retirada]:
        """
        Lê o arquivo JSON e reconstrói as retiradas.

        Os funcionários e materiais já carregados são recebidos como
        parâmetro para que os relacionamentos (``funcionario_id`` e
        ``material_codigo``) sejam reconstruídos apontando para os
        próprios objetos da aplicação, e não para cópias.

        Levanta RelacionamentoInvalidoError se alguma retirada referenciar
        um funcionário ou material inexistente.
        """
        nome_arquivo: str = self.__arquivo.caminho.name
        funcionarios_por_id: Dict[int, Funcionario] = {f.id: f for f in funcionarios}
        materiais_por_codigo: Dict[str, Material] = {m.codigo: m for m in materiais}

        retiradas: List[Retirada] = []
        ids_vistos: Set[int] = set()

        for posicao, item in enumerate(self.__arquivo.ler_lista(), start=1):
            retirada: Retirada = self.__para_objeto(
                item,
                f"{nome_arquivo}, item {posicao}",
                funcionarios_por_id,
                materiais_por_codigo,
            )
            if retirada.id in ids_vistos:
                raise DadosIncompativeisError(
                    f"{nome_arquivo}: o ID de retirada {retirada.id} aparece mais de uma vez."
                )
            ids_vistos.add(retirada.id)
            retiradas.append(retirada)
        return retiradas

    @staticmethod
    def __para_dados(retirada: Retirada) -> RetiradaDados:
        """Objeto -> dados simples (relacionamentos viram identificadores)."""
        return {
            "id": retirada.id,
            "funcionario_id": retirada.funcionario.id,
            "material_codigo": retirada.material.codigo,
            "quantidade": retirada.quantidade,
            "momento": retirada.momento.isoformat(),
        }

    @staticmethod
    def __para_objeto(
        item: Any,
        contexto: str,
        funcionarios_por_id: Dict[int, Funcionario],
        materiais_por_codigo: Dict[str, Material],
    ) -> Retirada:
        """Dados simples -> objeto, reconstruindo os relacionamentos pelos IDs."""
        registro: Dict[str, Any] = exigir_registro(item, contexto)

        id_retirada: int = ler_campo(registro, "id", int, contexto)
        funcionario_id: int = ler_campo(registro, "funcionario_id", int, contexto)
        material_codigo: str = ler_campo(registro, "material_codigo", str, contexto)
        quantidade: float = ler_campo(registro, "quantidade", float, contexto)
        momento_texto: str = ler_campo(registro, "momento", str, contexto)

        if quantidade <= 0:
            raise DadosIncompativeisError(f"{contexto}: a quantidade retirada deve ser maior que zero.")

        try:
            momento: datetime = datetime.fromisoformat(momento_texto)
        except ValueError as erro:
            raise DadosIncompativeisError(
                f"{contexto}: o campo 'momento' não está em um formato de data válido."
            ) from erro

        funcionario = funcionarios_por_id.get(funcionario_id)
        if funcionario is None:
            raise RelacionamentoInvalidoError(
                f"{contexto}: a retirada {id_retirada} referencia o funcionário "
                f"{funcionario_id}, que não existe."
            )

        material = materiais_por_codigo.get(material_codigo)
        if material is None:
            raise RelacionamentoInvalidoError(
                f"{contexto}: a retirada {id_retirada} referencia o material "
                f"'{material_codigo}', que não existe."
            )

        return Retirada(id_retirada, funcionario, material, quantidade, momento)
