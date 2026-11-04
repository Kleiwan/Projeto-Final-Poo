from aplicacao import Aplicacao
from interface.telas.tela_retiradas import Tela_Retirada
from interface.menu import Menu_base
from excecoes.almoxarifado__error import (
    FuncionarioNaoEncontradoError,
    FuncionarioSemPermissaoError,
    MaterialNaoEncontradoError,
    EstoqueInsuficienteError,
    QuantidadeInvalidaError,
    MaterialBloqueadoError,
)


class Op_Retirada(Menu_base):
    """Menu responsável pela interação com o usuário para operações de retirada."""

    def __init__(self, aplicacao: Aplicacao) -> None:
        self.__aplicacao = aplicacao

    def exibir_menu_especial(self) -> None:
        while True:
            Tela_Retirada.exibir_tela()

            deve_voltar = self.escolha()
            if deve_voltar:
                break

    def escolha(self) -> bool:
        op = input("Digite a opcao que voce deseja: ")

        try:
            if op == '0':
                return True
            elif op == '1':
                self.registrar_retirada()
            elif op == '2':
                self.listar_retiradas()
            elif op == '3':
                self.consultar_retirada()
            elif op == '4':
                self.consultar_retiradas_funcionario()
            elif op == '5':
                self.consultar_retiradas_material()
            elif op == '6':
                self.consultar_estoque()
            else:
                print('Opcao invalida!')
        except (
            FuncionarioNaoEncontradoError,
            FuncionarioSemPermissaoError,
            MaterialNaoEncontradoError,
            EstoqueInsuficienteError,
            QuantidadeInvalidaError,
            MaterialBloqueadoError,
            ValueError,
        ) as erro:
            print(f'Erro: {erro}')

        return False

    def registrar_retirada(self) -> None:
        """Solicita os dados ao usuário e registra uma nova retirada."""
        id_funcionario = int(input('Digite o ID do funcionario: '))
        codigo_material = input('Digite o codigo do material: ')
        quantidade = float(input('Digite a quantidade a retirar: '))

        self.__aplicacao.retirada_service.registrar(id_funcionario, codigo_material, quantidade)
        print('Retirada registrada com sucesso!')

    def listar_retiradas(self) -> None:
        """Lista todas as retiradas já registradas."""
        retiradas = self.__aplicacao.retirada_service.listar()
        if not retiradas:
            print('\nNenhuma retirada registrada.')
            return

        print('\n=== LISTA DE RETIRADAS ===')
        for retirada in retiradas:
            print(retirada)
        print('===========================')

    def consultar_retirada(self) -> None:
        """Consulta as retiradas, filtrando por funcionário ou material."""
        print('Consultar por: [1] Funcionario  [2] Material')
        opcao = input('Escolha uma opcao: ')
        if opcao == '1':
            self.consultar_retiradas_funcionario()
        elif opcao == '2':
            self.consultar_retiradas_material()
        else:
            print('Opcao invalida!')

    def consultar_retiradas_funcionario(self) -> None:
        """Lista as retiradas realizadas por um funcionário específico."""
        id_funcionario = int(input('Digite o ID do funcionario: '))
        retiradas = self.__aplicacao.retirada_service.consultar_por_funcionario(id_funcionario)

        if not retiradas:
            print('\nNenhuma retirada encontrada para esse funcionario.')
            return

        print('\n=== RETIRADAS DO FUNCIONARIO ===')
        for retirada in retiradas:
            print(retirada)
        print('=================================')

    def consultar_retiradas_material(self) -> None:
        """Lista as retiradas realizadas de um material específico."""
        codigo_material = input('Digite o codigo do material: ')
        retiradas = self.__aplicacao.retirada_service.consultar_por_material(codigo_material)

        if not retiradas:
            print('\nNenhuma retirada encontrada para esse material.')
            return

        print('\n=== RETIRADAS DO MATERIAL ===')
        for retirada in retiradas:
            print(retirada)
        print('==============================')

    def consultar_estoque(self) -> None:
        """Consulta a quantidade em estoque de um material específico."""
        codigo_material = input('Digite o codigo do material: ')
        material = self.__aplicacao.retirada_service.consultar_material(codigo_material)
        situacao = "Bloqueado" if material.bloqueado else "Desbloqueado"
        print(f'\nEstoque atual: {material.quantidade}')
        print(f'Situação: {situacao}')
        if material.bloqueado:
            print(f'Motivo do bloqueio: {material.motivo_bloqueio}')
