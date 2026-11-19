import json
import re
import unicodedata
from datetime import date
from pathlib import Path

from orientacao import Orientacao


def normalizar(texto):
    letras = unicodedata.normalize("NFD", texto.casefold())
    simples = "".join(c for c in letras if not unicodedata.combining(c))
    return " ".join(re.findall(r"[^\W_]+", simples))


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.orientacoes = []

    def carregar(self):
        try:
            dados = json.loads(self.caminho.read_text(encoding="utf-8"))
            registros = [Orientacao(**item) for item in dados]
            ids = set()
            for item in registros:
                if type(item.id) is not int or item.id in ids:
                    raise ValueError("ID inválido ou duplicado")
                ids.add(item.id)
                for campo, valor in vars(item).items():
                    if campo in ("palavras_chave", "documentos"):
                        if not isinstance(valor, list) or not valor or not all(isinstance(v, str) and v.strip() for v in valor):
                            raise ValueError(campo)
                    elif campo != "id" and not (isinstance(valor, str) and valor.strip()):
                        raise ValueError(campo)
                date.fromisoformat(item.verificado_em)
            self.orientacoes = registros
        except (OSError, ValueError, TypeError) as erro:
            print(f"Base indisponível. Confira o arquivo {self.caminho.name}. ({type(erro).__name__})")

    def categorias(self):
        return sorted({o.categoria for o in self.orientacoes})

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        texto = normalizar(pergunta)
        chaves = {normalizar(c) for c in orientacao.palavras_chave}
        pontos = sum(3 for chave in chaves if f" {chave} " in f" {texto} ")
        comuns = set(texto.split()) & set(normalizar(orientacao.titulo).split())
        return pontos + sum(1 for palavra in comuns if len(palavra) >= 4)

    def buscar(self, pergunta):
        resultados = [(self.pontuar(pergunta, item), item) for item in self.orientacoes]
        return sorted(resultados, key=lambda par: (-par[0], par[1].id))
