"""Ponto de entrada do sistema de almoxarifado."""

from aplicacao import Aplicacao
from interface.menus.menu_principal import Op_MenuInit


def main() -> None:
    """Abre a aplicação (e a sessão do banco) e inicia o menu principal."""
    with Aplicacao() as aplicacao:
        menu = Op_MenuInit(aplicacao)
        menu.exibir_menu_especial()


if __name__ == '__main__':
    main()
