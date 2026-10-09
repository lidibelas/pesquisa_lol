# Pesquisa LoL — Corpus Yiok

Corpus de vídeos, transcrições e comentários do canal **Yiok** (League of Legends) para pesquisa sobre **misoginia online em jogos**, usando abordagem **MOL (Misoginia Online em Léxico)**.

> ℹ️ **Sobre este projeto:** projeto de pesquisa pessoal da estudante **Lídia Belas** (Antropologia/UFBA), vinculado às disciplinas de **Métodos Digitais** e **Laboratório Quantitativo em Ciências Sociais**. Não há orientador formal — a pesquisadora conduz o projeto de forma independente. O propósito de toda a documentação é garantir reprodutibilidade e rastreabilidade metodológica para um futuro artigo acadêmico.


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
├── scripts/                               ← scripts de análise
│   └── analise_lexical.py                    ← aplica léxico MOL em comentários + transcrições
└── data/                                  ← dados da pesquisa (brutos e analíticos)
    ├── data_base yiok - videos.csv        ← base de vídeos (43 linhas, 30+ variáveis do YTDT + categoria_video)
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

O léxico MOL atual contém **92 termos** distribuídos em **8 categorias**, aplicados aos 1.222 comentários do corpus.

> ⚠️ **Versão preliminar.** O léxico MOL está em refinamento. Os números de detecção podem mudar significativamente com a melhoria do léxico.

### 5. Base analítica — codificação binária por categoria

A base analítica (`data/comentarios/base_analitica_mol.csv`) reúne os 1.222 comentários em uma única tabela com codificação binária (1 = presença / 0 = ausência) para cada uma das 8 categorias do léxico MOL, seguindo o modelo de datasets acadêmicos com codificação categorial (cf. Fernandez, Bertholini e Maia, 2025; Lourenço, Vitena e Silva, 2022).

**Estrutura da base analítica:**

| Coluna | Descrição |
|--------|-----------|
| `videoId` | ID do vídeo no YouTube |
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

> ⚠️ **Versão preliminar.** Esta é a versão inicial da base de dados. O léxico ainda será refinado e os números de detecção podem mudar.


## 🎬 Categorização dos vídeos

Os 43 vídeos do corpus foram classificados em **5 categorias de conteúdo** com base na análise dos títulos, descrições e transcrições. Esta categorização permite investigar se **diferentes tipos de conteúdo** geram **diferentes padrões de misoginia** nos comentários.

### Como as categorias foram definidas

A categorização foi feita por **análise indutiva do conteúdo** — cada vídeo foi classificado a partir do que de fato apresenta, não a partir de uma grade pré-fixada. Os critérios foram:

1. **Objetivo principal do vídeo** — o que o criador estava tentando fazer? (jogar, ensinar,entreter, narrar conflito)
2. **Estrutura narrativa** — é uma partida completa? Um clipe curto? Um tutorial? Um desabafo?
3. **Formato** — vídeos longos tendem a ser gameplay ou guia; shorts tendem a entretenimento/meme
4. **Presença de conflito interpessoal** — vídeos que narram ou respondem a tretas, haters ou polêmicas
5. **Relação com gênero** — vídeos que explicitamente envolvem mulheres no enredo (e-girl, relacionamento)

### As 5 categorias

| Categoria | Nº vídeos | O que é | Por que existe |
|-----------|-----------|---------|----------------|
| `gameplay` | 14 | Partidas gravadas, clipes de jogadas, momentos de jogo | Categoria central do canal: o Yiok é player de Kassadin e a maior parte do conteúdo é ele jogando. Inclui vídeos onde ele encontra haters na partida, pois o foco principal ainda é o gameplay |
| `entretenimento_meme` | 20 | Shorts humorísticos, memes, sketches, piadas | Maior categoria em quantidade. São clipes curtos (9-51s) com momentos engraçados, trocadilhos ou referências internas da comunidade. Quase todos os shorts se enquadram aqui |
| `guia_tutorial` | 5 | Conteúdo educativo: runas, builds, dicas, coach | Vídeos onde o objetivo é ensinar — seja um guia completo do campeão, análise de runas, discussão de items, ou coaching ao vivo para um viewer. Fundidos em uma categoria porque ambos são conteúdo didático |
| `treta_drama` | 3 | Conflito, polêmica, rivalidade entre players | Vídeos onde o foco não é o jogo em si, mas uma narrativa de conflito — ser atacado, ser ameaçado, ser odiado. Importante porque pode gerar mais comentários agressivos |
| `relacionamento_egirl` | 1 | Conteúdo que envolve gênero/mulher no enredo | Vídeo onde o Yiok encontra uma e-girl no jogo e reage. Categoria mantida separada porque é o tipo de conteúdo mais diretamente ligado a disparar comentários misóginos — a presença de uma mulher no centro do vídeo |

