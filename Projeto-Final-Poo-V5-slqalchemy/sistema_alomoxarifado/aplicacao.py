"""Camada de aplicação: controla a sessão e disponibiliza os serviços."""

from sqlalchemy.orm import Session

from persistencia.banco import criar_sessao, criar_tabelas
from servicos.funcionario_service import FuncionarioService
from servicos.material_service import MaterialService
from servicos.retirada_service import RetiradaService


class Aplicacao:
    """
    Inicializa o banco, abre a sessão e entrega a mesma sessão a todos os
    serviços. Deve ser usada com ``with``: a sessão é fechada ao sair do bloco.
    """

    def __init__(self) -> None:
        criar_tabelas()
        self.__sessao: Session | None = None
        self.__funcionario_service: FuncionarioService | None = None
        self.__material_service: MaterialService | None = None
        self.__retirada_service: RetiradaService | None = None

    def __enter__(self) -> "Aplicacao":
        self.__sessao = criar_sessao()
        self.__funcionario_service = FuncionarioService(self.sessao)
        self.__material_service = MaterialService(self.sessao)
        self.__retirada_service = RetiradaService(self.sessao)
        return self

    def __exit__(self, tipo_excecao, excecao, traceback) -> None:
        if self.__sessao is not None:
            self.__sessao.close()
            self.__sessao = None

    @property
    def sessao(self) -> Session:
        """Sessão em uso pela aplicação."""
        if self.__sessao is None:
            raise RuntimeError("A aplicação não foi inicializada.")
        return self.__sessao

    @property
    def funcionario_service(self) -> FuncionarioService:
        """Serviço de funcionários."""
        if self.__funcionario_service is None:
            raise RuntimeError("A aplicação não foi inicializada.")
        return self.__funcionario_service

    @property
    def material_service(self) -> MaterialService:
        """Serviço de materiais."""
        if self.__material_service is None:
            raise RuntimeError("A aplicação não foi inicializada.")
        return self.__material_service

    @property
    def retirada_service(self) -> RetiradaService:
        """Serviço de retiradas."""
        if self.__retirada_service is None:
            raise RuntimeError("A aplicação não foi inicializada.")
        return self.__retirada_service
