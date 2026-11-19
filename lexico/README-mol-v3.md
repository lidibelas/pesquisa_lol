# MOL v3 provisório — como usar

Dicionário reconstruído para **transcrições de 43 vídeos**, não comentários. O v2 permanece preservado. Os termos do CSV são **gatilhos de revisão contextual**, não manifestações confirmadas automaticamente.

## Critérios
- `violencia_sexual_metaforica`: registrar usos de estupro para descrever derrota, superioridade e dominação; separar referência literal, ameaça e crítica.
- `insultos_sexistas`: verificar alvo e componente de gênero.
- `deslegitimacao_gamer_genero`: verificar se expressões como `boostada`, `bustada`, `webgado`, `e-girl` deslegitimam mulheres; usos neutros não contam.
- `objetificacao_sexual`: verificar sexualização depreciativa e contexto; `buceta` isoladamente não comprova misoginia.
- `humilhacao_corporal_genero`: verificar alvo e gênero; não contar qualquer menção a peso.
- `policiamento_genero`: examinar julgamentos sobre aparência e feminilidade.
- `homofobia_transfobia_contextual`: dimensão própria, não sinonímia de misoginia.
- `frases_sexistas`: localizar expressões compostas e ler frase completa.

## Evidências exemplares
- `slhtOG9uSmQ`: “A play do estupro que deu merda.”
- `ifSpvNYqE2g`: “O cara não pode me estuprar assim, não, mano.”
- `Cyai8_m_ZQ8`: “Ela foi bustada pelo web namoradinho dela” — conferir áudio.
- `92KeIj8hsOE`: “escravo de buceta”.
- `SBT6DCNR4BY`: “Você não acha que essa voz dela é pouco feminina?”

## Aplicação
Revisar cada ocorrência com ID de vídeo, trecho, alvo e decisão (`confirmada`, `ambigua`, `nao_confirmada`). Conferir áudio em erros de Whisper, especialmente `bustada` e `estuprindo`. Calcular ocorrências **confirmadas por 1.000 palavras** por vídeo, distinguindo misoginia diretamente sexista de banalização da violência sexual.

**Atenção:** `scripts/analise_lexical.py` ainda lê comentários e sobrescreve tabelas históricas. **Não executar o script antigo diretamente com este CSV** antes de adaptá-lo ao novo desenho.

Referências iniciais: Bassignana, Basile e Patti (2018), *HurtLex*, https://aclanthology.org/2018.clicit-1.11/; Waseem e Hovy (2016), *Hateful Symbols or Hateful People?*, https://aclanthology.org/N16-2013/.
