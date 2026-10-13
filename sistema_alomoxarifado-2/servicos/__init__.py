"""
Pacote de serviços da aplicação.

Este módulo cria uma única instância da camada de aplicação
(Almoxarifado) e uma única instância de cada serviço, compartilhadas
por toda a interface. Isso evita que cada tela/menu crie sua própria
cópia dos dados em memória (o que faria, por exemplo, um funcionário
cadastrado pelo menu de funcionários "sumir" para o menu de retiradas).
"""

from almoxarifado import Almoxarifado
from servicos.fornecedor_service import FornecedorService
from servicos.funcionario_service import FuncionarioService
from servicos.material_service import MaterialService
from servicos.retirada_service import RetiradaService

_almoxarifado = Almoxarifado()

fornecedor_service = FornecedorService(_almoxarifado)
funcionario_service = FuncionarioService(_almoxarifado)
material_service = MaterialService(_almoxarifado, fornecedor_service)
retirada_service = RetiradaService(_almoxarifado, funcionario_service, material_service)

__all__ = [
    "fornecedor_service",
    "funcionario_service",
    "material_service",
    "retirada_service",
]
