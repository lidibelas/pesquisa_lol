# Pesquisa LoL — Corpus Yiok

Estudo de caso sobre linguagem, misoginia e visibilidade em vídeos de League of Legends no YouTube. Projeto independente de **Lídia Belas** (Antropologia/UFBA), vinculado às disciplinas de **Métodos Digitais** e **Laboratório Quantitativo em Ciências Sociais**. A documentação registra as decisões metodológicas e permite reproduzir a análise.

## Pergunta de pesquisa

**No canal do Yiok, vídeos com mais ocorrências de termos do léxico MOL por mil palavras transcritas têm mais visualizações?**

A unidade de análise é o vídeo. O recorte atual cruza **transcrições e visualizações por vídeo**. Os comentários e os resultados da comparação anterior entre transcrições e comentários continuam no repositório, mas não entram nesta análise. O estudo é descritivo e exploratório: trata de um canal e não estima a prevalência de misoginia em League of Legends.

## Corpus

- **Canal:** Yiok (League of Legends).
- **Janela de publicação:** 21/08/2025 a 21/11/2025, sem seleção prévia pela presença de termos.
- **Vídeos:** 43, sendo 22 longos e 21 Shorts, com transcrições automáticas e metadados.
- **Visualizações:** coluna `viewCount` da base de metadados. São os valores registrados na coleta, não o contador atual do YouTube.
- **Descrições escritas:** 14 vazias e 29 preenchidas, em sua maioria com texto padrão. Se analisadas, suas contagens ficam em colunas próprias, fora da taxa calculada sobre a transcrição do áudio.

## 📁 Estrutura do repositório

```
pesquisa_lol/
├── AGENTS.md                              ← guia para agentes de IA (leia antes de operar o repo)
├── README.md                              ← este arquivo
├── .gitignore
├── lexico/                                ← léxico MOL (ferramenta de análise, NÃO é dado bruto)
│   ├── mol-sem-frases-de-cena.csv          ← versão principal da análise
│   ├── mol-com-frases-de-cena.csv          ← comparação de sensibilidade
│   └── descartados/                       ← versões anteriores, para consulta histórica
├── scripts/                               ← scripts de análise
│   └── analise_lexical.py                    ← análise legada de comentários e segmentos de transcrição
└── data/                                  ← dados da pesquisa (brutos e analíticos)
    ├── data_base yiok - videos.csv        ← base de vídeos (43 linhas, 30+ variáveis do YTDT + categoria_video)
    ├── data_base yiok.csv                 ← cópia da base de vídeos (upload via navegador)
    ├── comentarios/                       ← comentários coletados e base analítica
    │   ├── data_base yiok - comentários.csv   ← base completa de comentários brutos (1.222)
    │   ├── base_analitica_mol.csv             ← base analítica unificada (1.222 + codificação binária MOL)
    │   └── comentarios_flagged_mol.csv        ← comentários sinalizados na análise anterior
    ├── analise/                           ← resultados da análise anterior
    │   ├── base_comparativa_por_video.csv     ← comparação anterior por vídeo (segmentos e comentários)
    │   ├── base_analitica_comentarios_mol.csv ← 1.222 comentários codificados pelo MOL
    │   ├── base_analitica_transcricoes_mol.csv← 8.384 segmentos codificados pelo MOL
    │   ├── crosstab_comentarios_video_categorias.csv  ← vídeo × categorias MOL (comentários)
    │   ├── crosstab_transcricoes_video_categorias.csv ← vídeo × categorias MOL (transcrições)
    │   ├── resumo_estatistico_mol.csv         ← métricas gerais
    │   ├── comentarios_flagged_mol.csv        ← comentários flagged pelo MOL
    │   └── transcricoes_flagged_mol.csv       ← segmentos flagged pelo MOL
    └── videos/                            ← uma pasta por vídeo (43 total)
        └── <videoId>/
            ├── descricao.md                   ← metadados + descrição original
            ├── <videoId>.mp3                  ← áudio do vídeo (35 de 43 no repo; 8 >25 MB mantidos localmente)
            ├── <videoId>_transcricao.txt      ← transcrição em texto com possíveis marcações de tempo
            ├── <videoId>_transcricao.csv      ← transcrição segmentada com coluna texto
            └── <videoId>_metadados_transcricao.txt ← parâmetros da transcrição
```

> 🔑 **Sobre a separação léxico ↔ dados:** o `lexico/` fica **na raiz**, fora de `data/`. O léxico é uma **ferramenta de análise** (lista de termos e categorias usada para sinalizar ocorrências de termos), não um dado bruto coletado do YouTube. Os dados brutos e analíticos ficam em `data/`.

## Metodologia

### 1. Coleta e delimitação do corpus — YouTube Data Tools v2

