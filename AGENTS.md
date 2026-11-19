# AGENTS.md — Guia para Agentes AI

> Este arquivo orienta qualquer agente de IA (LLM, bot, assistente) que acesse este repositório. Leia antes de fazer qualquer coisa.

## O que é este repositório

`pesquisa_lol` é o corpus de dados de um projeto de pesquisa pessoal da estudante **Lídia Belas** (Antropologia/UFBA), vinculado às disciplinas de **Métodos Digitais** e **Laboratório Quantitativo em Ciências Sociais**. A pesquisa investiga **a associação entre a frequência de expressões potencialmente misóginas nas falas dos vídeos de League of Legends e o número de visualizações** no YouTube, usando o léxico MOL.

O corpus foi coletado do canal do YouTuber **Yiok** (janela: 21/08/2025 a 21/11/2025), incluindo vídeos, transcrições, descrições e comentários.

> ℹ️ Este projeto é de interesse pessoal de pesquisa da Lídia (LoL/gaming), não vinculado ao LABHDUFBA nem ao PIBIC. Não há orientador formal — a pesquisadora conduz o projeto de forma independente.

## Propósito da base

Investigar, em estudo de caso quantitativo e exploratório do canal Yiok, se vídeos com maior frequência de expressões potencialmente misóginas nas transcrições apresentam maior número de visualizações. O léxico MOL é ferramenta de triagem, não classificação contextual definitiva. Preservar reprodutibilidade e rastreabilidade para pesquisa acadêmica. Os comentários e bases derivadas são acervo histórico, **excluído da análise atual**.

## Como lidar com os dados

### Hierarquia léxico ↔ dados

O repositório separa claramente **ferramenta de análise** de **dados brutos**:

- `lexico/` (raiz do repo) — o **léxico MOL** é uma ferramenta de análise, não um dado bruto. Contém a lista de termos e categorias usada para flaggear comentários. Pode ser atualizado, expandido e versionado independentemente dos dados.
- `data/` — todos os **dados da pesquisa**: brutos (vídeos, comentários, transcrições) e analíticos (base analítica com codificação binária).

**Nunca mova o léxico para dentro de `data/`.** Essa separação é uma decisão metodológica da pesquisadora.

### Regras de manejo

- ✅ **Ler e analisar** todos os arquivos do repositório
- ✅ **Atualizar o README.md** e o AGENTS.md quando a estrutura mudar
- ✅ **Adicionar novos dados** (novos vídeos, comentários) dentro de `data/`
- ✅ **Atualizar o léxico** em `lexico/` (acrescentar termos, categorias, versões)
- ✅ **Atualizar a base analítica** (`data/comentarios/base_analitica_mol.csv`) quando o léxico mudar
- ✅ **Criar scripts de análise** (Python, R) desde que não modifiquem os dados originais
- ✅ **Documentar mudanças** em commits claros e descritivos

### O que NÃO fazer

- ❌ **NUNCA usar a conta ou token de terceiros** neste repositório. Use apenas git + deploy key SSH da própria Lídia.
- ❌ **NÃO usar `gh` CLI** neste repositório — apenas `git` + deploy key SSH
- ❌ **NÃO versionar documentos `.docx` de metodologia** (o arquivo enviado pela pesquisadora fica apenas como referência local, não no repo)
- ❌ **NÃO subir áudios `.mp3` maiores que 25 MB** (limite do GitHub)
- ❌ **NÃO modificar ou deletar dados originais** coletados (comentários brutos, transcrições, descrições)
- ❌ **NÃO mover o `lexico/` para dentro de `data/`** — são coisas diferentes
- ❌ **NÃO inventar dados** — se algo não existe no corpus, diga que não existe
- ❌ **NÃO alterar a estrutura de pastas** sem atualizar o README.md e o AGENTS.md
- ❌ **NÃO expor credenciais, tokens, API keys ou deploy keys** em commits, issues ou arquivos do repo

## Estrutura do repositório

```
pesquisa_lol/
├── AGENTS.md                              ← este arquivo (leia primeiro!)
├── README.md                              ← documentação completa do projeto
├── .gitignore
├── lexico/                                ← léxico MOL (ferramenta de análise, NÃO é dado bruto)
│   ├── mol-lexicon.json
│   └── mol-lexicon.csv
├── scripts/                               ← scripts de análise
│   └── analise_lexical.py                    ← aplica léxico MOL em comentários + transcrições
└── data/                                  ← dados da pesquisa (brutos e analíticos)
    ├── data_base yiok - videos.csv        ← base de vídeos (43 linhas, 30+ variáveis YTDT + categoria_video)
    ├── data_base yiok.csv                 ← cópia da base de vídeos (upload via navegador)
    ├── comentarios/                       ← comentários coletados + base analítica
    │   ├── data_base yiok - comentários.csv   ← brutos (1.222 comentários)
    │   ├── base_analitica_mol.csv            ← base analítica (1.222 + codificação binária)
    │   └── comentarios_flagged_mol.csv       ← 61 comentários flagged
    └── videos/                            ← uma pasta por vídeo (43 total)
        └── <videoId>/
            ├── descricao.md               ← metadados + descrição original
            ├── <videoId>.mp3              ← áudio (35 de 43 no repo)
            ├── <videoId>_transcricao.txt  ← transcrição em texto puro
            ├── <videoId>_transcricao.csv  ← transcrição segmentada
            └── <videoId>_metadados_transcricao.txt
```

## Fontes da pesquisa

- **Ativas:** 43 transcrições dos vídeos (fala do criador) e metadados dos vídeos, incluindo visualizações e datas a conferir.
- **Históricas, fora da análise:** 1.222 comentários e tabelas analíticas anteriores. Preservar integralmente os dados originais e não utilizar comentários nos resultados do novo desenho.