### Lista completa por categoria

<details>
<summary><strong>🎮 gameplay (14 vídeos)</strong></summary>

| videoId | Título | Tipo |
|---------|--------|------|
| `hlf8CuBXMws` | RANK 1 KASSADIN VISITANDO O MESTRE! | longo |
| `ct2DIjWG4uM` | OFICIALMENTE DE VOLTA AO CHALLENGER! | longo |
| `PGFU_utw5qg` | E ASSIM QUE O TOP 1 KASSADIN DO BRASIL JOGA! | short |
| `_8W2fSnL1vY` | LATE GAME KASSADIN ☠️ | longo |
| `nmPCfoxku2k` | ABSOLUT CONHECEU O MELHOR KASSADIN DO MUNDO! | longo |
| `6l1hMZZ_3ms` | APAVORANDO PRO - PLAYER DA LOUD NO CHALLENGER! | longo |
| `9sFGyNdtN8Y` | TOP 1 KASSADIN CARREGANDO O @ayellol1 NO CHALLENGER! | longo |
| `zeYD8_RXrrA` | PIJACK PENSO QUE EU IA TROLAR A PARTIDA MAS ISSO ACONTECEU... | longo |
| `8q5VFwutoGE` | COMO JOGAR CONTRA O MAIOR COUNTER DO KASSADIN! | longo |
| `7iO7Ygle6sE` | KASSADIN DEPOIS DOS BUFFS ESTA IMPARÁVEL...! | longo |
| `12oibiOBoSI` | TOP 1 KASSADIN TESTA OS NOVOS BUFFS... * FICOU MUITO FORTE * | longo |
| `DierqZNnOHA` | FOI OU NÃO FOI? 🫢 | longo |
| `VvTJJ6u9n8Y` | YIOK CAIU COM 4 HATERS NO CHALLENGER TROLLANDO A PARTIDA! | longo |
| `E3ToJX4yMXM` | JUKES SURTOU AO CONHECER O PICK SECRETO DO YIOK! | longo |

</details>

<details>
<summary><strong>😂 entretenimento_meme (20 vídeos)</strong></summary>

| videoId | Título | Tipo |
|---------|--------|------|
| `slhtOG9uSmQ` | KASSADOLA DO ESTUDO! | short |
| `cyk1wQGe3tE` | KASSADOLF NA FUGA DO LAZARO 😂 | short |
| `w4wrS-f4oFo` | O COISA RUIM DE KASSADIN... | short |
| `IeNxaErKY7g` | TIPO O KAYNE WEST 😂 | short |
| `bxVRyxvjqmc` | OLHA O NICK DO CARA... 💀 | short |
| `eaMHWygC3PM` | BOATE KASSADIN 🤣 | short |
| `7STM0pLxRgo` | PASSAR EM MEDICINA OU SER MOD DA LIVE 😂 | short |
| `jV1M7FOgJoU` | SALVE GUIVEN VIM PELO YIOK... | short |
| `NlMxSXvoztk` | O CARA GASTOU 50K PRA FICAR PRESO NO MESTRE... | short |
| `TRNthMDhtSU` | SAPO IMUNDO 😂 | short |
| `Jyknzm3ZojA` | ESSE SYLAS É CEGO 😂 | short |
| `3-jtcrUTDTw` | KARMA INSTANTÂNEO... | short |
| `SeRNWYWd7V4` | TRESH DONO DO ENGENHO 💀 | short |
| `AysubRW-kvQ` | TIO DO ALANZOKA NO LOL... | short |
| `RtNMWGV4wf8` | TRESH FULL AP TA BUGADO 💀 | short |
| `F7XtKG59y4Q` | KASSADIN NA FUGA DO LAZARO 😂 | short |
| `MhR6WbG2UD0` | JOGAR DE ADC É ISSO AE 🫢 | short |
| `jjA-vG38qWU` | IMPOSSIVEL ACERTAR SKILL NO YIOK 😂 | short |
| `S8zUa3KSBj8` | TINHA COMO SER PIOR? 🫢 | short |
| `6hO01e5kvvQ` | PLAYZUDA NO LIMITE! 😎 | short |

</details>

<details>
<summary><strong>📚 guia_tutorial (5 vídeos)</strong></summary>

| videoId | Título | Tipo |
|---------|--------|------|
| `0sD6xl3EFbo` | TUDO O QUE VOCÊ PRECISA SABER - GUIA DEFINITIVO CHALLENGER KASSADIN | longo |
| `92KeIj8hsOE` | APÓS 1 ANO, FINALMENTE ENCONTREI A MELHOR RUNA DO KASSADIN! | longo |
| `PIyw-_gHTzU` | PAREM DE COMPRAR ESSE ITEM NO KASSADIN! | longo |
| `DjhpGJAZBi8` | A RIOT ADICIONOU UM BUFF EXTRA OCULTO NO KASSADIN! | longo |
| `r8C57BD7aDc` | YIOK SURTA AO VIVO DANDO COACH PARA UM VIEWER BRONZE IV! | longo |