A construção inicial do corpus foi realizada por meio do **YouTube Data Tools (YTDT)**, desenvolvido por **Bernhard Rieder** no âmbito da Digital Methods Initiative. A ferramenta utiliza a API v3 do YouTube e foi projetada especificamente para coleta de dados de pesquisa.

Inicialmente, utilizou-se o módulo **Channel Info** para identificação do canal do Yiok. Posteriormente, utilizou-se o módulo **Video List**, que gera uma tabela em que cada linha corresponde a um vídeo e contém metadados e métricas: identificador único do vídeo (`videoId`), título, data de publicação, duração, número de visualizações, likes e comentários.

A delimitação do corpus foi realizada a partir de um critério **exclusivamente temporal**, considerando os vídeos publicados entre **21 de agosto e 21 de novembro de 2025**. A definição prévia dessa janela busca preservar o caráter exploratório da pesquisa e evitar a seleção de conteúdos a partir da identificação antecipada de falas ou temáticas relacionadas à violência de gênero.

> 🔑 **Decisão metodológica**: os vídeos não foram selecionados porque pareciam conter misoginia. O critério foi exclusivamente temporal, definido antes da análise dos conteúdos.

### 2. Preparação dos vídeos para transcrição — Parabolic

Para manter um procedimento uniforme no corpus, foram produzidas transcrições próprias a partir das faixas de áudio.

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

- **`.txt`** — transcrição em texto, que pode incluir marcações de tempo
- **`.csv`** — segmentos com marcações de tempo e coluna `texto`
- **`_metadados_transcricao.txt`** — parâmetros e estatísticas da transcrição

### 4. Aplicação do léxico MOL

MOL (Misoginia Online em Léxico) foi construído a partir de fontes lexicais em português, literatura e vocabulário observado na comunidade de League of Legends e no corpus. Use o **[MOL sem frases específicas de cena](lexico/mol-sem-frases-de-cena.csv)** como indicador de referência e o **[MOL com frases específicas de cena](lexico/mol-com-frases-de-cena.csv)** para a comparação. Os dois derivam do v3 revisado e registram 97 entradas, incluindo formas fora da contagem. O v2 e os arquivos de origem do v3 estão em [descartados](lexico/descartados/), apenas para consulta e reprodução histórica. Veja as [decisões metodológicas](artigo/decisoes-metodologicas.md) para a diferença exata entre as versões. As entradas têm os seguintes status:

| Status | Uso |
|---|---|
| `principal` | Ocorrências que entram no indicador principal, com contagens por categoria: insulto de gênero, policiamento da masculinidade, deslegitimação da habilidade ou do elo, sexualização e desqualificação pela aparência. |
| `auxiliar` | Flags separadas para marcadores raciais, marcadores de homofobia ou transfobia e menções a violência sexual. Não entram na taxa principal. |
| `contextual` | Elementos preservados para interpretação, sem contagem automática. |
| `excluido` | Elementos documentados, mas fora das contagens. |

A análise proposta conta correspondências literais no campo `texto` dos CSVs de transcrição, sem distinguir maiúsculas de minúsculas e sem incluir horários ou outros metadados. As exceções de frase, como “puta que pariu”, “filho da puta” e “filha da puta”, afetam apenas a ocorrência correspondente de `puta`, não o número de palavras do trecho. Em sobreposições, conta-se a expressão mais longa uma vez, sem duplicar a palavra que faz parte dela. Uma **ocorrência** é cada correspondência aceita; uma **flag** indica que um segmento tem ao menos uma correspondência na categoria em questão. Várias ocorrências no mesmo segmento não equivalem a várias flags desse segmento.

A adaptação do léxico ao próprio corpus é exploratória, não uma validação externa do instrumento. As duas versões mantêm as mesmas exceções. A diferença é se as duas formulações específicas da cena do namorado entram como expressões principais; as formas curtas continuam elegíveis em ambas. Registre a versão e o critério antes de calcular a associação; não escolha a especificação pelo resultado mais alto. Correspondências são marcadores lexicais, não confirmação de misoginia, intenção, alvo ou autoria da fala.

### 5. Comparação por vídeo

A base da nova análise deve ter uma linha por `videoId`. O mesmo identificador vincula a transcrição aos metadados. A taxa principal é:

**Ocorrências principais por mil palavras = (ocorrências principais ÷ total de palavras transcritas) × 1.000.**

| Campo | Uso |
|---|---|
| `videoId` | Identificador único do vídeo |
| Total de palavras transcritas | Denominador da taxa |
| Ocorrências principais | Contagem bruta de correspondências de status `principal`, por vídeo |
| Segmentos sinalizados (flags) | Número de segmentos com pelo menos uma ocorrência principal, sem confundir com o total de ocorrências |
| Ocorrências principais por mil palavras | Medida padronizada para comparar transcrições de tamanhos diferentes |
| Flags auxiliares por categoria | Registradas separadamente, sem compor a taxa principal |
| `viewCount` | Visualizações registradas na base |
| Formato e `categoria_video` | Identificar Shorts, vídeos longos e categorias de conteúdo |

