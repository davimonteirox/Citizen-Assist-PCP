from dataclasses import dataclass


@dataclass
class Orientacao:
    id: int
    categoria: str
    titulo: str
    palavras_chave: list
    resposta: str
    documentos: list
    onde: str
    fonte: str
    verificado_em: str

    def exibir(self):
        print(f"\n{self.titulo} [{self.categoria}]\n{self.resposta}")
        print("Documentos ou dados necessários:")
        for documento in self.documentos:
            print(f"  - {documento}")
        print(f"Onde: {self.onde}\nFonte: {self.fonte}")
        print(f"Verificado em: {self.verificado_em}")
        print("Aviso: este assistente não é canal oficial.")
