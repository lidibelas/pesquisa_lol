# Como rodar o MOL v3 — 43 vídeos

No diretório raiz do repositório, com Python 3.9+:

```bash
python3 scripts/analise_mol_v3_videos.py
```

**Sem bibliotecas externas.** O script lê `lexico/mol-lexicon-v3.csv`, as 43 pastas de `data/videos/` e `data/data_base yiok - videos.csv`. Não lê comentários, não altera dados brutos e não sobrescreve resultados antigos.

Cria automaticamente `data/analise/mol_v3/` com:
- `mol_v3_por_video.csv`: uma linha por vídeo, views, duração, formato, data, palavras, ocorrências brutas, taxa MOL por 1.000 palavras e taxas por categoria.
- `mol_v3_ocorrencias.csv`: ocorrências, termos e trechos para auditoria pontual (não é necessária revisão integral para executar).
- `mol_v3_resumo.json`: informações da execução, cobertura e limites.

**Normalização:** a métrica principal é `mol_por_1000_palavras = ocorrencias_mol_brutas / palavras_transcritas * 1000`. É densidade de expressões candidatas, **não** quantidade de misoginia confirmada. O script evita sobreposição entre frases e palavras (por exemplo, `escravo de buceta` versus `buceta`).

**Cuidado metodológico:** as 43 transcrições podem conter erros do Whisper, e as palavras não são desambiguadas semanticamente. A métrica mede incidência lexical de um dicionário operacional. Shorts e vídeos longos têm regimes de distribuição distintos: compare também por `tipo` e não interprete correlação como efeito causal. A coluna `idade_dias_na_execucao` é aproximada; as views vêm do snapshot salvo no CSV e **não são atualizadas**. Sem data de coleta das views, a idade do vídeo na data da medição não pode ser reconstruída com precisão.

**Análise posterior:** gráfico de dispersão `mol_por_1000_palavras` versus `views` (ou `log1p(views)`), Spearman exploratório no conjunto e por formato; verificar outliers e tamanhos de transcrição. Reportar separadamente `n_violencia_sexual_metaforica` e demais categorias.

**Nota:** as referências sobre normalização de frequência lexical justificam a comparação por unidade textual; a escolha de 1.000 palavras é operacional e deve ser documentada, não tratada como medida universal de misoginia.
