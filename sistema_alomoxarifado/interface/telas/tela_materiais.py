from interface.tela import Tela

class TelaMaterial(Tela):
    """
    Modulo responsavel por printar o menu de MATERIAIS
    """

    @staticmethod
    def exibir_tela():
        print()
        print('=========MENU DE MATERIAIS=========')
        print('[1] - Cadastrar materiais')
        print('[2] - Listar materiais')
        print('[3] - Consultar materiais')
        print('[4] - Contsultar retirada de material')
        print('[0] - Voltar')
        print('======================================')