## Pergunta de pesquisa e design analítico

> **Qual é a relação entre a frequência de expressões potencialmente misóginas na fala presente nos vídeos de League of Legends e o número de visualizações que esses vídeos alcançam no YouTube?**

**H1:** vídeos com maior frequência de expressões potencialmente misóginas por mil palavras apresentam mais visualizações. **H0:** não há associação entre essas medidas.

**Desenho:** estudo de caso observacional, quantitativo e exploratório do canal Yiok; 43 vídeos publicados entre 21/08/2025 e 21/11/2025; unidade de análise = vídeo (n=43). Investigar associação, **não causalidade**.

**Variáveis:** frequência de ocorrências do léxico MOL por mil palavras da transcrição (indicador lexical sujeito a falsos positivos, gírias, citações e contexto); número de visualizações por vídeo (verificar nome da coluna, data de aferição e valores ausentes).

**Plano:** refinar e validar o léxico nas transcrições; verificar visualizações, datas de publicação e de medição; produzir **nova** base por vídeo sem sobrescrever bases antigas; descrever distribuições, construir dispersão e explorar correlação de Spearman. Considerar diferenças de idade dos vídeos e entre Shorts e vídeos longos; com n=43, interpretar com cautela. Não declarar resultados antes dos cálculos.

**Fora do escopo:** comentários e comparação fala × audiência; estratificação por categoria de vídeo. As cinco categorias já documentadas permanecem arquivadas, mas não integram a análise principal (opção A).

## Referência metodológica citável

**MARTÍNEZ ARRANZ, A.; ZECH, S. T.; BONOTTI, M.** Political Parties and Civility in Parliament: The Case of Australia from 1901 to 2020. *Parliamentary Affairs*, v. 77, n. 2, p. 371–399, 2024. DOI: 10.1093/pa/gsad008. Open Access.

- **Por que é relevante:** usa abordagem lexicon-based para detectar incivilidade (mesma família do MOL). Métrica central = frequência de termos por mil palavras → diretamente aplicável às transcrições deste corpus.
- **Equivalência:** léxico deles (1.383 termos, inglês) ↔ MOL (92 termos, português); corpus Hansard ↔ comentários + transcrições; comparação entre partidos ↔ comparação entre temas de vídeo.
- **Como citar:** na metodologia ("seguindo Martínez Arranz et al., 2024...") e na discussão ("enquanto Martínez Arranz et al. comparam incivilidade entre partidos, este estudo compara misoginia entre tipos de conteúdo...").

## Próximos passos do novo desenho

1. Refinar e validar o léxico MOL no contexto das transcrições.
2. Conferir visualizações e datas nos metadados do YouTube.
3. Criar nova tabela por vídeo: identificador, frequência MOL/mil palavras, visualizações, data de publicação e data de aferição (se disponível).
4. Fazer descrição, dispersão e análise exploratória de associação, com atenção à idade e ao formato dos vídeos.
5. Documentar limitações, sem inferir causalidade. Scripts e bases envolvendo comentários são legados e não devem ser usados como resultados atuais.

## Como eu quero organizar as coisas

- **`lexico/` na raiz** — separado de `data/` porque é ferramenta, não dado
- **`data/` para tudo que é coleta** — vídeos, comentários, transcrições, CSVs brutos e analíticos
- **Uma pasta por vídeo** (`data/videos/<videoId>/`) — preserva a correspondência metadados ↔ áudio ↔ transcrição ↔ comentários
- **`.docx` de metodologia fora do repo** — o documento enviado fica como referência local, não versionado
- **Áudios >25 MB fora do repo** — 8 áudios que excedem o limite do GitHub ficam com a pesquisadora
- **Commits claros** — `feat:`, `fix:`, `refactor:`, `docs:` para manter o histórico legível
- **Deploy key SSH da Lídia** — nunca conta/token de terceiros

## Credenciais e acesso

- **Deploy key SSH:** configurada em `~/.ssh/deploy_key_pesquisa_lol_write` (permissão de escrita)
- **Remote:** `github-pesquisa-lol-write:lidibelas/pesquisa_lol.git`
- **NUNCA** use token ou conta GitHub de terceiros aqui

## Estado atual (redirecionamento metodológico — nov/2026)

- ✅ 43 vídeos e transcrições preservados.
- ✅ 1.222 comentários e análises antigas preservados **fora da análise atual**.
- ✅ Léxico MOL v2 (92 termos / 8 categorias), em refinamento.
- ⏳ Conferir visualizações e datas de coleta.
- ⏳ Criar nova base por vídeo e executar análise exploratória de associação.
- ℹ️ Nenhuma correlação ou resultado novo foi calculado nesta atualização documental.

## Contexto acadêmico

- **Pesquisadora:** Lídia Belas (Antropologia/UFBA)
- **Projeto:** pesquisa pessoal (League of Legends / misoginia em gaming)
- **Disciplinas vinculadas:** Métodos Digitais e Laboratório Quantitativo em Ciências Sociais (UFBA)
- **Orientador:** não há orientador formal — a pesquisadora conduz o projeto de forma independente
- **Ferramenta de coleta:** YouTube Data Tools (ytdt.digitalmethods.net)
- **Léxico:** MOL — Misogyny-Oriented Lexicon (92 termos, 8 categorias)
- **Modelo de dataset:** Fernandez et al. (2025) e Lourenço et al. (2022) — codificação binária por categoria

## Contato

- **Lídia Belas:** responsável pelo repositório (pesquisa pessoal)
- **Tutor Hermes (pibic_labhdufba_bot):** agente de apoio à pesquisa