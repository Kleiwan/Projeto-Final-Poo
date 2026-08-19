from interface.telas.tela_retiradas import Tela_Retirada
from interface.menu import Menu_base
from almoxarifado import Almoxarifado

class Op_Retirada(Menu_base):

    def exibir_menu_especial():
        while True:
            Tela_Retirada.exibir_tela()

            deve_voltar = Op_Retirada.escolha()
            if deve_voltar:
                break
    
    def escolha():
        op = input("Digite a opcao que voce deseja: ")

        if op == '0':
            return True
        elif op == '1':
             Op_Retirada.registrar_retirada()
        elif op == '2':
            Op_Retirada.consultar_retirada()
        elif op == '3':
            Op_Retirada.listar_retiradas()
        elif op == '4':
            Op_Retirada.consultar_retiradas_funcionario()
        elif op == '5':
            Op_Retirada.consultar_retiradas_material()
        elif op == '6':
            Op_Retirada.consultar_estoque()
        else:
                print('Opcao invalida!')
                Op_Retirada.exibir_menu_especial