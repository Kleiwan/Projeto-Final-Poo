from interface.telas import tela_funcionario
from interface.menu import Menu_base
from almoxarifado import Almoxarifado

almoxarifado = Almoxarifado()


class Op_Funcionarios(Menu_base):

    @staticmethod
    def exibir_menu_especial():
        while True:
            tela_funcionario.Tela_Funcionario.exibir_tela()

            deve_voltar = Op_Funcionarios.escolha()
            if deve_voltar:
                break

    @staticmethod
    def escolha():
        op = input('Digite a opcao que voce deseja: ')
        if op == '1':
            nome = input('Digite o nome do funcionario: ')
            id = int(input('Digite o id do funcionario: '))
            setor = input('Digite o setor do funcionario: ')
            almoxarifado.cadastrar_funcionario(nome, id, setor)
        elif op == '2':
            almoxarifado.listar_funcionarios()
        elif op == '0':
            return True
        else:
            print('Opcao invalida!')
            
        return False