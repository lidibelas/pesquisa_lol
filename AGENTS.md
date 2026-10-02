# AGENTS.md — Guia para Agentes AI

> Este arquivo orienta qualquer agente de IA (LLM, bot, assistente) que acesse este repositório. Leia antes de fazer qualquer coisa.

## O que é este repositório

`pesquisa_lol` é o corpus de dados de um projeto de pesquisa pessoal da estudante **Lídia Belas** (Antropologia/UFBA), vinculado às disciplinas de **Métodos Digitais** e **Laboratório Quantitativo em Ciências Sociais**. A pesquisa investiga **misoginia em comentários de vídeos de League of Legends** no YouTube, usando uma abordagem baseada em léxico (**MOL — Misogyny-Oriented Lexicon**).

O corpus foi coletado do canal do YouTuber **Yiok** (janela: 21/08/2025 a 21/11/2025), incluindo vídeos, transcrições, descrições e comentários.

> ℹ️ Este projeto é de interesse pessoal de pesquisa da Lídia (LoL/gaming), não vinculado ao LABHDUFBA nem ao PIBIC. Não há orientador formal — a pesquisadora conduz o projeto de forma independente.

## Propósito da base

Esta base de dados serve como **corpus de pesquisa** para:

1. **Detectar misoginia** em comentários de vídeos de LoL no YouTube por abordagem léxico (MOL)
2. **Mapear categorias** de discurso misógino (xingamentos de gênero, body shaming, sexual degradante, racial interseccional, etc.)
3. **Produzir evidência empírica** para análise antropológica sobre violência de gênero em espaços digitais de gaming
4. **Servir de base para um artigo acadêmico futuro** — por isso a documentação precisa estar completa e bem organizada, garantindo reprodutibilidade e rastreabilidade metodológica
5. **Cumprir exigências das disciplinas** de Métodos Digitais e Laboratório Quantitativo em Ciências Sociais (UFBA)

A base segue o modelo de codificação binária por categoria inspirado em **Fernandez et al. (2025)** e **Lourenço et al. (2022)**: cada comentário = 1 linha, cada categoria do léxico = 1 coluna com valor 1 (presente) ou 0 (ausente).

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
└── data/                                  ← dados da pesquisa (brutos e analíticos)
    ├── data_base yiok - videos.csv        ← base de vídeos (43 linhas, 30 variáveis YTDT)
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

## As duas fontes do corpus

O corpus contém **duas fontes textuais distintas** — ambas analisáveis com o léxico MOL:

1. **Comentários** (`data/comentarios/`) — o que a audiência escreve. 1.222 comentários, 61 flagged (5,0%). Métrica: flag binário (1/0).
2. **Transcrições** (`data/videos/<videoId>/<videoId>_transcricao.txt`) — o que o Yiok diz nos vídeos. 43 transcrições, 81.553 palavras totais, 24 com misoginia detectada (55,8%). Métrica: frequência de termos por mil palavras.

> As transcrições são uma **segunda fonte analítica**, não um complemento. Permitem comparar a linguagem do criador de conteúdo com a linguagem da audiência.

## Opções de análise comparativa dentro da base

A base atual permite comparações internas (correlação, não apenas descrição). As opções viáveis mapeadas são:

1. **Tema do vídeo × misoginia nos comentários** — classificar vídeos por tipo de conteúdo (gameplay neutro / treta / relacionamento) e comparar proporção de comentários misóginos. VI: tema; VD: flag MOL. Teste: qui-quadrado + odds ratio.
2. **Discurso do vídeo × discurso dos comentários** — aplicar MOL às 43 transcrições e comparar misoginia na fala do Yiok com misoginia nos comentários. Métrica das transcrições: freq/mil palavras (mesma do artigo de Martínez Arranz et al., 2024).
3. **Engajamento × misoginia** — comparar likeCount entre comentários flagged e não-flagged. Teste: t-test ou Mann-Whitney.
4. **Categorias MOL × tipo de vídeo** — analisar se certas categorias (body shaming, racial, gamer misógino, etc.) são mais frequentes em certos tipos de vídeo. Teste: qui-quadrado por categoria ou análise de correspondência.

> ⚠️ Estas opções serão executadas **após o refinamento do léxico MOL**, que é a prioridade atual. Nenhuma análise estatística formal foi realizada ainda — as opções estão registradas para planejamento.

## Referência metodológica citável

**MARTÍNEZ ARRANZ, A.; ZECH, S. T.; BONOTTI, M.** Political Parties and Civility in Parliament: The Case of Australia from 1901 to 2020. *Parliamentary Affairs*, v. 77, n. 2, p. 371–399, 2024. DOI: 10.1093/pa/gsad008. Open Access.

- **Por que é relevante:** usa abordagem lexicon-based para detectar incivilidade (mesma família do MOL). Métrica central = frequência de termos por mil palavras → diretamente aplicável às transcrições deste corpus.
- **Equivalência:** léxico deles (1.383 termos, inglês) ↔ MOL (92 termos, português); corpus Hansard ↔ comentários + transcrições; comparação entre partidos ↔ comparação entre temas de vídeo.
- **Como citar:** na metodologia ("seguindo Martínez Arranz et al., 2024...") e na discussão ("enquanto Martínez Arranz et al. comparam incivilidade entre partidos, este estudo compara misoginia entre tipos de conteúdo...").

## O que eu pretendo fazer no futuro

A versão atual é **primária** (entrega de 02/10/2026). A prioridade é refinar o léxico antes de qualquer análise estatística. Os próximos passos planejados são:

1. **Refinar o léxico MOL** com termos específicos da comunidade de League of Legends (gamer slang, gírias do jogo) — **prioridade atual, bloqueia as análises abaixo**
2. **Recodificar os 43 vídeos** com coluna `tema_video` (gameplay neutro / treta / relacionamento) — necessária para a Opção 1
3. **Aplicar o léxico MOL às 43 transcrições** e gerar `base_transcricoes_mol.csv` — necessária para a Opção 2
4. **Rodar análise estatística formal** (qui-quadrado, odds ratio, correlação de Pearson) após refinamento do léxico
5. **Analisar as descrições dos 43 vídeos** — fonte ainda inexplorada
6. **Evoluir da codificação binária para análise multilabel** mais granular
7. **Atualizar colunas de transcrição** (`transcrição_ytb`, `status-transcricao`) com resultados do faster-whisper
8. **Baixar e armazenar o PDF** do artigo de Martínez Arranz et al. (2024) como referência metodológica

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

## Estado atual (versão primária — 02/10/2026)

- ✅ 43 vídeos coletados (22 longos + 21 shorts)
- ✅ 1.222 comentários brutos
- ✅ 61 comentários flagged pelo léxico MOL
- ✅ Léxico MOL v2 (92 termos / 8 categorias)
- ✅ Base analítica com codificação binária por categoria
- ✅ 43 transcrições (Whisper large-v3) — segunda fonte analítica identificada
- ✅ Opções de análise comparativa interna mapeadas (4 opções)
- ✅ Referência metodológica citável registrada (Martínez Arranz et al., 2024)
- ⏳ Léxico MOL em refinamento (prioridade atual) — análise estatística bloqueada até conclusão
- ⏳ Versão primária — será refinada (MOL + léxico gamer LoL, análise de transcrições, análise estatística)

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