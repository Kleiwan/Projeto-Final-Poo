from typing import Optional

from interface.telas.tela_materiais import TelaMaterial
from interface.menu import Menu_base
from servicos import material_service, retirada_service
from excecoes.almoxarifado__error import (
    FornecedorNaoEncontradoError,
    MaterialComRetiradasError,
    MaterialJaCadastradoError,
    MaterialNaoEncontradoError,
    QuantidadeInvalidaError,
    PersistenciaError,
)


def _texto_ou_none(mensagem: str) -> Optional[str]:
    """Lê um texto; se o usuário apenas pressionar Enter, retorna None (manter valor atual)."""
    texto = input(mensagem).strip()
    return texto if texto else None


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
                texto_fornecedor = _texto_ou_none('ID do fornecedor (Enter para nenhum): ')
                id_fornecedor = int(texto_fornecedor) if texto_fornecedor is not None else None
                material_service.cadastrar(codigo, nome, quantidade, id_fornecedor)
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
                material_service.consultar(codigo).printar()
                print('(Pressione Enter para manter o valor atual)')
                nome = _texto_ou_none('Novo nome: ')
                texto_fornecedor = _texto_ou_none(
                    'Novo ID do fornecedor (digite "-" para remover o vinculo): '
                )
                desvincular = texto_fornecedor == '-'
                id_fornecedor = (
                    int(texto_fornecedor)
                    if texto_fornecedor is not None and not desvincular
                    else None
                )
                material_service.editar(codigo, nome, id_fornecedor, desvincular)
                print('Material atualizado com sucesso!')
            elif op == '6':
                codigo = input('Digite o codigo do material: ')
                material_service.remover(codigo)
                print('Material removido com sucesso!')
            else:
                print('Opcao invalida!')
        except (
            MaterialJaCadastradoError,
            MaterialNaoEncontradoError,
            MaterialComRetiradasError,
            FornecedorNaoEncontradoError,
            QuantidadeInvalidaError,
            PersistenciaError,
        ) as erro:
            print(f'Erro: {erro}')
        except ValueError:
            print('Erro: valor numerico invalido.')

        return False