Uma transcrição válida sem ocorrência tem taxa zero; transcrição ausente ou vazia não tem taxa calculável. Na leitura dos resultados, mantenha as contagens brutas junto às taxas: uma ocorrência pode pesar muito num Short com poucas palavras. O gráfico principal compara taxa e visualizações, distinguindo os formatos. Diferenças no tempo de exposição e na circulação dos vídeos limitam a interpretação. Uma associação, se observada, não demonstra causalidade.

## 🎬 Categorização dos vídeos

Os 43 vídeos do corpus foram classificados em **5 categorias de conteúdo** com base na análise dos títulos, descrições e transcrições. As categorias descrevem o corpus e podem ajudar a interpretar diferenças entre vídeos na análise exploratória.

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
| `treta_drama` | 3 | Conflito, polêmica, rivalidade entre players | Vídeos onde o foco não é o jogo em si, mas uma narrativa de conflito — ser atacado, ser ameaçado, ser odiado. Categoria descritiva para vídeos centrados em conflito |
| `relacionamento_egirl` | 1 | Conteúdo que envolve gênero/mulher no enredo | Vídeo onde o Yiok encontra uma e-girl no jogo e reage. Categoria mantida separada porque gênero e relacionamento aparecem no próprio enredo |

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

## Arquivos da análise anterior

O script `scripts/analise_lexical.py` e as tabelas existentes em `data/analise/` documentam o recorte anterior. **O script legado não implementa os status e as exceções do v3.** Passar um dos CSVs ativos para ele não reproduz o desenho descrito aqui. O caminho padrão dele aponta para o v2 antes do arquivamento; para reprodução histórica, use uma cópia isolada e indique `--lexico lexico/descartados/mol-lexicon.csv` para não sobrescrever resultados do projeto. Na tabela `data/analise/base_comparativa_por_video.csv`, `freq_mol_por_mil` significa **segmentos sinalizados por mil segmentos transcritos**, e não ocorrências por mil palavras. O percentual de comentários sinalizados também pertence ao recorte anterior. Nenhuma dessas colunas deve ser usada como resultado da nova comparação com visualizações.

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
- **RADFORD, Alec; KIM, Jong Wook; XU, Tao; BROCKMAN, Greg; MCLEAVEY, Christine; SUTSKEVER, Ilya.** Robust Speech Recognition via Large-Scale Weak Supervision. *Proceedings of the 40th International Conference on Machine Learning*, v. 202, p. 28492–28518, 2023.
- **MARTÍNEZ ARRANZ, A.; ZECH, S. T.; BONOTTI, M.** Political Parties and Civility in Parliament: The Case of Australia from 1901 to 2020. *Parliamentary Affairs*, v. 77, n. 2, p. 371–399, 2024. DOI: [10.1093/pa/gsad008](https://doi.org/10.1093/pa/gsad008). Open Access.
- **FERNANDEZ, Michelle; BERTHOLINI, Frederico; MAIA, Bárbara.** Políticas de saúde dos Estados brasileiros durante a pandemia de Covid-19: um dataset das normativas produzidas. *Dados*, Rio de Janeiro, v. 68, n. 3, e20230153, 2025.
- **LOURENÇO, Luiz Claudio; VITENA, Gabrielle Simões Lima; SILVA, Marina de Macedo.** Prisão provisória, racismo e seletividade penal: uma discussão a partir dos prontuários de uma unidade prisional. *Revista Brasileira de Segurança Pública*, v. 16, n. 2, p. 220–239, 2022.

Martínez Arranz, Zech e Bonotti (2024) são uma referência para o uso de dicionário e normalização por mil palavras. O estudo deles trata de incivilidade parlamentar; não valida automaticamente o léxico MOL ou sua interpretação no contexto de LoL.

### Criador do conteúdo

- **Yiok** — YouTuber de League of Legends, criador dos vídeos que compõem este corpus

## 📄 Licença

Este repositório contém dados de pesquisa acadêmica. Os vídeos e áudios pertencem ao canal Yiok. As transcrições e análises são de uso acadêmico.

## Próximos passos

- [x] Publicar os dois léxicos ativos e arquivar suas versões anteriores.
- [ ] Implementar e testar um script para o v3, incluindo flags separadas e exceções de frase.
- [ ] Gerar uma nova tabela por vídeo sem sobrescrever dados brutos ou análises antigas.
- [ ] Conferir a junção por `videoId`, os denominadores e a cobertura das transcrições.
- [ ] Comparar as taxas e as visualizações, distinguindo Shorts e vídeos longos.
- [ ] Usar apenas resultados verificados no relatório e na apresentação de Métodos Digitais.
