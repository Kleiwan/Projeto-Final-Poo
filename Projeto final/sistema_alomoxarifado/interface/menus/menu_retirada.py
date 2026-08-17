from interface.telas.tela_retiradas import Tela_Retirada
from interface.menu import Menu_base

class Op_Retirada(Menu_base):

    def exibir_menu_especial():
        Tela_Retirada.exibir_tela()
        Op_Retirada.escolha()
    
    def escolha():
        op = input("Digite a opcao que voce deseja: ")

        if op == '0':
            pass
        elif op == '1':
            pass
        elif op == '2':
            pass
        elif op == '3':
            pass
        elif op == '4':
            pass
        else:
                print('Opcao invalida!')
                Op_Retirada.exibir_menu_especial