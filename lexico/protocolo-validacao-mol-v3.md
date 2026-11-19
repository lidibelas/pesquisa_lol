# Protocolo rápido — revisão provisória do léxico MOL v3

## Objetivo e unidade

Investigar a associação entre **frequência de expressões misóginas nas falas dos vídeos** e visualizações, em 43 vídeos do canal Yiok. Unidade quantitativa: vídeo. Fonte textual: **transcrições**. Comentários e frequências oriundas dos comentários são históricos e **não compõem a nova análise**.

## Por que revisar

O MOL v2 reúne 92 termos de oito categorias, mas contém palavras genéricas (por exemplo, `caralho`, `pica`), gírias (`gado`, `egirl`) e palavras ambíguas (`baleia`) cuja presença não comprova misoginia. O arquivo `mol-v3-triagem.csv` é uma **triagem de risco de falso positivo**, não validação empírica.

## Critérios operacionais

1. **Misoginia contextual confirmada:** a expressão, interpretada na frase e no contexto da fala, inferioriza, sexualiza de modo depreciativo, deslegitima ou hostiliza mulheres por gênero, ou reproduz estereótipos sexistas de competência, comportamento ou sexualidade.
2. **Expressão ambígua:** palavra que pode assumir sentido misógino, mas exige exame de alvo, co-texto, ironia, citação e enunciador. **Não contabilizar automaticamente**.
3. **Não evidência de misoginia:** palavrão genérico, gíria técnica, nome próprio, metáfora ou insulto sem componente de gênero demonstrável. Excluir da contagem de misoginia.
4. **Outras discriminações:** racismo, homofobia e humilhação corporal devem ser registrados separadamente, e só codificados como misoginia interseccional quando houver componente de gênero identificável.
5. **Citação ou crítica:** distinguir fala que endossa insulto de fala que o relata, cita ou condena.

## Procedimento mínimo

- Buscar cada expressão nas **43 transcrições**, preservando janela de contexto e ID do vídeo.
- Anotar ocorrência, contexto curto, alvo, classe (`confirmada`, `ambigua`, `nao_misogina`) e justificativa.
- Se houver tempo, fazer dupla anotação de uma amostra e discutir discordâncias; se não houver, declarar a limitação.
- Calcular a frequência **confirmada** por mil palavras em cada vídeo. Reportar frequência bruta separadamente como análise de sensibilidade, não como sinônimo de misoginia.
- Conferir datas de publicação e aferição das visualizações; explorar associação (por exemplo, Spearman), sem inferir causalidade.

## Fundamentação bibliográfica inicial

- **Bassignana, E.; Basile, V.; Patti, V. (2018).** HurtLex: A Multilingual Lexicon of Words to Hurt. *CLiC-it*. https://aclanthology.org/2018.clicit-1.11/ — sustenta léxicos de linguagem ofensiva, **não** equivalência entre ofensa e misoginia.
- **Waseem, Z.; Hovy, D. (2016).** Hateful Symbols or Hateful People? Predictive Features for Hate Speech Detection on Twitter. *NAACL Student Research Workshop*. https://aclanthology.org/N16-2013/ — critérios para anotação de linguagem sexista e racista.
- **Jane, E. A. (2014).** 'Your a Ugly, Whorish, Slut': Understanding E-bile. *Feminist Media Studies*, 14(4), 531–546. https://doi.org/10.1080/14680777.2012.741073 — misoginia e hostilidade dirigida a mulheres em ambientes digitais.
- **Kendall, L. (2002).** *Hanging Out in the Virtual Pub: Masculinities and Relationships Online*. University of California Press — linguagem e masculinidades em sociabilidades digitais.
- **Consalvo, M. (2007).** *Cheating: Gaining Advantage in Videogames*. MIT Press — cultura, normas e práticas em jogos digitais.

## Texto metodológico utilizável

A operacionalização da misoginia parte de um léxico de expressões candidatas, submetidas a revisão contextual nas transcrições dos vídeos. A literatura sobre léxicos ofensivos permite localizar ocorrências potencialmente relevantes, mas não autoriza equiparar automaticamente palavrões, gírias de jogos e referências sexuais a ataques misóginos (Bassignana, Basile e Patti, 2018). Assim, a codificação distingue manifestações de inferiorização ou deslegitimação por gênero, usos ambíguos e usos não misóginos, considerando alvo, contexto enunciativo e expressões próprias da comunidade de League of Legends. O glossário gamer funciona como instrumento auxiliar de interpretação e prevenção de falsos positivos. Para cada vídeo, a medida principal será a frequência de ocorrências contextualmente confirmadas por mil palavras; as visualizações serão obtidas dos metadados do YouTube. O desenho é observacional e exploratório, sem pretensão de estabelecer causalidade.

**Limite explícito:** esta documentação e triagem não significam que as transcrições foram codificadas, nem que a variável ou a correlação já foram calculadas.
