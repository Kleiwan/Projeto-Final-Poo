from interface.telas.tela_retiradas import Tela_Retirada
from interface.menu import Menu_base
from dados import almoxarifado

class Op_Retirada(Menu_base):

    @staticmethod
    def exibir_menu_especial():
        while True:
            Tela_Retirada.exibir_tela()

            deve_voltar = Op_Retirada.escolha()

            if deve_voltar:
                break

    @staticmethod
    def escolha():
        op = input("Digite a opcao que voce deseja: ")

        if op == '0':
            return True

        elif op == '1':
            almoxarifado.registrar_retirada()

        elif op == '2':
            almoxarifado.listar_retiradas()

        elif op == '3':
            almoxarifado.consultar_retiradas()

        elif op == '4':
            almoxarifado.consultar_retiradas_funcionario()

        elif op == '5':
            almoxarifado.consultar_retiradas_material()

        elif op == '6':
            almoxarifado.consultar_estoque()

        else:
            print('Opcao invalida!')

        return False