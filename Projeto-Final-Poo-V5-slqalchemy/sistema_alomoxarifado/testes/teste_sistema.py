"""
Teste do sistema integrado (cadastro, consulta, atualização, remoção,
relacionamentos e regras de negócio). Popula ``dados/almoxarifado.db``.

Execute na pasta ``sistema_alomoxarifado``:

    python -m testes.teste_sistema
"""

from aplicacao import Aplicacao
from excecoes.almoxarifado__error import AlmoxarifadoError


def tentar(descricao: str, acao, esperado_erro: bool = False) -> None:
    """Executa a ação e informa se o resultado foi o esperado."""
    try:
        acao()
        resultado = "OK" if not esperado_erro else "FALHOU (deveria ser recusado)"
    except (AlmoxarifadoError, ValueError) as erro:
        resultado = f"recusado: {erro}" if esperado_erro else f"FALHOU: {erro}"
    print(f"- {descricao}: {resultado}")


with Aplicacao() as app:
    funcionarios = app.funcionario_service
    materiais = app.material_service
    retiradas = app.retirada_service

    print("\n=== Cadastros ===")
    for nome, id_, setor in [("Carlos", 1, "Cozinha"), ("Layse", 57, "Obras"), ("Rafael", 3, "TI"), ("Temp", 99, "Teste")]:
        if funcionarios.buscar(id_) is None:
            tentar(f"cadastrar funcionário {nome}", lambda n=nome, i=id_, s=setor: funcionarios.cadastrar(n, i, s))
    for codigo, nome, qtd in [("1", "Molho de tomate", 20.0), ("67", "Telha de vidro", 100.0), ("P01", "Papel A4", 50.0), ("TMP", "Temporario", 1.0)]:
        if materiais.buscar(codigo) is None:
            tentar(f"cadastrar material {nome}", lambda c=codigo, n=nome, q=qtd: materiais.cadastrar(c, n, q))
    tentar("funcionário duplicado", lambda: funcionarios.cadastrar("Outro", 1, "X"), esperado_erro=True)
    tentar("material duplicado", lambda: materiais.cadastrar("1", "Outro", 1), esperado_erro=True)

    print("\n=== Retiradas e relacionamentos ===")
    tentar("retirar 3 de molho (Carlos)", lambda: retiradas.registrar(1, "1", 3))
    tentar("retirar 10 de papel (Rafael)", lambda: retiradas.registrar(3, "P01", 10))
    print("  estoque do molho:", retiradas.consultar_estoque("1"))
    for r in retiradas.consultar_por_funcionario(1):
        print("  retirada do Carlos:", r)
    for r in retiradas.consultar_por_material("P01"):
        print("  retirada de papel:", r)

    print("\n=== Atualizações ===")
    tentar("repor 5 de papel", lambda: materiais.adicionar_estoque("P01", 5))
    tentar("bloquear telha de vidro", lambda: materiais.bloquear("67", "Lote com defeito"))
    tentar("retirar permissão da Layse", lambda: funcionarios.retirar_permissao(57))

    print("\n=== Regras de negócio (todas devem ser recusadas) ===")
    tentar("retirar material bloqueado", lambda: retiradas.registrar(1, "67", 1), esperado_erro=True)
    tentar("retirar acima do estoque", lambda: retiradas.registrar(1, "1", 9999), esperado_erro=True)
    tentar("retirar quantidade <= 0", lambda: retiradas.registrar(1, "1", 0), esperado_erro=True)
    tentar("retirar sem permissão", lambda: retiradas.registrar(57, "P01", 1), esperado_erro=True)
    tentar("funcionário inexistente", lambda: retiradas.registrar(404, "1", 1), esperado_erro=True)
    tentar("material inexistente", lambda: retiradas.registrar(1, "XYZ", 1), esperado_erro=True)
    tentar("remover funcionário com retiradas", lambda: funcionarios.remover(1), esperado_erro=True)
    tentar("remover material com retiradas", lambda: materiais.remover("1"), esperado_erro=True)
    print("  estoque do molho continua:", retiradas.consultar_estoque("1"))

    print("\n=== Remoção ===")
    if funcionarios.buscar(99) is not None:
        tentar("remover funcionário sem retiradas", lambda: funcionarios.remover(99))
    if materiais.buscar("TMP") is not None:
        tentar("remover material sem retiradas", lambda: materiais.remover("TMP"))

print("\nTeste concluído. Rode novamente 'python -m testes.consultar_banco' em outra execução para verificar a persistência.")
