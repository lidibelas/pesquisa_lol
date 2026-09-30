# AGENTS.md — Guia para Agentes AI

> Este arquivo orienta qualquer agente de IA (LLM, bot, assistente) que acesse este repositório. Leia antes de fazer qualquer coisa.

## O que é este repositório

`pesquisa_lol` é o corpus de dados da pesquisa de iniciação científica **PIBIC 2025–2026** da bolsista **Lídia Belas** no **LABHDUFBA** (Laboratório de Humanidades Digitais da UFBA). A pesquisa investiga **misoginia em comentários de vídeos de League of Legends** no YouTube, usando uma abordagem baseada em léxico (**MOL — Misogyny-Oriented Lexicon**).

O corpus foi coletado do canal do YouTuber **Yiok** (janela: 21/08/2025 a 21/11/2025), incluindo vídeos, transcrições, descrições e comentários.

## Estrutura do repositório

```
pesquisa_lol/
├── AGENTS.md                              ← este arquivo (leia primeiro!)
├── README.md                              ← documentação completa do projeto
├── .gitignore
└── data/                                  ← TODOS os dados da pesquisa
    ├── data_base yiok - videos.csv        ← base de vídeos (43 linhas, 30 variáveis YTDT)
    ├── videos/                            ← uma pasta por vídeo (43 total)
    │   └── <videoId>/
    │       ├── descricao.md               ← metadados + descrição original
    │       ├── <videoId>.mp3              ← áudio (35 de 43 no repo)
    │       ├── <videoId>_transcricao.txt  ← transcrição em texto puro
    │       ├── <videoId>_transcricao.csv  ← transcrição segmentada
    │       └── <videoId>_metadados_transcricao.txt
    ├── comentarios/                       ← comentários coletados + base analítica
    │   ├── data_base yiok - comentários.csv   ← brutos (1.222 comentários)
    │   ├── base_analitica_mol.csv            ← base analítica (1.222 + codificação binária)
    │   └── comentarios_flagged_mol.csv       ← 61 comentários flagged
    └── lexico/                              ← léxico MOL
        ├── mol-lexicon.json
        └── mol-lexicon.csv
```

## O que você PODE fazer

- ✅ **Ler e analisar** todos os arquivos do repositório
- ✅ **Atualizar o README.md** e o AGENTS.md quando a estrutura mudar
- ✅ **Adicionar novos dados** (novos vídeos, comentários, versões do léxico) dentro de `data/`
- ✅ **Criar scripts de análise** (Python, R) desde que não modifiquem os dados originais
- ✅ **Atualizar a base analítica** (`base_analitica_mol.csv`) quando o léxico mudar
- ✅ **Documentar mudanças** em commits claros e descritivos

## O que você NÃO PODE fazer

- ❌ **NUNCA usar a conta ou token do orientador Leonardo (`leofn`)** neste repositório. Use apenas git + deploy key SSH da própria Lídia.
- ❌ **NÃO subir arquivos `.docx`** para o repositório (documentos de metodologia ficam locais)
- ❌ **NÃO subir áudios `.mp3` maiores que 25 MB** (limite do GitHub)
- ❌ **NÃO modificar ou deletar dados originais** coletados (comentários brutos, transcrições, descrições)
- ❌ **NÃO inventar dados** — se algo não existe no corpus, diga que não existe
- ❌ **NÃO alterar a estrutura de pastas** sem atualizar o README.md e o AGENTS.md
- ❌ **NÃO expor credenciais, tokens, API keys ou deploy keys** em commits, issues ou arquivos do repo
- ❌ **NÃO usar `gh` CLI** neste repositório — apenas `git` + deploy key SSH

## Credenciais e acesso

- **Deploy key SSH:** configurada em `~/.ssh/deploy_key_lidibelas_write` (permissão de escrita)
- **Remote:** `github-lidibelas-write:lidibelas/pesquisa_lol.git`
- **NUNKA** use o token ou conta GitHub do orientador aqui

## Estado atual (versão primária — 02/10/2026)

- ✅ 43 vídeos coletados (22 longos + 21 shorts)
- ✅ 1.222 comentários brutos
- ✅ 61 comentários flagged pelo léxico MOL
- ✅ Léxico MOL v2 (92 termos / 8 categorias)
- ✅ Base analítica com codificação binária por categoria
- ⏳ Versão primária — será refinada (MOL + léxico gamer LoL, análise de descrições, multilabel)

## Contexto acadêmico

- **Bolsista:** Lídia Belas (Antropologia/UFBA, LABHDUFBA)
- **Orientador:** Leonardo Fernandes Nascimento (LABHDUFBA)
- **Período:** PIBIC 2025–2026
- **Ferramenta de coleta:** YouTube Data Tools (ytdt.digitalmethods.net)
- **Léxico:** MOL — Misogyny-Oriented Lexicon (92 termos, 8 categorias)
- **Modelo de dataset:** Fernandez et al. (2025) e Lourenço et al. (2022) — codificação binária por categoria

## Contato

- **Lídia Belas:** responsável pelo repositório
- **Leonardo Nascimento:** orientador (LABHDUFBA)
- **Tutor Hermes (pibic_labhdufba_bot):** agente de apoio à pesquisa