"""Serviço responsável por coordenar o registro e a consulta de retiradas."""

from datetime import datetime
from typing import List

from almoxarifado import Almoxarifado
from modelos.retirada import Retirada
from servicos.funcionario_service import FuncionarioService
from servicos.material_service import MaterialService
from excecoes.almoxarifado__error import QuantidadeInvalidaError


class RetiradaService:
    """
    Coordena a operação de retirada de materiais.

    Localiza o funcionário e o material envolvidos, verifica as
    condições necessárias (quantidade válida e estoque disponível)
    e, se tudo estiver correto, realiza a operação e registra a retirada.
    """

    def __init__(
        self,
        almoxarifado: Almoxarifado,
        funcionario_service: FuncionarioService,
        material_service: MaterialService,
    ) -> None:
        self.__almoxarifado = almoxarifado
        self.__funcionario_service = funcionario_service
        self.__material_service = material_service

    def registrar(self, id_funcionario: int, codigo_material: str, quantidade: float) -> Retirada:
        """
        Registra a retirada de uma quantidade de material por um funcionário.

        Levanta FuncionarioNaoEncontradoError, MaterialNaoEncontradoError,
        QuantidadeInvalidaError ou EstoqueInsuficienteError, conforme o caso.
        """
        if quantidade <= 0:
            raise QuantidadeInvalidaError("A quantidade retirada deve ser maior que zero.")

        funcionario = self.__funcionario_service.consultar(id_funcionario)
        material = self.__material_service.consultar(codigo_material)

        material.retirar_estoque(quantidade)

        retirada = Retirada(funcionario, material, quantidade, datetime.now())
        self.__almoxarifado.adicionar_retirada(retirada)
        return retirada

    def listar(self) -> List[Retirada]:
        """Retorna a lista de todas as retiradas registradas."""
        return self.__almoxarifado.retiradas

    def consultar_por_funcionario(self, id_funcionario: int) -> List[Retirada]:
        """Retorna as retiradas realizadas por um funcionário específico."""
        return [
            retirada
            for retirada in self.__almoxarifado.retiradas
            if retirada.funcionario.id == id_funcionario
        ]

    def consultar_por_material(self, codigo_material: str) -> List[Retirada]:
        """Retorna as retiradas realizadas de um material específico."""
        return [
            retirada
            for retirada in self.__almoxarifado.retiradas
            if retirada.material.codigo == codigo_material
        ]

    def consultar_estoque(self, codigo_material: str) -> float:
        """Retorna a quantidade em estoque de um material específico."""
        material = self.__material_service.consultar(codigo_material)
        return material.quantidade
