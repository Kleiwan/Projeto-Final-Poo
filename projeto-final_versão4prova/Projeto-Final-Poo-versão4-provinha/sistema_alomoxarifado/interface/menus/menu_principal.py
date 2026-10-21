from interface.telas.tela_pricipal import tela_menu_principal
from interface.menus.menu_funcionarios import Op_Funcionarios
from interface.menus.menu_materiais import Op_Materiaes
from interface.menus.menu_retirada import Op_Retirada
from interface.menu import Menu_base


class Op_MenuInit(Menu_base):
    @staticmethod
    def exibir_menu_especial() -> None:
        while True:
            tela_menu_principal.exibir_tela()
            deve_sair = Op_MenuInit.escolha()
            if deve_sair:
                print('Saindo do sistema...')
                break

    @staticmethod
    def escolha() -> bool:
        op = input('Digite a opcao que voce deseja: ')
        if op == '1':
            Op_Funcionarios.exibir_menu_especial()
        elif op == '2':
            Op_Materiaes.exibir_menu_especial()
        elif op == '3':
            Op_Retirada.exibir_menu_especial()
        elif op == '0':
            return True
        else:
            print('Opcao invalida!')
        return False
