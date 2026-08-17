from interface.telas.tela_materiais import TelaMaterial
from interface.menu import Menu_base


class Op_Materiaes(Menu_base):

    def exibir_menu_especial():
        TelaMaterial.exibir_tela()
        Op_Materiaes.escolha()

    def escolha():
        op = input('Digite a opcao que voce deseja')
        if op == '0':
            pass
        if op == '1':
            pass
        if op == '2':
            pass
        if op == '3':
            pass
        if op == '4':
            pass


