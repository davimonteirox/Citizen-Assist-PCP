# Citizen Assist AI | Guia do Eleitor

**Davi Monteiro · RM 573290**  
Global Solution 2026.2 · Pensamento Computacional e Automação com Python

Jovens eleitores que usam os serviços digitais pela primeira vez costumam confundir o número do título, o local de votação e os diferentes comprovantes. O guia orienta em português, pelo terminal, e mostra o caminho oficial para realizar cada serviço. O projeto se relaciona ao ODS 16 pelo acesso à informação pública e ao ODS 10 pela proposta de reduzir barreiras de linguagem. Funciona localmente, sem APIs ou integrações com outras disciplinas.

## Executar

Extraia a pasta inteira, abra o terminal em `citizen-assist-ai` e rode `python main.py` com Python 3.8 ou posterior. No Windows também é possível usar `py main.py`. Não é preciso instalar pacotes. O menu oferece pergunta livre, navegação por categoria, indicadores e exportação. Use 0 para voltar nas listas e 5 para sair do menu principal. Cada pessoa deve encerrar sua sessão e avaliar a facilidade uma vez.

## Organização e decisão técnica

`main.py` monta os objetos e apresenta o menu. Cada dicionário do JSON vira uma `Orientacao`, que sabe exibir seu conteúdo. A `BaseConhecimento` mantém uma lista dessas orientações. O `Assistente` recebe a base, conduz a conversa e salva os atendimentos. A separação permite atualizar um procedimento oficial alterando apenas o JSON. Reinicie o programa para carregar as mudanças.

## Como funciona a busca

O programa remove acentos e pontuação, converte para minúsculas e compara termos inteiros. Cada palavra-chave distinta encontrada como expressão completa vale 3. Cada palavra distinta da pergunta com quatro letras ou mais presente no título vale 1. A busca devolve tuplas (pontos, orientação) em ordem decrescente, com desempate pelo menor ID. A partir de 6 a confiança é alta, entre 3 e 5 é média, abaixo de 3 a resposta é recusada. A tela apresenta a primeira orientação e até duas alternativas que atingiram o mínimo.

Exemplo: “Onde votar? Qual meu local de votação?” ativa as chaves “onde votar” e “local de votação” (+6). “local” e “votação” também aparecem no título (+2). Total de 8, confiança alta. “Onde votar?” sozinha vale 3, confiança média.

## Dados e indicadores

O histórico JSON guarda um registro por atendimento concluído. O CSV pode ser atualizado pelo menu ou ao sair. Uma reformulação conta como outra tentativa no mesmo atendimento. O resultado registrado é o da última tentativa. A navegação direta vale uma tentativa. Cancelar com 0 abandona a interação. O cronômetro monotônico mede até a confirmação do usuário, incluindo leitura e eventuais reformulações.

- Resposta encontrada e taxa de acerto usam todos os atendimentos como denominador. A primeira mede se o guia apresentou orientação; a segunda mede quantos confirmaram que ela ajudou.
- Tempo médio considera só os atendimentos que encontraram orientação. Tentativas médias incluem todos.
- Facilidade é a média das notas de saída, guardadas em `data/facilidade.json`. Cada sessão encerrada pelo menu vale uma nota.
- Dúvidas sem solução incluem as buscas sem resultado e respostas marcadas como pouco úteis.

O programa recusa qualquer pergunta com @ ou oito dígitos no total, mesmo separados. Só palavras presentes no vocabulário permitido são conservadas no histórico. Como consequência, um termo desconhecido pode não aparecer na lista de dúvidas. Durante os testes, anote à parte apenas o assunto omitido. O guia não consulta cadastros, não verifica a identidade do usuário e não confirma a situação individual de ninguém. A confiança mede coincidência textual. A base precisa de revisão quando o TSE muda seus serviços. Use uma instância por pasta de dados.

## Teste com usuários

**Situação: coleta externa pendente.** Os arquivos de entrega começam vazios. Antes da gravação, use esta cópia exclusivamente com pelo menos três pessoas de fora da equipe. Distribua quatro atendimentos para a primeira pessoa e três para cada uma das outras. Peça que formulem as dúvidas com as próprias palavras, experimentem as categorias e incluam um tema que esperariam encontrar. Após cada resposta, a própria pessoa decide se ajudou. Encerre pelo menu para colher a nota. Não anote nomes.

Após as três sessões, reabra o programa, consulte os indicadores e preencha a tabela abaixo. Registre uma dificuldade observada, implemente uma mudança no código ou no JSON e repita a pergunta em uma cópia separada. Assim o reteste não altera os números da coleta inicial. Exporte o CSV da coleta e inclua os dados anônimos na entrega.

| Medida | Resultado da coleta |
|---|---|
| Pessoas externas / atendimentos | A preencher |
| Respostas encontradas (%) | A preencher |
| Respostas que ajudaram (%) | A preencher |
| Tempo médio com resposta (s) | A preencher |
| Tentativas médias | A preencher |
| Facilidade média (1 a 5) | A preencher |
| Dúvidas sem solução | A preencher |
| Melhoria aplicada, motivo e resultado antes/depois | A preencher |

## Fontes oficiais consultadas em 19/11/2026

- [Número do título e local de votação](https://www.tse.jus.br/institucional/corregedoria-geral-eleitoral/sistemas-e-servicos-1/consulta-titulo-e-local-de-votacao)
- [Situação do título](https://www.tse.jus.br/comunicacao/noticias/2026/Abril/eleitor-em-dia-saiba-como-verificar-se-seu-titulo-esta-regular-1)
- [Quitação eleitoral](https://www.tse.jus.br/comunicacao/noticias/2025/Outubro/eleitor-em-dia-saiba-como-emitir-a-certidao-de-quitacao-eleitoral-de-forma-pratica-e-segura)
- [Certidões e declarações](https://www.tse.jus.br/servicos-eleitorais/certidoes/certidoes)
- [Serviços do e-Título](https://www.tse.jus.br/servicos-eleitorais/e-titulo-perguntas-frequentes/2-quais-servicos-voce-encontra-no-e-titulo)
- [Dúvidas frequentes da Ouvidoria](https://www.tse.jus.br/servicos-eleitorais/servicos/ouvidoria-tse)

## Vídeo técnico

Link do YouTube: (https://youtu.be/UOeWEejFThM)