</details>

<details>
<summary><strong>🔥 treta_drama (3 vídeos)</strong></summary>

| videoId | Título | Tipo |
|---------|--------|------|
| `Cyai8_m_ZQ8` | YIOK FOI ATACADO PELOS GADOS DA COMUNIVIA... TRETA PESADA! | longo |
| `xJExphI2SRU` | YIOK FOI AMEAÇADO AO VIVO PELO MUCALOL! | longo |
| `ifSpvNYqE2g` | COMO O YIOK SE TORNOU O PLAYER MAIS ODIADO DO SERVIDOR! | longo |

</details>

<details>
<summary><strong>💖 relacionamento_egirl (1 vídeo)</strong></summary>

| videoId | Título | Tipo |
|---------|--------|------|
| `SBT6DCNR4BY` | YIOK CAIU CONTRA UMA E-GIRL NO CHALLENGER E FICOU APAIXONADO! | longo |

</details>

A coluna `categoria_video` foi adicionada ao arquivo `data/data_base yiok - videos.csv`.


## 📊 As duas fontes do corpus

Este corpus contém **duas fontes textuais distintas**, ambas passíveis de análise pelo léxico MOL:

| | Fonte 1 — Comentários | Fonte 2 — Transcrições |
|---|---|---|
| **O que é** | O que a audiência escreve | O que o Yiok diz nos vídeos |
| **Arquivos** | `data/comentarios/` | `data/videos/<videoId>/<videoId>_transcricao.txt` |
| **Volume** | 1.222 comentários | 43 transcrições (81.553 palavras) |
| **Métrica MOL** | Flag binário (1/0) por comentário | Frequência de termos por mil palavras |
| **Natureza** | Reação da audiência | Discurso do criador de conteúdo |

> 🔑 As transcrições são uma **segunda fonte analítica**, não um complemento dos comentários. Permitem comparar a linguagem do streamer com a linguagem da audiência — uma camada analítica que a maioria dos estudos de comentários de YouTube não tem.


## 🔍 Opções de análise comparativa dentro da base

A base atual permite **comparações internas** (não apenas descrições de dados). As opções viáveis são:

### Opção 1 — Categoria do vídeo × misoginia nos comentários

Comparar a proporção de comentários misóginos entre as **5 categorias de vídeo** (gameplay, entretenimento_meme, guia_tutorial, treta_drama, relacionamento_egirl).

- **Variável independente:** categoria do vídeo (5 categorias)
- **Variável dependente:** presença de misoginia (flag MOL)
- **Teste:** qui-quadrado + odds ratio

### Opção 2 — Discurso do vídeo × discurso dos comentários

Aplicar o léxico MOL às **43 transcrições** (além dos comentários) e comparar a misoginia na fala do Yiok com a misoginia nos comentários de cada vídeo.

- **Métrica das transcrições:** frequência de termos por mil palavras (mesma métrica usada por Martínez Arranz et al., 2024)
- **Métrica dos comentários:** % de comentários flagged
- **Pergunta:** vídeos em que o criador usa mais linguagem misógina geram comentários mais misóginos?

### Opção 3 — Engajamento × misoginia

Avaliar se comentários misóginos recebem mais ou menos likes que comentários não-misóginos.

- **Variável independente:** flag MOL (sim/não)
- **Variável dependente:** likeCount
- **Teste:** comparação de médias (t-test ou Mann-Whitney)

### Opção 4 — Categorias de misoginia × categoria do vídeo

Analisar se certas **categorias do léxico MOL** (body shaming, racial interseccional, gamer misógino, etc.) são mais frequentes em certos tipos de vídeo do que em outros.

- **Variável independente:** categoria do vídeo (5 categorias)
- **Variável dependente:** distribuição das 8 categorias MOL
- **Teste:** qui-quadrado por categoria ou análise de correspondência

> ⚠️ Estas opções serão executadas **após o refinamento do léxico MOL**, que é a prioridade atual. As opções estão registradas aqui para planejamento — a análise estatística formal ainda não foi realizada.


