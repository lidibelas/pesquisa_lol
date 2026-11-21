# AGENTS.md — Guia para Agentes AI

> Este arquivo orienta qualquer agente de IA (LLM, bot, assistente) que acesse este repositório. Leia antes de fazer qualquer coisa.

## Autorização obrigatória da Lídia

- **Só acesse ou consulte este repositório quando Lídia pedir.** Um pedido de análise ou revisão autoriza leitura, não alterações.
- **Antes de mudar qualquer coisa, informe o que pretende fazer e espere a autorização explícita da Lídia.** Isso vale para criar, editar, mover ou apagar arquivos, gerar ou substituir resultados no repositório, fazer commits, criar branches, abrir pull requests, dar push ou fazer merge, mesmo para correções pequenas.
- A autorização vale só para a ação, os arquivos e o modo de acesso combinados. Se o escopo mudar, peça autorização de novo. Uma exceção à regra da chave SSH para uma tarefa não vale para a próxima.
- As listas de tarefas e de boas práticas neste arquivo descrevem como trabalhar **depois** da autorização; não são permissões permanentes.

## O que é este repositório

`pesquisa_lol` reúne dados de um projeto independente de **Lídia Belas** (Antropologia/UFBA) vinculado a **Métodos Digitais** e ao **Laboratório Quantitativo em Ciências Sociais**. Não é um projeto do LABHDUFBA ou do PIBIC. A pesquisadora conduz o projeto sem orientador formal.

## Desenho atual

**Pergunta:** no canal do Yiok, vídeos com mais ocorrências de termos do léxico MOL por mil palavras transcritas têm mais visualizações?

- **Unidade de análise:** vídeo (`videoId`). São 43 vídeos publicados de 21/08/2025 a 21/11/2025, sendo 22 longos e 21 Shorts, com transcrições automáticas.
- **Fonte principal:** campo `texto` em `data/videos/<videoId>/<videoId>_transcricao.csv`. Use `viewCount` da base `data/data_base yiok - videos.csv`, como o valor registrado na coleta, não o contador atual. Identifique formato e categoria do vídeo.
- **Descrições escritas:** podem ser medidas separadamente, sem somar suas palavras ou ocorrências às das transcrições. Não trate descrição inexistente como se fosse texto analisado.
- **Comentários:** pertencem ao recorte anterior. Preserve os dados e resultados, mas não os use como insumo para a comparação atual.
- **Interpretação:** estudo de caso exploratório, sem inferência causal. Um marcador lexical não confirma misoginia nem determina a intenção ou identidade do falante.

## Léxico, contagens e resultados

- Os únicos léxicos ativos são [sem frases específicas de cena](lexico/mol-sem-frases-de-cena.csv) (referência) e [com frases específicas de cena](lexico/mol-com-frases-de-cena.csv) (comparação). Os arquivos anteriores estão em [descartados](lexico/descartados/) e não são entradas da análise atual. Consulte as [decisões metodológicas](artigo/decisoes-metodologicas.md). Mantenha `lexico/` separado de `data/` e registre o arquivo usado em toda execução.
- A taxa principal é **ocorrências de status `principal` ÷ palavras transcritas × 1.000**. Uma flag indica um segmento com pelo menos uma correspondência; não equivale à quantidade de termos. Marcadores raciais, de homofobia ou transfobia e menções a violência sexual têm flags auxiliares independentes e ficam fora da taxa principal. Não conte entradas contextuais ou excluídas.
- Aplique as exceções por ocorrência, sem alterar o denominador de palavras; em sobreposições, dê prioridade à expressão mais longa. Se houver comparação com e sem expressões específicas, documente o critério antes de calcular a associação com views e apresente as duas especificações sem escolher pela correlação mais alta.
- Gere uma nova tabela com uma linha por vídeo: ID, total de palavras, ocorrências principais, segmentos sinalizados, taxa por mil palavras, flags auxiliares, views e formato. Registre transcrição ausente ou vazia como sem taxa, não como zero.
- **O script `scripts/analise_lexical.py` é legado.** Não passa a aplicar as regras do v3 apenas trocando o arquivo de léxico. Seu caminho padrão é anterior ao arquivamento: só para reprodução histórica, em cópia isolada, indique `--lexico lexico/descartados/mol-lexicon.csv`. A coluna `freq_mol_por_mil` da tabela antiga mede segmentos sinalizados por mil segmentos, não ocorrências por mil palavras.
- **Nunca sobrescreva os dados brutos ou resultados anteriores.** Uma nova implementação, execução, atualização de arquivos ou publicação deve respeitar o escopo autorizado pela Lídia. Não declare a análise executada até verificar a nova tabela e a cobertura do corpus.

