# Pesquisa LoL — Corpus Yiok

Corpus de vídeos, transcrições e comentários do canal **Yiok** (League of Legends) para pesquisa sobre **misoginia online em jogos**, usando abordagem **MOL (Misoginia Online em Léxico)**.


## 📋 Visão geral

- **Canal**: Yiok (`UC_GFcLxFl1WhIOpZTzf9FSg`)
- **Total de vídeos**: 43 (22 longos + 21 shorts)
- **Período de coleta**: 21/08/2025 – 21/11/2025
- **Total de comentários**: 1.222
- **Total de views**: 418.042
- **Transcrições**: 43 (Whisper large-v3 via faster-whisper)

## 📁 Estrutura do repositório

```
pesquisa_lol/
├── AGENTS.md                              ← guia para agentes de IA (leia antes de operar o repo)
├── README.md                              ← este arquivo
├── .gitignore
├── lexico/                                ← léxico MOL (ferramenta de análise, NÃO é dado bruto)
│   ├── mol-lexicon.json
│   └── mol-lexicon.csv
└── data/                                  ← dados da pesquisa (brutos e analíticos)
    ├── data_base yiok - videos.csv        ← base de vídeos (43 linhas, 30 variáveis do YTDT)
    ├── data_base yiok.csv                 ← cópia da base de vídeos (upload via navegador)
    ├── comentarios/                       ← comentários coletados e base analítica
    │   ├── data_base yiok - comentários.csv   ← base completa de comentários brutos (1.222)
    │   ├── base_analitica_mol.csv             ← base analítica unificada (1.222 + codificação binária MOL)
    │   └── comentarios_flagged_mol.csv        ← 61 comentários flagged (MOL)
    └── videos/                            ← uma pasta por vídeo (43 total)
        └── <videoId>/
            ├── descricao.md                   ← metadados + descrição original
            ├── <videoId>.mp3                  ← áudio do vídeo (35 de 43 no repo; 8 >25 MB mantidos localmente)
            ├── <videoId>_transcricao.txt      ← transcrição em texto puro
            ├── <videoId>_transcricao.csv      ← transcrição segmentada (start, end, text)
            └── <videoId>_metadados_transcricao.txt ← parâmetros da transcrição
```

> 🔑 **Sobre a separação léxico ↔ dados:** o `lexico/` fica **na raiz**, fora de `data/`. O léxico é uma **ferramenta de análise** (lista de termos e categorias usada para detectar misoginia), não um dado bruto coletado do YouTube. Os dados brutos e analíticos ficam em `data/`.

## 🔬 Metodologia

### 1. Coleta e delimitação do corpus — YouTube Data Tools v2

A construção inicial do corpus foi realizada por meio do **YouTube Data Tools (YTDT)**, desenvolvido por **Bernhard Rieder** no âmbito da Digital Methods Initiative. A ferramenta utiliza a API v3 do YouTube e foi projetada especificamente para coleta de dados de pesquisa.

Inicialmente, utilizou-se o módulo **Channel Info** para identificação do canal do Yiok. Posteriormente, utilizou-se o módulo **Video List**, que gera uma tabela em que cada linha corresponde a um vídeo e contém metadados e métricas: identificador único do vídeo (`videoId`), título, data de publicação, duração, número de visualizações, likes e comentários.

A delimitação do corpus foi realizada a partir de um critério **exclusivamente temporal**, considerando os vídeos publicados entre **21 de agosto e 21 de novembro de 2025**. A definição prévia dessa janela busca preservar o caráter exploratório da pesquisa e evitar a seleção de conteúdos a partir da identificação antecipada de falas ou temáticas relacionadas à violência de gênero.

> 🔑 **Decisão metodológica**: os vídeos não foram selecionados porque pareciam conter misoginia. O critério foi exclusivamente temporal, definido antes da análise dos conteúdos.

### 2. Preparação dos vídeos para transcrição — Parabolic

