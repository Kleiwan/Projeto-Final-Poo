from interface.tela import Tela
class Tela_Retirada(Tela):
    @staticmethod
    def exibir_tela():
        print("\\n========= MENU DE MOVIMENTAÇÕES =========")
        print("[1] Registrar retirada")
        print("[2] Listar retiradas")
        print("[3] Consultar retiradas")
        print("[4] Consultar por funcionário")
        print("[5] Consultar por material")
        print("[6] Consultar estoque")
        print("[7] Registrar entrada/reposição")
        print("[8] Listar entradas")
        print("[0] Voltar")
