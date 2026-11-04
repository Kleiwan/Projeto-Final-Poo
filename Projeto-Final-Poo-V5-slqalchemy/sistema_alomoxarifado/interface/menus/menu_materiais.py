from aplicacao import Aplicacao
from interface.telas.tela_materiais import TelaMaterial
from interface.menu import Menu_base
from excecoes.almoxarifado__error import (
    MaterialJaCadastradoError,
    MaterialNaoEncontradoError,
    QuantidadeInvalidaError,
    RemocaoNaoPermitidaError,
    MaterialBloqueadoError,
    MaterialJaBloqueadoError,
    MaterialNaoBloqueadoError,
)


class Op_Materiaes(Menu_base):
    """Menu responsável pela interação com o usuário para operações de materiais."""

    def __init__(self, aplicacao: Aplicacao) -> None:
        self.__aplicacao = aplicacao

    def exibir_menu_especial(self) -> None:
        while True:
            TelaMaterial.exibir_tela()

            deve_voltar = self.escolha()
            if deve_voltar:
                break

    def escolha(self) -> bool:
        material_service = self.__aplicacao.material_service
        retirada_service = self.__aplicacao.retirada_service

        op = input('Digite a opcao que voce deseja: ')
        try:
            if op == '0':
                return True
            elif op == '1':
                codigo = input('Digite o codigo do material: ')
                nome = input('Digite o nome do material: ')
                quantidade = float(input('Digite a quantidade inicial em estoque: '))
                material_service.cadastrar(codigo, nome, quantidade)
                print('Material cadastrado com sucesso!')
            elif op == '2':
                materiais = material_service.listar()
                if not materiais:
                    print('\nNenhum material cadastrado.')
                else:
                    print('\n=== LISTA DE MATERIAIS ===')
                    for material in materiais:
                        material.printar()
                    print('===========================')
            elif op == '3':
                codigo = input('Digite o codigo do material: ')
                material = material_service.consultar(codigo)
                material.printar()
            elif op == '4':
                codigo = input('Digite o codigo do material: ')
                retiradas = retirada_service.consultar_por_material(codigo)
                if not retiradas:
                    print('\nNenhuma retirada encontrada para esse material.')
                else:
                    print('\n=== RETIRADAS DO MATERIAL ===')
                    for retirada in retiradas:
                        print(retirada)
                    print('==============================')
            elif op == '5':
                codigo = input('Digite o codigo do material: ')
                motivo = input('Informe o motivo do bloqueio: ')
                material_service.bloquear(codigo, motivo)
                print('Material bloqueado com sucesso!')
            elif op == '6':
                codigo = input('Digite o codigo do material: ')
                material_service.desbloquear(codigo)
                print('Material desbloqueado com sucesso!')
            elif op == '7':
                codigo = input('Digite o codigo do material: ')
                material_service.remover(codigo)
                print('Material removido com sucesso!')
            else:
                print('Opcao invalida!')
        except (
            MaterialJaCadastradoError,
            MaterialNaoEncontradoError,
            QuantidadeInvalidaError,
            RemocaoNaoPermitidaError,
            MaterialBloqueadoError,
            MaterialJaBloqueadoError,
            MaterialNaoBloqueadoError,
            ValueError,
        ) as erro:
            print(f'Erro: {erro}')

        return False
