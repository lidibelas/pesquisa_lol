# Decisões metodológicas | Pesquisa LoL — Corpus Yiok

Este documento reúne decisões para o artigo de Laboratório Quantitativo e para a apresentação em Métodos Digitais. A fonte do desenho e da coleta é o [README do projeto](../README.md). **Estado:** corpus e léxicos disponíveis; nova análise, tabela final, gráfico e correlações ainda não executados. Não reutilizar números do recorte anterior como resultados deste.

## 1. Pergunta e desenho

**Pergunta:** no canal do Yiok, vídeos com mais ocorrências de termos do MOL por mil palavras transcritas têm mais visualizações?

- **Unidade de análise:** vídeo, identificado por `videoId`. A mesma unidade liga os arquivos de transcrição à tabela de metadados.
- **Delimitação:** 43 vídeos de um único canal de League of Legends no YouTube, publicados entre 21/08/2025 e 21/11/2025 (22 vídeos longos e 21 Shorts). A seleção foi temporal, não baseada na presença prévia de termos.
- **Desenho:** estudo de caso descritivo e exploratório. A hipótese de associação positiva é uma hipótese de trabalho, não um resultado. A análise não estabelece causalidade, não mede a prevalência em LoL inteiro e não identifica o que o algoritmo recomendou.
- **Escopo atual:** falas transcritas × visualizações. Comentários do público e tabelas da análise anterior ficam arquivados e não entram no cálculo atual.

## 2. Fontes, coleta e tratamento

| Fonte | Decisão |
|---|---|
| [Metadados](../data/data_base%20yiok%20-%20videos.csv) | O README registra YouTube Data Tools v2, módulos Channel Info e Video List. Usar `viewCount` como valor do arquivo da coleta, não como contador atual. A data exata dessa medição deve ser indicada se houver registro verificável; não confundir com a janela de publicação. |
| Áudio | O README registra a extração com Parabolic/yt-dlp. Usar as transcrições já existentes, sem baixar ou transcrever de novo nesta etapa. |
| Transcrição | O README registra faster-whisper, Whisper large-v3, idioma `pt`, CUDA/float16, beam 5, VAD ligado e condicionamento no texto anterior desligado. Usar apenas a coluna `texto` do CSV segmentado, sem timestamps no total de palavras. Não presumir que toda fala seja do criador. |
| Descrição escrita | A base traz 14 vazias e 29 preenchidas, em sua maioria texto padrão. Se houver contagem, registrar em colunas próprias e fora do denominador das falas. Descrição vazia não é texto analisado com zero achados. |
| Formato e conteúdo | Manter Short/longo e as cinco categorias descritivas do README: gameplay, entretenimento/meme, guia/tutorial, treta/drama e relacionamento/e-girl. Formato e categoria de conteúdo não são a mesma variável. |

## 3. Construção do MOL e decisões de inclusão

O MOL combina fontes lexicais em português, literatura e termos observados na comunidade e nas transcrições. A adaptação ao próprio corpus é exploratória. **As categorias classificam entradas do léxico, não a intenção nem a natureza de cada trecho.**

- **Excluir da contagem:** `caralho`, `pica`, `foder`, `puto` e `putinho`. São usos genéricos ou ambíguos; o próprio corpus traz, por exemplo, `caralho` como interjeição. A exclusão não permite afirmar que todos os falsos positivos foram eliminados.
- **Preservar `puta` e `putinha`** como entradas distintas. Desconsiderar a ocorrência de `puta` nas expressões “puta que pariu”, “filho da puta” e “filha da puta”. A exceção afeta só aquela ocorrência, não outras no mesmo trecho nem o denominador.
- **Indicador principal:** insulto de gênero/desqualificação sexual; policiamento da masculinidade (por exemplo, `gado` e `escravoceta`); deslegitimação da habilidade/elo (`boostada` e a forma `bustada` observada na transcrição); sexualização (`gostosona`); e desqualificação pela aparência (`gorda`, `feia`, também em contagem própria). Esses termos admitem usos não ofensivos. A cena da acusação de elo ilustra como a competência é enquadrada, não prova conduta ou mérito da jogadora.
- **Flags auxiliares:** marcadores raciais (por exemplo, `macaco` e `neguinho`), de homofobia/transfobia, e menções a violência sexual (`estupro`, `estuprar` e variantes registradas). Não entram na taxa principal. Uma menção não distingue denúncia, citação, metáfora de gameplay ou endosso.
- **Fora da contagem automática:** entradas `contextual` e `excluido`. Exemplos de indicadores contextuais: `e-girl` isolado, referências anatômicas isoladas e `mulher mestre`. A forma `estuprindo` foi mantida como contextual por incerteza de transcrição.

