import csv
import json
import time
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

from base_conhecimento import normalizar


CAMPOS = ("data", "origem", "pergunta", "id_orientacao", "encontrou", "ajudou",
          "tentativas", "tempo_segundos")


def escolher(rotulo, opcoes, voltar=True):
    while True:
        print(f"\n{rotulo}")
        for numero, opcao in enumerate(opcoes, 1):
            print(f"{numero}. {opcao}")
        if voltar:
            print("0. Voltar")
        resposta = input("> ").strip()
        if voltar and resposta == "0":
            return 0
        if resposta in map(str, range(1, len(opcoes) + 1)):
            return int(resposta)
        print("Escolha um dos números exibidos.")


def confirmou(rotulo):
    while True:
        valor = input(rotulo + " (s/n): ").strip().lower()
        if valor in ("s", "n"):
            return valor == "s"
        print("Digite s ou n.")


def salvar(caminho, escrever):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(mode="w", encoding="utf-8", newline="", delete=False,
                            dir=caminho.parent) as temporario:
        destino = Path(temporario.name)
        try:
            escrever(temporario)
            temporario.close()
            destino.replace(caminho)
        finally:
            destino.unlink(missing_ok=True)


class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.pasta = base.caminho.parent
        self.bloqueados = set()
        self.historico = self._ler("historico.json", self._registro_valido)
        self.notas = self._ler("facilidade.json", lambda n: type(n) is int and 1 <= n <= 5)

    @staticmethod
    def _registro_valido(r):
        return (isinstance(r, dict) and all(c in r for c in CAMPOS)
                and isinstance(r["pergunta"], str)
                and all(type(r[c]) is bool for c in ("encontrou", "ajudou"))
                and type(r["tentativas"]) is int
                and type(r["tempo_segundos"]) in (int, float))

    def _ler(self, arquivo, validar):
        try:
            itens = json.loads((self.pasta / arquivo).read_text(encoding="utf-8"))
            if not isinstance(itens, list) or not all(map(validar, itens)):
                raise ValueError
            return itens
        except FileNotFoundError:
            return []
        except (ValueError, OSError):
            self.bloqueados.add(arquivo)
            print(f"Confira {arquivo}. O original será preservado; novos dados ficam na sessão.")
            return []

    def _adicionar(self, arquivo, lista, valor):
        lista.append(valor)
        if arquivo not in self.bloqueados:
            try:
                salvar(self.pasta / arquivo, lambda f: json.dump(lista, f, ensure_ascii=False, indent=2))
            except OSError:
                print(f"Falha ao salvar {arquivo}; os dados continuam nesta sessão.")

    def registrar(self, origem, pergunta, item, ajudou, tentativas, inicio):
        registro = dict(data=datetime.now().astimezone().isoformat(timespec="seconds"),
                        origem=origem, pergunta=pergunta, id_orientacao=item.id if item else None,
                        encontrou=item is not None, ajudou=ajudou, tentativas=tentativas,
                        tempo_segundos=round(time.monotonic() - inicio, 1))
        self._adicionar("historico.json", self.historico, registro)

    def _tema_seguro(self, pergunta):
        # Só termos temáticos conhecidos podem ser gravados no disco.
        palavras = set("como onde qual meu minha posso fazer tirar perdi segunda via emitir baixar boleto ônibus transporte passe escolar estágio emprego vacina passaporte bolsa faculdade".split())
        for item in self.base.orientacoes:
            palavras.update(normalizar(" ".join([item.titulo, *item.palavras_chave])).split())
        return " ".join(p for p in normalizar(pergunta).split() if p in palavras) or "[tema fora do vocabulário]"

    def perguntar(self):
        inicio = time.monotonic()
        tentativas = 0
        while True:
            pergunta = input("\nDigite somente o tema da dúvida, sem dados pessoais (0 para voltar): ").strip()
            if pergunta == "0":
                return
            if "@" in pergunta or sum(c.isdigit() for c in pergunta) >= 8:
                print("Não digite CPF, telefone ou e-mail. Reescreva.")
                continue
            if not normalizar(pergunta):
                print("Escreva uma dúvida.")
                continue
            tentativas += 1
            resultados = [(p, o) for p, o in self.base.buscar(pergunta) if p >= 3]
            item = None
            ajudou = False
            if resultados:
                pontos, item = resultados[0]
                print(f"Confiança: {'ALTA' if pontos >= 6 else 'MÉDIA'} ({pontos} pontos)")
                item.exibir()
                for _, alternativa in resultados[1:3]:
                    print(f"Alternativa em {alternativa.categoria}: {alternativa.titulo}")
                ajudou = confirmou("Essa orientação resolveu sua dúvida?")
            else:
                print("Não encontrei. Tente outras palavras ou consulte as categorias.")
            if ajudou or not confirmou("Quer reformular esta mesma dúvida?"):
                self.registrar("pergunta", self._tema_seguro(pergunta), item, ajudou, tentativas, inicio)
                return

    def navegar(self):
        categorias = self.base.categorias()
        inicio = time.monotonic()
        while categorias:
            indice = escolher("Categorias", categorias)
            if not indice:
                return
            itens = self.base.por_categoria(categorias[indice - 1])
            while True:
                indice = escolher("Orientações", [o.titulo for o in itens])
                if not indice:
                    break
                item = itens[indice - 1]
                print("Seleção direta por categoria.")
                item.exibir()
                ajudou = confirmou("Essa orientação resolveu sua dúvida?")
                self.registrar("categoria", item.titulo, item, ajudou, 1, inicio)
                inicio = time.monotonic()
        if not categorias:
            print("Nenhuma categoria disponível.")

    def indicadores(self):
        total = len(self.historico)
        encontrados = [r for r in self.historico if r["encontrou"]]
        resolveu = sum(r["ajudou"] for r in self.historico)
        print(f"\nAtendimentos: {total}")
        if total:
            print(f"Resposta encontrada: {100 * len(encontrados) / total:.1f}%")
            print(f"Taxa de acerto (ajudou): {100 * resolveu / total:.1f}%")
            print(f"Tentativas por atendimento: {sum(r['tentativas'] for r in self.historico) / total:.2f}")
        if encontrados:
            media = sum(r["tempo_segundos"] for r in encontrados) / len(encontrados)
            print(f"Tempo médio dos atendimentos com resposta: {media:.1f} s")
        elif not total:
            print("Sem atendimentos para calcular taxas.")
        else:
            print("Tempo médio: sem respostas encontradas.")
        print("Facilidade média (1–5):", f"{sum(self.notas)/len(self.notas):.2f}" if self.notas else "sem notas")
        pendentes = sorted({r["pergunta"] for r in self.historico if not r["ajudou"]})
        print("Dúvidas sem solução:", ", ".join(pendentes) or "nenhuma registrada")

    def exportar_csv(self):
        if "historico.json" in self.bloqueados:
            print("Recupere o histórico antes de atualizar o CSV.")
            return
        def escrever(arquivo):
            tabela = csv.DictWriter(arquivo, fieldnames=CAMPOS, extrasaction="ignore")
            tabela.writeheader()
            tabela.writerows(self.historico)
        try:
            salvar(self.pasta / "atendimentos.csv", escrever)
            print("CSV exportado em data/atendimentos.csv.")
        except OSError:
            print("Falha ao exportar. Confira as permissões e feche o CSV se estiver aberto.")

    def avaliar(self):
        nota = escolher("Qual foi a facilidade de uso?", ["Muito difícil", "Difícil", "Regular", "Fácil", "Muito fácil"], voltar=False)
        self._adicionar("facilidade.json", self.notas, nota)
