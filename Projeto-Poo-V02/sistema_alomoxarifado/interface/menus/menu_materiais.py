from interface.telas.tela_materiais import TelaMaterial
from interface.menu import Menu_base
from servicos import material_service, retirada_service
from excecoes.almoxarifado__error import (
    MaterialJaCadastradoError,
    MaterialNaoEncontradoError,
    QuantidadeInvalidaError,
)


class Op_Materiaes(Menu_base):
    """Menu responsável pela interação com o usuário para operações de materiais."""

    @staticmethod
    def exibir_menu_especial() -> None:
        while True:
            TelaMaterial.exibir_tela()

            deve_voltar = Op_Materiaes.escolha()
            if deve_voltar:
                break

    @staticmethod
    def escolha() -> bool:
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
            else:
                print('Opcao invalida!')
        except (MaterialJaCadastradoError, MaterialNaoEncontradoError, QuantidadeInvalidaError) as erro:
            print(f'Erro: {erro}')

        return False