## 4. Duas versões, uma única diferença

| Versão | Uso | Entradas de status principal |
|---|---|---:|
| [Sem frases de cena](../lexico/mol-sem-frases-de-cena.csv) | Especificação de referência | 34 |
| [Com frases de cena](../lexico/mol-com-frases-de-cena.csv) | Comparação de sensibilidade; reproduz o MOL v3 revisado | 40 |

O arquivo **com** conserva 97 entradas. O **sem** tem 90: as sete linhas abaixo foram retiradas fisicamente do CSV, em vez de apenas mudar seu status.

- `foi boostada pelo namorado` e `foi bustada pelo namorado`;
- `mulher falando de lol`;
- `mulher não sabe jogar` e `mulher nao sabe jogar`;
- `mulher não entende de lol` e `mulher nao entende de lol`.

No arquivo **com**, seis dessas linhas têm status `principal`; `mulher falando de lol` continua `contextual` e não entra automaticamente na taxa. As outras 90 linhas são idênticas entre as versões, incluindo `boostada`, `bustada` e gírias de várias palavras, como `web puta`. As exceções por frase são regras para não contar uma ocorrência, não entradas do léxico. Quando a versão **com** reconhece uma expressão longa que contém um termo curto elegível, não duplica a ocorrência. Assim, remover uma expressão longa pode não mudar o total se o termo curto ainda contar. A comparação testa o efeito das formulações selecionadas, não de todas as expressões com várias palavras.

As duas versões usam as **mesmas exceções de frase** e as mesmas categorias auxiliares. A seleção foi feita antes de executar a comparação com views. Não trocar de especificação em função de qual resultado ficou mais forte.

## 5. Contagem e CSV a produzir

- Buscar palavras inteiras e expressões literais, com variantes explicitadas e sem diferenciar maiúsculas de minúsculas. Não interpretar automaticamente contexto, alvo ou intenção. Em sobreposição, contar a expressão elegível mais longa uma vez; entradas fora da contagem não bloqueiam termos elegíveis.
- **Ocorrência:** cada correspondência elegível, incluindo repetições. **Flag:** um segmento com ao menos uma correspondência no grupo em questão, ainda que contenha mais de uma.
- **Taxa:** ocorrências principais / total de palavras da transcrição × 1.000. Ausente/vazia → sem taxa; transcrição analisável sem ocorrência → zero. Reportar total bruto junto à taxa, especialmente em textos curtos.
- **Tabela nova:** uma linha por `videoId`, com views do arquivo, formato, categoria, total de palavras, ocorrências principais, flags e taxa por mil palavras para cada versão, e flags auxiliares por categoria. Se processar descrição, usar colunas distintas. Conferir 43 IDs únicos e cobertura das transcrições antes de interpretar.
- Não sobrescrever dados brutos ou tabelas antigas. `scripts/analise_lexical.py` não implementa o protocolo acima. A coluna histórica `freq_mol_por_mil` conta segmentos sinalizados por mil segmentos e não é a nova taxa por palavras.

## 6. Comparação e o que reportar

Fazer gráfico de dispersão de taxa × views, distinguindo Shorts de vídeos longos. Usar a mesma base e os mesmos filtros para as duas versões. Calcular Spearman para a relação entre a ordem das taxas e a ordem das views, reportando o número de vídeos analisados e, se houver dados suficientes, resultados por formato. Não usar diferença de significância estatística como única medida de mudança.

Registrar as duas estimativas e quantos vídeos mudaram de taxa. **No artigo e nos slides, destacar a comparação se ela mudar a leitura do resultado**, por exemplo, se uma tendência desaparecer, inverter de modo relevante ou se concentrar em um vídeo. Se quase nada mudar, basta uma nota curta ou tabela complementar. Não dizer que houve diferença sem executar as duas versões.

## 7. Limitações e transparência

- Transcrição automática pode trocar grafias, omitir termos e não identificar locutor; confirmar o áudio antes de citar exemplos centrais como fala exata. A variante `bustada` veio da transcrição.
- A contagem não detecta ironia, recorrência fora do dicionário ou se a pessoa está citando/contestando o enunciado. Falsos positivos e negativos são possíveis; não alegar validação externa ou revisão integral se não forem feitas.
- Shorts e vídeos longos podem ter exposição, duração e padrões de circulação diferentes. Não confundir associação, confirmação de misoginia e causalidade.
- Registrar a versão do léxico e do script e o recorte do arquivo de metadados usado. Se houver uso de IA, explicitar e justificar os usos reais em anexo, conforme o programa da disciplina, e conferir também as normas da revista.

Ver [Referências bibliográficas](referencias-bibliograficas.md).