Consulte o [README](README.md) para estrutura de pastas, coleta, transcrição e referências. Martínez Arranz, Zech e Bonotti (2024) são uma referência para normalização por mil palavras, não uma validação do MOL no corpus Yiok.

### O que NÃO fazer

- ❌ **NUNCA usar a conta ou token de terceiros** neste repositório. Use apenas git + deploy key SSH da própria Lídia.
- ❌ **NÃO usar `gh` CLI** neste repositório — apenas `git` + deploy key SSH
- ❌ **NÃO versionar documentos `.docx` de metodologia** (o arquivo enviado pela pesquisadora fica apenas como referência local, não no repo)
- ❌ **NÃO subir áudios `.mp3` maiores que 25 MB** (limite adotado neste projeto)
- ❌ **NÃO modificar ou deletar dados originais** coletados (comentários brutos, transcrições, descrições)
- ❌ **NÃO mover o `lexico/` para dentro de `data/`** — são coisas diferentes
- ❌ **NÃO inventar dados** — se algo não existe no corpus, diga que não existe
- ❌ **NÃO alterar a estrutura de pastas** sem atualizar o README.md e o AGENTS.md
- ❌ **NÃO expor credenciais, tokens, API keys ou deploy keys** em commits, issues ou arquivos do repo

## Como eu quero organizar as coisas

- **`lexico/` na raiz** — separado de `data/` porque é ferramenta, não dado
- **`data/` para tudo que é coleta** — vídeos, comentários, transcrições, CSVs brutos e analíticos
- **Uma pasta por vídeo** (`data/videos/<videoId>/`) — preserva a correspondência metadados ↔ áudio ↔ transcrição ↔ comentários
- **`.docx` de metodologia fora do repo** — o documento enviado fica como referência local, não versionado
- **Áudios >25 MB fora do repo** — 8 áudios que excedem o limite adotado neste projeto ficam com a pesquisadora
- **Commits claros** — `feat:`, `fix:`, `refactor:`, `docs:` para manter o histórico legível
- **Deploy key SSH da Lídia** — nunca conta/token de terceiros

## Credenciais e acesso

- **Deploy key SSH:** configurada em `~/.ssh/deploy_key_pesquisa_lol_write` (permissão de escrita)
- **Remote:** `github-pesquisa-lol-write:lidibelas/pesquisa_lol.git`
- **NUNCA** use token ou conta GitHub de terceiros aqui

## Estado da análise

O corpus e os dois léxicos ativos já estão disponíveis. A implementação e a execução da nova análise transcrições × visualizações ainda estão pendentes. A análise legada permanece arquivada.

## Contexto acadêmico

- **Pesquisadora:** Lídia Belas (Antropologia/UFBA)
- **Projeto:** pesquisa pessoal (League of Legends / misoginia em gaming)
- **Disciplinas vinculadas:** Métodos Digitais e Laboratório Quantitativo em Ciências Sociais (UFBA)
- **Orientador:** não há orientador formal — a pesquisadora conduz o projeto de forma independente
- **Ferramenta de coleta:** YouTube Data Tools (ytdt.digitalmethods.net)
- **Léxico:** MOL — Misoginia Online em Léxico; v3 revisado para o recorte atual e v2 preservado como legado
- **Referências da análise anterior:** Fernandez et al. (2025) e Lourenço et al. (2022), para codificação binária por categoria

## Contato

- **Lídia Belas:** responsável pelo repositório (pesquisa pessoal)
- **Tutor Hermes (pibic_labhdufba_bot):** agente de apoio à pesquisa
