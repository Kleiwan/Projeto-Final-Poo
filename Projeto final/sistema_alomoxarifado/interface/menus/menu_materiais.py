from interface.telas.tela_materiais import TelaMaterial
from interface.menu import Menu_base


class Op_Materiaes(Menu_base):

    def exibir_menu_especial():
        while True:
            TelaMaterial.exibir_tela()

            deve_voltar = Op_Materiaes.escolha()
            if deve_voltar:
                break

    def escolha():
        op = input('Digite a opcao que voce deseja')
        if op == '0':
            return True
        if op == '1':
            pass
        if op == '2':
            pass
        if op == '3':
            pass
        if op == '4':
            pass


