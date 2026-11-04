"""
Lista o conteúdo do banco para verificar a persistência entre execuções.

    python -m testes.consultar_banco
"""

from aplicacao import Aplicacao

with Aplicacao() as app:
    print("\n=== FUNCIONÁRIOS ===")
    for funcionario in app.funcionario_service.listar():
        funcionario.printar()

    print("\n=== MATERIAIS ===")
    for material in app.material_service.listar():
        material.printar()

    print("\n=== RETIRADAS ===")
    for retirada in app.retirada_service.listar():
        print(retirada)
