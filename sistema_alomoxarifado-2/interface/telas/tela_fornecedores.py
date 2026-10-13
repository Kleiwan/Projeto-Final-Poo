from interface.tela import Tela


class TelaFornecedor(Tela):
    """
    Modulo responsavel por exibir o menu de FORNECEDORES
    """

    @staticmethod
    def exibir_tela():
        print()
        print('=========MENU DE FORNECEDORES=========')
        print('[1] - Cadastrar fornecedor')
        print('[2] - Listar fornecedores')
        print('[3] - Consultar fornecedor')
        print('[4] - Editar fornecedor')
        print('[5] - Remover fornecedor')
        print('[0] - Voltar')
        print('======================================')
