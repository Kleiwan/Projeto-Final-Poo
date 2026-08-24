from modelos.funcionario import Funcionario
from modelos.material import Material
from modelos.retirada import Retirada
from excecoes.validacao_funcionario import id_invalido 

# Importando a função de validação (certifique-se de ter criado o arquivo validacao_entrada.py)
from excecoes.validacao_entrada import ler_inteiro 

'''
Arquivo para armazenar e cadastrar Objetos
'''

class Almoxarifado:
#=====================================================================        
# Modulos para Funcionarios:
#=====================================================================        
    def __init__(self):
        self.funcionarios = []
        self.materiais = []
        self.retiradas = []

    def cadastrar_funcionario(self, nome: str, id: int, setor: str):
        if self.buscar_funcionario(id) is not None:
            print('Funcionário já cadastrado')
        elif id <= 0:
            id_invalido()
        else:
            funcionario = Funcionario(nome, id, setor)
            self.funcionarios.append(funcionario)
            print('Funcionário cadastrado com sucesso!')
        
    def listar_funcionarios(self):
        if not self.funcionarios:
            print('\nNenhum funcionario cadastrado.')
            return
        else:
            print('\n=== LISTA DE FUNCIONARIOS ===')
            for func in self.funcionarios:
                print(f'ID: {func.funcionario_id} | Nome: {func.nome} | Setor: {func.setor}')
            print('=============================')

    def consultar_retirada_lista(self):
        if not self.retiradas:
            print('Nenhuma retirada registrada.')
            return

        print('\n=== LISTA DE RETIRADAS ===')
        for indice, ret in enumerate(self.retiradas):
            print(f'Índice: {indice}')
            ret.printar_retirada()
        print('=============================')
         
#=====================================================================        
## Funcoes de consulta Funcionarios:
#=====================================================================        

    def buscar_funcionario(self, funcionario_id):
        for funcionario in self.funcionarios:
            if funcionario.funcionario_id == funcionario_id:
                return funcionario
        return None

    def consultar_funcionario(self):
        id_funcionario = ler_inteiro('Digite o ID do funcionario: ')
        
        funcionario = self.buscar_funcionario(id_funcionario)
        if funcionario:
            funcionario.printar()
        else:
            print('Funcionário não encontrado.')

#=====================================================================        
# Modulos para Material
#=====================================================================        

    def cadastrar_material(self, codigo: str, nome: str, qt_material: int):
        if self.buscar_material(codigo) is not None:
            print('Material já cadastrado')
        else:
            material = Material(codigo, nome, qt_material)
            self.materiais.append(material)
            print('Material cadastrado com sucesso!')

    def listar_materiais(self):
        if not self.materiais:
            print('\nNenhum material cadastrado.')
            return
        else:
            print('\n=== LISTA DE MATERIAIS ===')
            for mat in self.materiais:
                print(f'ID: {mat.codigo} | Nome: {mat.nome} | Quantidade: {mat.qt_material}')
            print('=============================')

#=====================================================================        
## Funcoes de consulta Materiais:
#=====================================================================  
    def buscar_material(self, codigo):
            for material in self.materiais:
                if material.codigo == codigo:
                    return material
            return None

    def consultar_material(self):
        codigo_material = ler_inteiro('Digite o ID do material: ')
        
        material = self.buscar_material(codigo_material)
        if material:
            material.printar_material()
        else:
            print('Material não encontrado.')

#=====================================================================        
## Modulos para Retirada de Materiais:
#=====================================================================  

    def registrar_retirada(self):
        # Validações separadas
        funcionario_id = ler_inteiro('Digite o ID do funcionario: ')
        codigo = ler_inteiro('Digite o ID do material: ')
        qt_retirada = ler_inteiro('Digite a quantidade a ser retirada: ')

        if qt_retirada <= 0:
            print('Erro: A quantidade a ser retirada deve ser maior que zero.')
            return

        funcionario = self.buscar_funcionario(funcionario_id)
        material = self.buscar_material(codigo)

        if funcionario and material:
            if material.qt_material >= qt_retirada:
                material.qt_material -= qt_retirada
                retirada = Retirada(funcionario, material, qt_retirada)
                self.retiradas.append(retirada)
                print('Retirada registrada com sucesso!')
            else:
                print('Quantidade insuficiente em estoque.')
        else:
            print('Funcionário ou material não encontrado.')

    def listar_retiradas(self):
        if not self.retiradas:
            print('\nNenhuma retirada registrada.')
            return
        else:
            print('\n=== CONSULTA DE RETIRADAS ===')
            for indice, ret in enumerate(self.retiradas):
                print(f'Índice: {indice}')
                ret.printar_retirada()
            print('=============================')

#=====================================================================        
## Funcoes de consulta Retiradas:
#=====================================================================

    def consultar_retiradas(self):
        if not self.retiradas:
            print('Nenhuma retirada registrada.')
            return

        indice = ler_inteiro('Digite o índice da retirada: ')

        if 0 <= indice < len(self.retiradas):
            retirada = self.retiradas[indice]
            retirada.printar_retirada()
        else:
            print('Índice inválido.')

    def consultar_retiradas_funcionario(self):
        funcionario_id = ler_inteiro('Digite o ID do funcionario: ')
        
        funcionario = self.buscar_funcionario(funcionario_id)

        if funcionario:
            print(f'\n=== RETIRADAS DO FUNCIONARIO {funcionario.nome} ===')
            for ret in self.retiradas:
                if ret.funcionario == funcionario:
                    ret.printar_retirada()
            print('===============================================')
        else:
            print('Funcionário não encontrado.')

    def consultar_retiradas_material(self):
        codigo_material = ler_inteiro('Digite o ID do material: ')
        
        material = self.buscar_material(codigo_material)

        if material:
            print(f'\n=== RETIRADAS DO MATERIAL {material.nome} ===')
            for ret in self.retiradas:
                if ret.material == material:
                    ret.printar_retirada()
            print('===============================================')
        else:
            print('Material não encontrado.')

    def consultar_estoque(self):
        if not self.materiais:
            print('Nenhum material cadastrado.')
            return

        print('\n=== ESTOQUE DE MATERIAIS ===')
        for mat in self.materiais:
            print(f'ID: {mat.codigo} | Nome: {mat.nome} | Quantidade: {mat.qt_material}')
        print('=============================')