"""Camada de aplicação: gerencia sessão e disponibiliza os serviços."""
from sqlalchemy.orm import Session
from persistencia.banco import criar_sessao, criar_tabelas
from servicos.funcionario_service import FuncionarioService
from servicos.material_service import MaterialService
from servicos.retirada_service import RetiradaService
from servicos.entrada_service import EntradaService

class Aplicacao:
    def __init__(self):
        criar_tabelas()
        self.__sessao: Session | None = None
    def __enter__(self):
        self.__sessao=criar_sessao()
        self.__funcionario_service=FuncionarioService(self.sessao)
        self.__material_service=MaterialService(self.sessao)
        self.__retirada_service=RetiradaService(self.sessao)
        self.__entrada_service=EntradaService(self.sessao)
        return self
    def __exit__(self,tipo_excecao,excecao,traceback):
        if self.__sessao is not None: self.__sessao.close(); self.__sessao=None
    @property
    def sessao(self):
        if self.__sessao is None: raise RuntimeError("A aplicação não foi inicializada.")
        return self.__sessao
    @property
    def funcionario_service(self): return self.__funcionario_service
    @property
    def material_service(self): return self.__material_service
    @property
    def retirada_service(self): return self.__retirada_service
    @property
    def entrada_service(self): return self.__entrada_service
