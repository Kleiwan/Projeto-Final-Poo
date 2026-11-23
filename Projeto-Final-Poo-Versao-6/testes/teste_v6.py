import os, tempfile, unittest
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from modelos.base import Base
from modelos import funcionario, material, retirada, entrada
from servicos.funcionario_service import FuncionarioService
from servicos.material_service import MaterialService
from servicos.retirada_service import RetiradaService
from servicos.entrada_service import EntradaService

class TesteVersao6(unittest.TestCase):
    def setUp(self):
        self.engine=create_engine("sqlite://")
        Base.metadata.create_all(self.engine)
        self.s=Session(self.engine)
        self.fs=FuncionarioService(self.s); self.ms=MaterialService(self.s)
        self.rs=RetiradaService(self.s); self.es=EntradaService(self.s)
        self.fs.cadastrar("Ana",1,"TI")
        self.ms.cadastrar("MAT-1","Papel",100)
    def tearDown(self):
        self.s.close(); self.engine.dispose()
    def test_editar_funcionario(self):
        f=self.fs.editar(1,"Ana Silva","Tecnologia")
        self.assertEqual((f.nome,f.setor),("Ana Silva","Tecnologia"))
    def test_editar_material(self):
        m=self.ms.editar("MAT-1","Papel A4","Papelaria","resma",5)
        self.assertEqual(m.categoria,"Papelaria")
        self.assertEqual(m.estoque_minimo,5)
    def test_entrada_e_retirada_com_historico(self):
        e=self.es.registrar(1,"MAT-1",20,"Compra")
        self.assertEqual(self.ms.consultar("MAT-1").quantidade,120)
        r=self.rs.registrar(1,"MAT-1",15,"Uso interno")
        self.assertEqual(self.ms.consultar("MAT-1").quantidade,105)
        self.assertEqual(len(self.es.listar()),1)
        self.assertEqual(len(self.rs.listar()),1)
    def test_nao_remove_historico(self):
        self.rs.registrar(1,"MAT-1",1)
        with self.assertRaises(Exception): self.fs.remover(1)

if __name__=="__main__": unittest.main(verbosity=2)
