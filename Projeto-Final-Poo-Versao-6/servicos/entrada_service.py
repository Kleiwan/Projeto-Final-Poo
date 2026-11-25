"""Serviço para registrar entradas e reposições, mantendo histórico."""
from sqlalchemy import select
from sqlalchemy.orm import Session
from modelos.entrada import Entrada
from modelos.funcionario import Funcionario
from modelos.material import Material
from excecoes.almoxarifado__error import FuncionarioNaoEncontradoError, MaterialNaoEncontradoError, QuantidadeInvalidaError

class EntradaService:
    def __init__(self, sessao: Session): self.__sessao=sessao
    def registrar(self, id_funcionario: int, codigo_material: str, quantidade: float, observacao: str="") -> Entrada:
        if quantidade <= 0: raise QuantidadeInvalidaError("A quantidade de entrada deve ser maior que zero.")
        funcionario=self.__sessao.get(Funcionario,id_funcionario)
        if funcionario is None: raise FuncionarioNaoEncontradoError(f"Funcionário {id_funcionario} não encontrado.")
        if not funcionario.ativo: raise ValueError("Funcionário inativo não pode registrar entrada.")
        material=self.__sessao.get(Material,codigo_material)
        if material is None: raise MaterialNaoEncontradoError(f"Material {codigo_material} não encontrado.")
        if not material.ativo: raise ValueError("Material inativo não pode receber movimentações.")
        try:
            material.adicionar_estoque(quantidade)
            entrada=Entrada(funcionario=funcionario,material=material,quantidade=quantidade,observacao=observacao.strip())
            self.__sessao.add(entrada); self.__sessao.commit(); self.__sessao.refresh(entrada)
            return entrada
        except Exception:
            self.__sessao.rollback(); raise
    def listar(self):
        return list(self.__sessao.scalars(select(Entrada).order_by(Entrada.id)).all())
    def consultar_por_material(self,codigo):
        return list(self.__sessao.scalars(select(Entrada).where(Entrada.material_codigo==codigo).order_by(Entrada.id)).all())