Como os vídeos não apresentavam legendas/transcrições disponíveis, optou-se por produzir transcrições próprias a partir das faixas de áudio.

Para a extração dos áudios, utilizou-se o **Parabolic** ([github.com/NickvisionApps/Parabolic](https://github.com/NickvisionApps/Parabolic)), um aplicativo de código aberto que funciona como interface gráfica para o `yt-dlp`. Os arquivos são extraídos em formato MP3, mantendo-se no nome do arquivo o `videoId` fornecido pelo YouTube. Essa estratégia permite preservar a correspondência entre metadados ↔ áudio ↔ transcrição ↔ comentários.

**Versões técnicas registradas no primeiro teste bem-sucedido:**

- yt-dlp: versão 2026.08.19
- Deno: 2.9.7
- FFmpeg: n8.1.1-8-gb21e00eda5-20260524

> 💡 Deno e FFmpeg são dependências técnicas do processo, registradas para reprodutibilidade.

### 3. Transcrição automática — faster-whisper

As transcrições foram geradas com **faster-whisper** ([github.com/SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper)), uma reimplementação do modelo Whisper (OpenAI) usando CTranslate2, que busca executar a inferência com menor consumo de memória e maior velocidade.

**Parâmetros utilizados:**

- **Modelo**: `Whisper large-v3`
- **Idioma**: `pt` (fixado)
- **Device**: `cuda` (GPU)
- **Compute type**: `float16`
- **Beam size**: `5`
- **VAD filter**: `True`
- **condition_on_previous_text**: `False`

Cada transcrição gera três arquivos:

- **`.txt`** — texto puro contínuo
- **`.csv`** — segmentos com timestamps (`start`, `end`, `text`)
- **`_metadados_transcricao.txt`** — parâmetros e estatísticas da transcrição

### 4. Análise léxico (MOL)

A detecção de misoginia utiliza a abordagem **MOL (Misoginia Online em Léxico)**, combinando:

- **HurtLex PT** — léxico de discurso de ódio com categorias misóginas
- **Termos emergentes** — vocabulário observado empiricamente na comunidade de League of Legends, acrescentado pela pesquisadora a partir de sua experiência como jogadora

O léxico MOL final contém **92 termos** distribuídos em **8 categorias**, aplicados aos 1.222 comentários do corpus.

### 5. Base analítica — codificação binária por categoria

A base analítica (`data/comentarios/base_analitica_mol.csv`) reúne os 1.222 comentários em uma única tabela com codificação binária (1 = presença / 0 = ausência) para cada uma das 8 categorias do léxico MOL, seguindo o modelo de datasets acadêmicos com codificação categorial (cf. Fernandez, Bertholini e Maia, 2025; Lourenço, Vitena e Silva, 2022).

**Estrutura da base analítica (17 colunas):**

| Coluna | Descrição |
|--------|-----------|
| `videoId` | ID do vídeo no YouTube |
| `comment_id` | ID único do comentário |
| `text` | Texto do comentário |
| `publishedAt` | Data de publicação |
| `likeCount` | Número de likes |
| `isReply` | Se é resposta (true/false) |
| `flag_mol` | 1 se ≥1 termo MOL encontrado, 0 caso contrário |
| `n_matches` | Número de termos do léxico encontrados |
| `cat_xingamentos_genero` | 1/0 — xingamentos de gênero |
| `cat_genitalia_feminina` | 1/0 — referências a genitália feminina |
| `cat_body_shaming` | 1/0 — depreciação corporal |
| `cat_gamer_misogino` | 1/0 — termos misóginos da cultura gamer |
| `cat_homofobia_misoginia` | 1/0 — homofobia + misoginia |
| `cat_sexual_degradante` | 1/0 — linguagem sexual degradante |
| `cat_prostituicao_degradante` | 1/0 — depreciação via prostituição |
| `cat_racial_interseccional` | 1/0 — interseccionalidade raça/gênero |
| `termos_encontrados` | Lista dos termos que bateram |

**Distribuição dos 61 comentários flagged por categoria:**

| Categoria | Comentários |
|-----------|-------------|
| racial_interseccional | 18 |
| body_shaming | 14 |
| sexual_degradante | 13 |
| xingamentos_genero | 11 |
| gamer_misogino | 7 |
| genitalia_feminina | 1 |
| homofobia_misoginia | 1 |
| prostituicao_degradante | 0 |

> ⚠️ **Versão primária.** Esta é a versão inicial da base de dados, entregue como primeira versão da entrega prevista para 02/10/2026. A codificação por flag binário (presença/ausência) é um modelo provisório que ainda será refinado em etapas futuras.


## 🙏 Créditos e referências

### Software e ferramentas

| Ferramenta | Citar no artigo? | Como citar |
|------------|-------------------|------------|
| YouTube Data Tools | Sim, obrigatório | Rieder (2015) |
| Parabolic | Sim | Software/projeto NickvisionApps |
| yt-dlp | Sim | Repositório/software |
| Whisper | Sim | Radford et al. (2023) |
| faster-whisper | Sim | Software/repositório SYSTRAN |
| Google Colab | Não essencial | Mencionar o ambiente |
| FFmpeg | Não essencial | Registrar tecnicamente |
| Deno | Não essencial | Registrar tecnicamente |

### Referências

- **RIEDER, Bernhard.** YouTube Data Tools. Version 2.0. 2015. Software.
- **RADFORD, Alec; KIM, Jong Wook; XU, Tao; BROCKMAN, Greg; MCLEAVEY, Christine; SUTSKEVER, Ilya.** Robust Speech Recognition via Large-Scale Weak Supervision. *Proceedings of the 40th International Conference on Machine Learning*, v. 202, p. 28492–28518, 2023.
- **FERNANDEZ, Michelle; BERTHOLINI, Frederico; MAIA, Bárbara.** Políticas de saúde dos Estados brasileiros durante a pandemia de Covid-19: um dataset das normativas produzidas. *Dados*, Rio de Janeiro, v. 68, n. 3, e20230153, 2025.
- **LOURENÇO, Luiz Claudio; VITENA, Gabrielle Simões Lima; SILVA, Marina de Macedo.** Prisão provisória, racismo e seletividade penal: uma discussão a partir dos prontuários de uma unidade prisional. *Revista Brasileira de Segurança Pública*, v. 16, n. 2, p. 220–239, 2022.

### Criador do conteúdo

- **Yiok** — YouTuber de League of Legends, criador dos vídeos que compõem este corpus

## 📄 Licença

Este repositório contém dados de pesquisa acadêmica. Os vídeos e áudios pertencem ao canal Yiok. As transcrições e análises são de uso acadêmico.

## 📌 Status

**Versão primária da base de dados** — primeira versão da entrega prevista para 02/10/2026. A base está funcional mas ainda será refinada em etapas futuras.

- ✅ 43 pastas por videoId com descrição, transcrição e metadados
- ✅ 35 áudios `.mp3` no repositório (8 mantidos localmente pela pesquisadora)
- ✅ Léxico MOL v2 (92 termos / 8 categorias)
- ✅ Base de vídeos (`data/data_base yiok - videos.csv`) — 43 vídeos, 30 variáveis do YTDT
- ✅ 1.222 comentários brutos (`data/comentarios/data_base yiok - comentários.csv`)
- ✅ Base analítica unificada (`data/comentarios/base_analitica_mol.csv`) — 1.222 comentários + codificação binária por categoria
- ✅ 61 comentários flagged (MOL)


### 🔜 Próximos passos previstos

- [ ] Refinar o léxico MOL com termos específicos da comunidade de League of Legends (gamer slang)
- [ ] Analisar também as descrições dos 43 vídeos
- [ ] Evoluir da codificação binária para análise multilabel mais granular
- [ ] Atualizar colunas de transcrição (`transcrição_ytb`, `status-transcricao`) com resultados do faster-whisper