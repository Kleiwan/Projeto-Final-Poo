"""
Camada de aplicação do sistema de almoxarifado.
"""

from pathlib import Path
from typing import List, Optional, Union

from modelos.funcionario import Funcionario
from modelos.material import Material
from modelos.retirada import Retirada
from persistencia.funcionario_persistencia import FuncionarioPersistencia
from persistencia.material_persistencia import MaterialPersistencia
from persistencia.retirada_persistencia import RetiradaPersistencia

DIRETORIO_DADOS_PADRAO: Path = Path(__file__).resolve().parent / "dados"


class Almoxarifado:
    """
    Organiza os dados do sistema e coordena sua persistência.

    A classe guarda as coleções de funcionários, materiais e retiradas em
    memória e fornece acesso controlado a elas para a camada de serviços.
    Ao ser criada, carrega os dados gravados nos arquivos JSON; as
    operações de gravação são solicitadas pelos serviços, que não
    conhecem os arquivos: quem os conhece é a camada de persistência.
    """

    def __init__(self, diretorio_dados: Optional[Union[str, Path]] = None) -> None:
        self.__funcionarios: List[Funcionario] = []
        self.__materiais: List[Material] = []
        self.__retiradas: List[Retirada] = []

        pasta: Path = Path(diretorio_dados) if diretorio_dados is not None else DIRETORIO_DADOS_PADRAO
        self.__persistencia_funcionarios: FuncionarioPersistencia = FuncionarioPersistencia(
            pasta / "funcionarios.json"
        )
        self.__persistencia_materiais: MaterialPersistencia = MaterialPersistencia(
            pasta / "materiais.json"
        )
        self.__persistencia_retiradas: RetiradaPersistencia = RetiradaPersistencia(
            pasta / "retiradas.json"
        )

        self.carregar_dados()

    # ------------------------------------------------------------------
    # Persistência
    # ------------------------------------------------------------------
    def carregar_dados(self) -> None:
        """
        Carrega os funcionários, os materiais e as retiradas dos arquivos
        JSON e reconstrói os relacionamentos entre eles.

        Os dados só substituem os que estão em memória se todos os
        arquivos forem lidos com sucesso. Levanta PersistenciaError (ou
        uma de suas subclasses) caso algum arquivo tenha problemas.
        """
        funcionarios: List[Funcionario] = self.__persistencia_funcionarios.carregar()
        materiais: List[Material] = self.__persistencia_materiais.carregar()
        retiradas: List[Retirada] = self.__persistencia_retiradas.carregar(funcionarios, materiais)

        self.__funcionarios = funcionarios
        self.__materiais = materiais
        self.__retiradas = retiradas

    def salvar_funcionarios(self) -> None:
        """Grava os funcionários em ``funcionarios.json``."""
        self.__persistencia_funcionarios.salvar(self.funcionarios)

    def salvar_materiais(self) -> None:
        """Grava os materiais em ``materiais.json``."""
        self.__persistencia_materiais.salvar(self.materiais)

    def salvar_retiradas(self) -> None:
        """Grava as retiradas em ``retiradas.json``."""
        self.__persistencia_retiradas.salvar(self.retiradas)

    def salvar_dados(self) -> None:
        """Grava todos os dados persistentes nos arquivos JSON."""
        self.salvar_funcionarios()
        self.salvar_materiais()
        self.salvar_retiradas()

    # ------------------------------------------------------------------
    # Dados em memória
    # ------------------------------------------------------------------
    @property
    def funcionarios(self) -> List[Funcionario]:
        """Retorna uma cópia da lista de funcionários cadastrados."""
        return list(self.__funcionarios)

    def adicionar_funcionario(self, funcionario: Funcionario) -> None:
        """Adiciona um funcionário à coleção mantida em memória."""
        self.__funcionarios.append(funcionario)

    @property
    def materiais(self) -> List[Material]:
        """Retorna uma cópia da lista de materiais cadastrados."""
        return list(self.__materiais)

    def adicionar_material(self, material: Material) -> None:
        """Adiciona um material à coleção mantida em memória."""
        self.__materiais.append(material)

    @property
    def retiradas(self) -> List[Retirada]:
        """Retorna uma cópia da lista de retiradas registradas."""
        return list(self.__retiradas)

    def adicionar_retirada(self, retirada: Retirada) -> None:
        """Adiciona uma retirada à coleção mantida em memória."""
        self.__retiradas.append(retirada)

    def proximo_id_retirada(self) -> int:
        """Retorna o próximo identificador disponível para uma retirada."""
        return max((retirada.id for retirada in self.__retiradas), default=0) + 1
