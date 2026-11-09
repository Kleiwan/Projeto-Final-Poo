"""
Teste do sistema integrado (cadastro, consulta, atualização, remoção,
relacionamentos, chaves estrangeiras e regras de negócio).

Execute na pasta ``sistema_alomoxarifado``:

    python -m testes.teste_sistema

Por padrão os testes rodam em um banco SQLite TEMPORÁRIO, criado vazio a cada
execução. Assim o resultado não depende de execuções anteriores e o banco
principal (``dados/almoxarifado.db``) nunca é apagado nem alterado.

Para registrar os dados do cenário no banco principal (uma única vez, sem
apagar nada), defina ``ALMOXARIFADO_TESTE_PRINCIPAL=1``. Se o banco principal
já tiver dados, a execução é recusada.
"""

import os
import sys
import tempfile
import unittest

USAR_BANCO_PRINCIPAL = os.environ.get("ALMOXARIFADO_TESTE_PRINCIPAL") == "1"
_PASTA_TEMPORARIA = None

if not USAR_BANCO_PRINCIPAL:
    # Deve ser definido antes de importar o módulo do banco.
    _PASTA_TEMPORARIA = tempfile.TemporaryDirectory()
    os.environ["ALMOXARIFADO_DB"] = os.path.join(_PASTA_TEMPORARIA.name, "teste.db")

from sqlalchemy import text  # noqa: E402
from sqlalchemy.exc import IntegrityError  # noqa: E402

from aplicacao import Aplicacao  # noqa: E402
from excecoes.almoxarifado__error import (  # noqa: E402
    EstoqueInsuficienteError,
    FuncionarioJaCadastradoError,
    FuncionarioNaoEncontradoError,
    FuncionarioSemPermissaoError,
    MaterialBloqueadoError,
    MaterialJaBloqueadoError,
    MaterialJaCadastradoError,
    MaterialNaoEncontradoError,
    QuantidadeInvalidaError,
    RemocaoNaoPermitidaError,
)
from modelos.retirada import Retirada  # noqa: E402

app = None


def setUpModule() -> None:
    """Abre a aplicação e garante que o banco comece vazio (sem apagar nada)."""
    global app
    app = Aplicacao()
    app.__enter__()
    if USAR_BANCO_PRINCIPAL and (
        app.funcionario_service.listar()
        or app.material_service.listar()
        or app.retirada_service.listar()
    ):
        app.__exit__(None, None, None)
        raise RuntimeError(
            "O banco principal já possui dados; nada foi alterado. "
            "Rode os testes sem ALMOXARIFADO_TESTE_PRINCIPAL para usar o banco temporário."
        )


def tearDownModule() -> None:
    app.__exit__(None, None, None)
    from persistencia.banco import engine
    engine.dispose()  # fecha as conexões, senão o Windows não deixa apagar o arquivo
    if _PASTA_TEMPORARIA is not None:
        _PASTA_TEMPORARIA.cleanup()

