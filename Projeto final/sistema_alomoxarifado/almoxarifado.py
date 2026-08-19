from modelos.funcionario import Funcionario
'''
Arquivo para armazenar e cadastrar Objetos
'''

class Almoxarifado:
#=====================================================================        
#Modulos para Funcionarios:
#=====================================================================        
    def __init__(self):
        self.funcionarios = []

    def cadastrar_funcionario(self, nome: str, id: int, setor: str):
        if self.buscar_funcionario(id) is not None:
            print('Funcionário já cadastrado')
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
                print(f'ID: {func.id} | Nome: {func.nome} | Setor: {func.setor}')
            print('=============================')
#=====================================================================        
##Funcoes de consulta Funcionarios:
#=====================================================================        

    def buscar_funcionario(self, id):
        for funcionario in self.funcionarios:
            if funcionario.id == id:
                return funcionario

        return None

    def consultar_funcionario(self):
        id_funcionario = int(input('Digite o ID do funcionario: '))
        funcionario = self.buscar_funcionario(id_funcionario)
        if funcionario:
            funcionario.printar()
        else:
            print('Funcionário não encontrado.')

#=====================================================================        
#Modulos para Material
#=====================================================================        
