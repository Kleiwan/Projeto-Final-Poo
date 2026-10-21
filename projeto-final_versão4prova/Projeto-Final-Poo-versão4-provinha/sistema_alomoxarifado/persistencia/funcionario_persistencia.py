"""Persistência dos funcionários em arquivo JSON."""

from pathlib import Path
from typing import Any, Dict, List, Sequence, Set, TypedDict, Union

from excecoes.almoxarifado__error import DadosIncompativeisError
from modelos.funcionario import Funcionario
from persistencia.arquivo_json import ArquivoJson
from persistencia.validacao import exigir_registro, ler_campo


class FuncionarioDados(TypedDict):
    """Dados simples de um funcionário, como gravados no JSON."""

    id: int
    nome: str
    setor: str
    pode_retirar: bool


class FuncionarioPersistencia:
    """Converte funcionários em dados simples/JSON e reconstrói os objetos."""

    def __init__(self, caminho: Union[str, Path]) -> None:
        self.__arquivo: ArquivoJson = ArquivoJson(caminho)

    def salvar(self, funcionarios: Sequence[Funcionario]) -> None:
        """Grava todos os funcionários no arquivo JSON."""
        dados: List[FuncionarioDados] = [self.__para_dados(f) for f in funcionarios]
        self.__arquivo.gravar_lista(list(dados))

    def carregar(self) -> List[Funcionario]:
        """Lê o arquivo JSON e reconstrói a lista de funcionários."""
        nome_arquivo: str = self.__arquivo.caminho.name
        funcionarios: List[Funcionario] = []
        ids_vistos: Set[int] = set()

        for posicao, item in enumerate(self.__arquivo.ler_lista(), start=1):
            funcionario: Funcionario = self.__para_objeto(item, f"{nome_arquivo}, item {posicao}")
            if funcionario.id in ids_vistos:
                raise DadosIncompativeisError(
                    f"{nome_arquivo}: o ID de funcionário {funcionario.id} aparece mais de uma vez."
                )
            ids_vistos.add(funcionario.id)
            funcionarios.append(funcionario)
        return funcionarios

    @staticmethod
    def __para_dados(funcionario: Funcionario) -> FuncionarioDados:
        """Objeto -> dados simples."""
        return {
            "id": funcionario.id,
            "nome": funcionario.nome,
            "setor": funcionario.setor,
            "pode_retirar": funcionario.pode_retirar,
        }

    @staticmethod
    def __para_objeto(item: Any, contexto: str) -> Funcionario:
        """Dados simples -> objeto."""
        registro: Dict[str, Any] = exigir_registro(item, contexto)

        # Arquivos gravados antes da existência da permissão não têm o campo
        # "pode_retirar"; nesse caso o funcionário continua autorizado, como
        # era o comportamento anterior. Se o campo existir, deve ser booleano.
        pode_retirar: bool = True
        if "pode_retirar" in registro:
            pode_retirar = ler_campo(registro, "pode_retirar", bool, contexto)

        return Funcionario(
            nome=ler_campo(registro, "nome", str, contexto),
            id=ler_campo(registro, "id", int, contexto),
            setor=ler_campo(registro, "setor", str, contexto),
            pode_retirar=pode_retirar,
        )
