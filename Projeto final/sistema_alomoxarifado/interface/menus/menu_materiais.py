from interface.telas import tela_materiais
from interface.menu import Menu_base
from dados import almoxarifado

class Op_Materiaes(Menu_base):

    @staticmethod
    def exibir_menu_especial():
        while True:
            tela_materiais.TelaMaterial.exibir_tela()

            deve_voltar = Op_Materiaes.escolha()
            if deve_voltar:
                break

    @staticmethod
    def escolha():
        op = input('Digite a opcao que voce deseja: ')
        
        if op == '1':
            try:
                codigo = int(input('Digite o id do material: '))
                if codigo <= 0:
                    raise ValueError("ID inválido. O ID deve ser um número positivo.")
            except ValueError as e:
                print(f"Erro: {e}")
                return False

            nome = input('Digite o nome do material: ')
            if not nome.strip():
                raise ValueError("Nome inválido. O nome não pode ser vazio.")
            try:
                qt_material = int(input('Digite a quantidade desse material: '))
                if qt_material < 0:
                    raise ValueError("Quantidade inválida. A quantidade deve ser um número não negativo.")
                
            except ValueError as e:
                print(f"Erro: {e}")
                return False
            almoxarifado.cadastrar_material(codigo, nome, qt_material)

        elif op == '2':
            almoxarifado.listar_materiais()
        elif op == '3':
            almoxarifado.consultar_material()
        elif op == '4':
            almoxarifado.consultar_retiradas()
        elif op == '0':
            return True
        else:
            print('Opção invalida')
        return False