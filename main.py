from pathlib import Path

from assistente import Assistente, escolher
from base_conhecimento import BaseConhecimento


def main():
    base = BaseConhecimento(Path(__file__).parent / "data/base_conhecimento.json")
    base.carregar()
    assistente = Assistente("Citizen Assist AI — Guia do Eleitor", base)
    print(assistente.nome, "\nEste assistente não é canal oficial. Não informe dados pessoais.")
    acoes = [assistente.perguntar, assistente.navegar, assistente.indicadores, assistente.exportar_csv]
    while True:
        opcao = escolher("Menu principal", ["Fazer pergunta", "Explorar categorias", "Ver indicadores", "Exportar CSV", "Sair"], voltar=False)
        if opcao == 5:
            assistente.avaliar()
            assistente.exportar_csv()
            break
        acoes[opcao - 1]()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSessão encerrada.")
