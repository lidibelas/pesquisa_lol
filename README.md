# Pesquisa LoL — Corpus Yiok

Corpus de vídeos, transcrições e comentários do canal **Yiok** (League of Legends) para pesquisa sobre **misoginia online em jogos**, usando abordagem **MOL (Misoginia Online em Léxico)**.

> 📄 O documento metodológico completo (diário metodológico) fundamenta este README. O arquivo `.docx` original não é versionado no repositório.

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
├── README.md                              ← este arquivo
├── .gitignore
├── comentarios/                           ← comentários coletados
│   └── comentarios_flagged_mol.csv        ← 61 comentários flagged (MOL)
├── lexico/                                ← léxico MOL
│   ├── mol-lexicon.json
│   └── mol-lexicon.csv
└── videos/                                ← uma pasta por vídeo (43 total)
    └── <videoId>/
        ├── descricao.md                   ← metadados + descrição original
        ├── <videoId>.mp3                  ← áudio do vídeo (35 de 43 no repo; 8 mantidos localmente pela pesquisadora)
        ├── <videoId>_transcricao.txt      ← transcrição em texto puro
        ├── <videoId>_transcricao.csv      ← transcrição segmentada (start, end, text)
        ├── <videoId>_metadados_transcricao.txt ← parâmetros da transcrição
        └──                                ← (.gitkeep removido; pastas sem mp3 mantêm os demais arquivos)
```

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

### Criador do conteúdo

- **Yiok** — YouTuber de League of Legends, criador dos vídeos que compõem este corpus

## 📄 Licença

Este repositório contém dados de pesquisa acadêmica. Os vídeos e áudios pertencem ao canal Yiok. As transcrições e análises são de uso acadêmico.

## 📌 Status

**Base de dados em construção.**

- ✅ 43 pastas por videoId com descrição, transcrição e metadados
- ✅ 35 áudios `.mp3` no repositório (8 mantidos localmente pela pesquisadora)
- ✅ Léxico MOL (92 termos / 8 categorias)
- ✅ 61 comentários flagged (MOL)
- 🟡 Pendente: CSV completo dos 1.222 comentários brutos