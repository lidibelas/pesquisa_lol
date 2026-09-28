# Pesquisa LoL — Corpus Yiok

Corpus de vídeos, transcrições e comentários do canal **Yiok** (League of Legends) para pesquisa sobre **misoginia online em jogos**, usando abordagem **MOL (Misoginia Online em Léxico)**.

## 📋 Visão geral

- **Canal**: Yiok (`UC_GFcLxFl1WhIOpZTzf9FSg`)
- **Total de vídeos**: 43 (22 longos + 21 shorts)
- **Período de coleta**: 21/08/2025 – 20/11/2025
- **Total de comentários**: 1.222
- **Total de views**: 418.042
- **Transcrições**: 43 (Whisper large-v3 via faster-whisper)

## 📁 Estrutura do repositório

```
pesquisa_lol/
├── README.md                              ← este arquivo
├── .gitignore
├── comentarios/                           ← comentários coletados (a adicionar)
├── lexico/                                ← léxico MOL (a adicionar)
└── videos/                                ← uma pasta por vídeo (43 total)
    └── <videoId>/
        ├── descricao.md                   ← metadados + descrição original
        ├── <videoId>.mp3                  ← áudio do vídeo (35 disponíveis)
        ├── <videoId>_transcricao.txt      ← transcrição em texto puro
        ├── <videoId>_transcricao.csv      ← transcrição segmentada (start, end, text)
        ├── <videoId>_metadados_transcricao.txt ← parâmetros da transcrição
        └── .gitkeep                       ← placeholder (quando áudio ainda não subido)
```

## 🔬 Metodologia

### 1. Coleta dos vídeos

Os vídeos do canal Yiok foram identificados manualmente a partir da lista pública do canal, filtrando o período de **21/08/2025 a 20/11/2025** (3 meses). Foram selecionados todos os 43 vídeos publicados nesse intervalo, incluindo vídeos longos (streams, gameplays, guias) e shorts.

### 2. Coleta dos comentários

Os comentários foram coletados utilizando a ferramenta **YouTube Data Tools** ([ytdt.digitalmethods.net](https://ytdt.digitalmethods.net)), desenvolvida por **Bernhard Rieder** (University of Amsterdam). A ferramenta permite extrair comentários, metadados e dados de engajamento de vídeos do YouTube via API oficial.

### 3. Download dos áudios

Os áudios dos vídeos foram baixados utilizando o **Parabolic** ([github.com/NickvisionApps/Parabolic](https://github.com/NickvisionApps/Parabolic)), um frontend open-source do `yt-dlp` desenvolvido pela **Nickvision** (contribuidor principal: **nlogozzo**), sob licença MIT. 

> *"Um santo que me salvou."* — Lídia Belas, sobre o criador do Parabolic 🙏

### 4. Transcrição automática

As transcrições foram geradas com **faster-whisper** ([github.com/SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper)), uma implementação otimizada do Whisper usando CTranslate2.

**Parâmetros utilizados:**

- **Modelo**: `Whisper large-v3`
- **Idioma**: `pt`
- **Device**: `cuda` (GPU)
- **Compute type**: `float16`
- **Beam size**: `5`
- **VAD filter**: `True`
- **condition_on_previous_text**: `False`

Cada transcrição gera três arquivos:

- **`.txt`** — texto puro contínuo
- **`.csv`** — segmentos com timestamps (`start`, `end`, `text`)
- **`_metadados_transcricao.txt`** — parâmetros e estatísticas da transcrição

### 5. Análise léxico (MOL)

A detecção de misoginia utiliza a abordagem **MOL (Misoginia Online em Léxico)**, combinando:

- **HurtLex PT** — léxico de discurso de ódio com categorias misóginas
- **Termos emergentes** — vocabulário observado empiricamente na comunidade de League of Legends, acrescentado pela pesquisadora a partir de sua experiência como jogadora

O léxico MOL final contém **92 termos** distribuídos em **8 categorias**, aplicados aos 1.222 comentários do corpus.

## 🙏 Créditos e agradecimentos

### Criadores das ferramentas

- **Bernhard Rieder** — YouTube Data Tools (coleta de comentários)
- **Nickvision / nlogozzo** — [Parabolic](https://github.com/NickvisionApps/Parabolic) (download de áudio, frontend do yt-dlp)
- **SYSTRAN** — [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (transcrição automática)
- **OpenAI** — Whisper large-v3 (modelo de transcrição)

### Criador do conteúdo

- **Yiok** — YouTuber de League of Legends, criador dos vídeos que compõem este corpus

## 📄 Licença

Este repositório contém dados de pesquisa acadêmica. Os vídeos e áudios pertencem ao canal Yiok. As transcrições e análises são de uso acadêmico.

## 📌 Status

**Em construção** — ver [Issues](https://github.com/lidibelas/pesquisa_lol/issues) para pendências.