## 📚 Créditos e referências

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
- **RADFORD, Alec; KIM, Jong Wook; XU, Tao; BROCKMAN, Greg; MCLEAVEY, Christine; SUTSKEVER, Ilya.** Robust Speech Recognition via Large-Scale Weak Supervision. *Proceedings of the 40th International Conference on Machine Learning*, v. 202, p. 28492–28418, 2023.
- **MARTÍNEZ ARRANZ, A.; ZECH, S. T.; BONOTTI, M.** Political Parties and Civility in Parliament: The Case of Australia from 1901 to 2020. *Parliamentary Affairs*, v. 77, n. 2, p. 371–399, 2024. DOI: [10.1093/pa/gsad008](https://doi.org/10.1093/pa/gsad008). Open Access.
- **FERNANDEZ, Michelle; BERTHOLINI, Frederico; MAIA, Bárbara.** Políticas de saúde dos Estados brasileiros durante a pandemia de Covid-19: um dataset das normativas produzidas. *Dados*, Rio de Janeiro, v. 68, n. 3, e20230153, 2025.
- **LOURENÇO, Luiz Claudio; VITENA, Gabrielle Simões Lima; SILVA, Marina de Macedo.** Prisão provisória, racismo e seletividade penal: uma discussão a partir dos prontuários de uma unidade prisional. *Revista Brasileira de Segurança Pública*, v. 16, n. 2, p. 220–239, 2022.

### Referência metodológica citável — Martínez Arranz et al. (2024)

> MARTÍNEZ ARRANZ, A.; ZECH, S. T.; BONOTTI, M. **Political Parties and Civility in Parliament: The Case of Australia from 1901 to 2020.** *Parliamentary Affairs*, v. 77, n. 2, p. 371–399, 2024. DOI: [10.1093/pa/gsad008](https://doi.org/10.1093/pa/gsad008). Open Access.

**Por que este artigo é relevante:**

O artigo usa uma **abordagem lexicon-based** para detectar incivilidade no Parlamento australiano (corpus Hansard, >1,2 milhão de documentos) — a mesma família metodológica do MOL deste projeto. A métrica central é **frequência de termos por mil palavras**, que pode ser aplicada diretamente às transcrições deste corpus.

**Equivalência metodológica:**

| Artigo (Martínez Arranz et al.) | Este projeto |
|---|---|
| Corpus: discursos Hansard | Corpus: comentários + transcrições de vídeos de LoL |
| Léxico: 1.383 termos de incivilidade (inglês) | Léxico MOL: 92 termos de misoginia (português) |
| Métrica: frequência/mil palavras | Métrica: flag binário (comentários) + freq/mil palavras (transcrições) |
| Comparação: entre partidos, câmaras, décadas | Comparação: entre categorias de vídeo, fala vs comentários |
| Variável dependente: incivilidade | Variável dependente: misoginia |

**Como citar no artigo futuro:**

- Na **seção de metodologia**: "Seguindo a abordagem lexicon-based de Martínez Arranz, Zech e Bonotti (2024) para detecção de incivilidade parlamentar — que utiliza um dicionário de termos e mede frequência por mil palavras —, este estudo aplica um léxico de misoginia em português brasileiro..."
- Na **seção de discussão**: "Enquanto Martínez Arranz et al. (2024) comparam incivilidade entre partidos políticos, este estudo compara misoginia entre tipos de conteúdo em vídeos de gaming..."

### Criador do conteúdo

- **Yiok** — YouTuber de League of Legends, criador dos vídeos que compõem este corpus

## 📄 Licença

Este repositório contém dados de pesquisa acadêmica. Os vídeos e áudios pertencem ao canal Yiok. As transcrições e análises são de uso acadêmico.


## 📌 Status

**Versão preliminar** — entrega inicial para as disciplinas de Métodos Digitais e Laboratório Quantitativo em Ciências Sociais. O léxico MOL está em refinamento e os números podem mudar.

- ✅ 43 vídeos coletados (22 longos + 21 shorts)
- ✅ 43 vídeos categorizados em 5 categorias (`categoria_video` no CSV)
- ✅ 1.222 comentários brutos
- ✅ Léxico MOL v2 (92 termos / 8 categorias) — em refinamento
- ✅ Base analítica com codificação binária por categoria
- ✅ 43 transcrições (Whisper large-v3) — segunda fonte analítica
- ✅ Referência metodológica citável registrada (Martínez Arranz et al., 2024)
- ✅ Script de análise léxica (`scripts/analise_lexical.py`) — roda léxico em comentários + transcrições

### 🔜 Próximos passos previstos

- [ ] **Refinar o léxico MOL** com termos específicos da comunidade de League of Legends — prioridade atual
- [ ] Aplicar o léxico MOL melhorado aos comentários e transcrições
- [ ] Rodar análise estatística formal (qui-quadrado, odds ratio, correlação) após refinamento do léxico
- [ ] Comparar misoginia entre as 5 categorias de vídeo
- [ ] Comparar misoginia na fala do criador vs comentários da audiência
- [ ] Evoluir da codificação binária para análise multilabel mais granular
- [ ] Baixar e armazenar o PDF do artigo de Martínez Arranz et al. (2024) como referência metodológica