from modelos.funcionario import Funcionario

class Almoxarifado:
    def __init__(self):
        self.funcionarios = []

    def cadastrar_funcionario(self, nome: str, id: int, setor: str):
        funcionario = Funcionario(nome, id, setor)
        self.funcionarios.append(funcionario)
        print ("Funcionario cadastrado com sucesso!")
        
    def listar_funcionarios(self):
        if not self.funcionarios:
            print('\nNenhum funcionario cadastrado.')
            return
        else:
            print('\n=== LISTA DE FUNCIONARIOS ===')
            for func in self.funcionarios:
                print(f'ID: {func.id} | Nome: {func.nome} | Setor: {func.setor}')
            print('=============================')