class TesteSistema(unittest.TestCase):
    """Os testes são numerados porque compartilham o estado inicial vazio do módulo."""

    def test_01_cadastros(self) -> None:
        for nome, id_, setor in [("Carlos", 1, "Cozinha"), ("Layse", 57, "Obras"),
                                 ("Rafael", 3, "TI"), ("Temp", 99, "Teste")]:
            app.funcionario_service.cadastrar(nome, id_, setor)
        for codigo, nome, qtd in [("1", "Molho de tomate", 20.0), ("67", "Telha de vidro", 100.0),
                                  ("P01", "Papel A4", 50.0), ("TMP", "Temporario", 1.0)]:
            app.material_service.cadastrar(codigo, nome, qtd)
        self.assertEqual(len(app.funcionario_service.listar()), 4)
        self.assertEqual(len(app.material_service.listar()), 4)

    def test_02_cadastros_invalidos(self) -> None:
        with self.assertRaises(FuncionarioJaCadastradoError):
            app.funcionario_service.cadastrar("Outro", 1, "X")
        with self.assertRaises(MaterialJaCadastradoError):
            app.material_service.cadastrar("1", "Outro", 1)
        with self.assertRaises(ValueError):
            app.material_service.cadastrar("Z0", "Qtd zero", 0)
        with self.assertRaises(ValueError):
            app.material_service.cadastrar("Z1", "Qtd negativa", -5)
        self.assertIsNone(app.material_service.buscar("Z0"))
        self.assertIsNone(app.material_service.buscar("Z1"))

    def test_03_retiradas_e_relacionamentos(self) -> None:
        app.retirada_service.registrar(1, "1", 3)
        app.retirada_service.registrar(3, "P01", 10)
        self.assertEqual(app.retirada_service.consultar_estoque("1"), 17)
        self.assertEqual(app.retirada_service.consultar_estoque("P01"), 40)
        do_carlos = app.retirada_service.consultar_por_funcionario(1)
        self.assertEqual(len(do_carlos), 1)
        self.assertEqual(do_carlos[0].material.codigo, "1")
        self.assertEqual(do_carlos[0].funcionario.nome, "Carlos")
        do_papel = app.retirada_service.consultar_por_material("P01")
        self.assertEqual(len(do_papel), 1)
        self.assertEqual(do_papel[0].funcionario.id, 3)

    def test_04_atualizacoes(self) -> None:
        app.material_service.adicionar_estoque("P01", 5)
        self.assertEqual(app.retirada_service.consultar_estoque("P01"), 45)
        material = app.material_service.bloquear("67", "Lote com defeito")
        self.assertTrue(material.bloqueado)
        funcionario = app.funcionario_service.retirar_permissao(57)
        self.assertFalse(funcionario.pode_retirar)
        with self.assertRaises(MaterialJaBloqueadoError):
            app.material_service.bloquear("67", "De novo")

    def test_05_regras_de_negocio(self) -> None:
        r = app.retirada_service
        with self.assertRaises(MaterialBloqueadoError):
            r.registrar(1, "67", 1)
        with self.assertRaises(EstoqueInsuficienteError):
            r.registrar(1, "1", 9999)
        with self.assertRaises(QuantidadeInvalidaError):
            r.registrar(1, "1", 0)
        with self.assertRaises(FuncionarioSemPermissaoError):
            r.registrar(57, "P01", 1)
        with self.assertRaises(FuncionarioNaoEncontradoError):
            r.registrar(404, "1", 1)
        with self.assertRaises(MaterialNaoEncontradoError):
            r.registrar(1, "XYZ", 1)
        with self.assertRaises(RemocaoNaoPermitidaError):
            app.funcionario_service.remover(1)
        with self.assertRaises(RemocaoNaoPermitidaError):
            app.material_service.remover("1")
        self.assertEqual(r.consultar_estoque("1"), 17)

    def test_06_chaves_estrangeiras(self) -> None:
        sessao = app.sessao
        self.assertEqual(sessao.execute(text("PRAGMA foreign_keys")).scalar(), 1)
        sessao.add(Retirada(funcionario_id=404, material_codigo="1", quantidade=1))
        with self.assertRaises(IntegrityError):
            sessao.commit()
        sessao.rollback()
        self.assertEqual(len(app.retirada_service.listar()), 2)

    def test_07_remocao(self) -> None:
        app.funcionario_service.remover(99)
        app.material_service.remover("TMP")
        self.assertIsNone(app.funcionario_service.buscar(99))
        self.assertIsNone(app.material_service.buscar("TMP"))

    def test_08_estado_final(self) -> None:
        self.assertEqual(len(app.funcionario_service.listar()), 3)
        self.assertEqual(len(app.material_service.listar()), 3)
        self.assertEqual(len(app.retirada_service.listar()), 2)


if __name__ == "__main__":
    # unittest.main termina com código diferente de zero se algum teste falhar.
    unittest.main(argv=[sys.argv[0], "-v"])
