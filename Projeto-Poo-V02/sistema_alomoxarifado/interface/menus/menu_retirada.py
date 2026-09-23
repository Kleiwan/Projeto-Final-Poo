from interface.telas.tela_retiradas import Tela_Retirada
from interface.menu import Menu_base
from servicos import retirada_service
from excecoes.almoxarifado__error import (
    FuncionarioNaoEncontradoError,
    MaterialNaoEncontradoError,
    EstoqueInsuficienteError,
    QuantidadeInvalidaError,
)


class Op_Retirada(Menu_base):
    """Menu responsável pela interação com o usuário para operações de retirada."""

    @staticmethod
    def exibir_menu_especial() -> None:
        while True:
            Tela_Retirada.exibir_tela()

            deve_voltar = Op_Retirada.escolha()
            if deve_voltar:
                break

    @staticmethod
    def escolha() -> bool:
        op = input("Digite a opcao que voce deseja: ")

        try:
            if op == '0':
                return True
            elif op == '1':
                Op_Retirada.registrar_retirada()
            elif op == '2':
                Op_Retirada.listar_retiradas()
            elif op == '3':
                Op_Retirada.consultar_retirada()
            elif op == '4':
                Op_Retirada.consultar_retiradas_funcionario()
            elif op == '5':
                Op_Retirada.consultar_retiradas_material()
            elif op == '6':
                Op_Retirada.consultar_estoque()
            else:
                print('Opcao invalida!')
        except (
            FuncionarioNaoEncontradoError,
            MaterialNaoEncontradoError,
            EstoqueInsuficienteError,
            QuantidadeInvalidaError,
        ) as erro:
            print(f'Erro: {erro}')

        return False

    @staticmethod
    def registrar_retirada() -> None:
        """Solicita os dados ao usuário e registra uma nova retirada."""
        id_funcionario = int(input('Digite o ID do funcionario: '))
        codigo_material = input('Digite o codigo do material: ')
        quantidade = float(input('Digite a quantidade a retirar: '))

        retirada_service.registrar(id_funcionario, codigo_material, quantidade)
        print('Retirada registrada com sucesso!')

    @staticmethod
    def listar_retiradas() -> None:
        """Lista todas as retiradas já registradas."""
        retiradas = retirada_service.listar()
        if not retiradas:
            print('\nNenhuma retirada registrada.')
            return

        print('\n=== LISTA DE RETIRADAS ===')
        for retirada in retiradas:
            print(retirada)
        print('===========================')

    @staticmethod
    def consultar_retirada() -> None:
        """Consulta as retiradas, filtrando por funcionário ou material."""
        print('Consultar por: [1] Funcionario  [2] Material')
        opcao = input('Escolha uma opcao: ')
        if opcao == '1':
            Op_Retirada.consultar_retiradas_funcionario()
        elif opcao == '2':
            Op_Retirada.consultar_retiradas_material()
        else:
            print('Opcao invalida!')

    @staticmethod
    def consultar_retiradas_funcionario() -> None:
        """Lista as retiradas realizadas por um funcionário específico."""
        id_funcionario = int(input('Digite o ID do funcionario: '))
        retiradas = retirada_service.consultar_por_funcionario(id_funcionario)

        if not retiradas:
            print('\nNenhuma retirada encontrada para esse funcionario.')
            return

        print('\n=== RETIRADAS DO FUNCIONARIO ===')
        for retirada in retiradas:
            print(retirada)
        print('=================================')

    @staticmethod
    def consultar_retiradas_material() -> None:
        """Lista as retiradas realizadas de um material específico."""
        codigo_material = input('Digite o codigo do material: ')
        retiradas = retirada_service.consultar_por_material(codigo_material)

        if not retiradas:
            print('\nNenhuma retirada encontrada para esse material.')
            return

        print('\n=== RETIRADAS DO MATERIAL ===')
        for retirada in retiradas:
            print(retirada)
        print('==============================')

    @staticmethod
    def consultar_estoque() -> None:
        """Consulta a quantidade em estoque de um material específico."""
        codigo_material = input('Digite o codigo do material: ')
        quantidade = retirada_service.consultar_estoque(codigo_material)
        print(f'\nEstoque atual: {quantidade}')
