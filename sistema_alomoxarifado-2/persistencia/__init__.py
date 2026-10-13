"""
Camada de persistência do sistema de almoxarifado.

Responsável por transformar os objetos do sistema em dados simples
gravados em arquivos JSON e por reconstruir os objetos a partir deles.
"""

from persistencia.fornecedor_persistencia import FornecedorPersistencia
from persistencia.funcionario_persistencia import FuncionarioPersistencia
from persistencia.material_persistencia import MaterialPersistencia
from persistencia.retirada_persistencia import RetiradaPersistencia

__all__ = [
    "FornecedorPersistencia",
    "FuncionarioPersistencia",
    "MaterialPersistencia",
    "RetiradaPersistencia",
]
