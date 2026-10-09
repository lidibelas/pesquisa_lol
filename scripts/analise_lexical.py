#!/usr/bin/env python3
"""
Análise léxica MOL — versão 2 (out/2026)
Aplica o léxico MOL melhorado em:
  1. Comentários (data/comentarios/data_base yiok - comentários.csv)
  2. Transcrições de vídeos (data/videos/*/[videoId]_transcricao.csv)

Gera:
  - Base analítica unificada (comentários + transcrições) com codificação binária por categoria
  - Crosstab vídeo × categorias (comentários)
  - Crosstab vídeo × categorias (transcrições)
  - Resumo estatístico
  - CSVs prontos para análise

Uso:
  python3 scripts/analise_lexical.py [--lexico lexico/mol-lexicon-v2.csv]
"""

import csv
import json
import os
import re
import sys
import argparse
from collections import defaultdict
from pathlib import Path

# === CAMINHOS ===
BASE = Path(__file__).resolve().parent.parent
COMMENTS_CSV = BASE / "data" / "comentarios" / "data_base yiok - comentários.csv"
VIDEOS_CSV = BASE / "data" / "data_base yiok - videos.csv"
VIDEOS_DIR = BASE / "data" / "videos"
LEXICO_DEFAULT = BASE / "lexico" / "mol-lexicon.csv"
OUTPUT_DIR = BASE / "data" / "analise"


def carregar_lexico(caminho):
    """Carrega o léxico do CSV. Retorna dict {categoria: [termos]}."""
    categorias = defaultdict(list)
    with open(caminho, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            termo = row["termo"].strip().lower()
            cat = row["categoria"].strip()
            if termo and cat:
                categorias[cat].append(termo)
    
    # Compilar regex para cada termo (word boundary, case-insensitive)
    lexico_regex = {}
    for cat, termos in categorias.items():
        # Escapar termos que contêm caracteres especiais (@, 3, etc)
        padroes = []
        for t in termos:
            # Substituir @ por variantes (a/@/3) — léxico pode ter ob3sinh@s etc
            if "@" in t:
                t_variants = [t.replace("@", "a"), t.replace("@", "o"), t.replace("@", "3")]
                for v in t_variants:
                    padroes.append(re.escape(v))
            else:
                padroes.append(re.escape(t))
        
        # Juntar todos os padrões da categoria em uma regex
        if padroes:
            regex = re.compile(r"\b(" + "|".join(padroes) + r")\b", re.IGNORECASE)
            lexico_regex[cat] = (regex, termos)
    
    return categorias, lexico_regex


def analisar_texto(texto, lexico_regex):
    """Analisa um texto e retorna: {categoria: count}, termos_encontrados, n_matches, flag."""
    if not texto:
        return {}, [], 0, 0
    
    texto_lower = texto.lower()
    cats_found = {}
    termos_encontrados = []
    n_matches = 0
    
    for cat, (regex, termos) in lexico_regex.items():
        matches = regex.findall(texto_lower)
        if matches:
            cats_found[cat] = len(matches)
            termos_encontrados.extend(matches)
            n_matches += len(matches)
    
    flag = 1 if cats_found else 0
    return cats_found, termos_encontrados, n_matches, flag


def carregar_comentarios():
    """Carrega comentários brutos."""
    with open(COMMENTS_CSV, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def carregar_transcricoes():
    """Carrega todas as transcrições CSV. Retorna lista de segmentos."""
    segmentos = []
    for video_dir in VIDEOS_DIR.iterdir():
        if not video_dir.is_dir():
            continue
        video_id = video_dir.name
        transc_csv = video_dir / f"{video_id}_transcricao.csv"
        if transc_csv.exists():
            with open(transc_csv, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    segmentos.append({
                        "videoId": video_id,
                        "segmento": row.get("segmento", ""),
                        "inicio_s": row.get("inicio_s", ""),
                        "fim_s": row.get("fim_s", ""),
                        "texto": row.get("texto", ""),
                    })
    return segmentos


def carregar_videos():
    """Carrega metadados dos vídeos."""
    with open(VIDEOS_CSV, "r", encoding="utf-8") as f:
        return {v["videoId"]: v for v in csv.DictReader(f)}


def analisar_comentarios(comentarios, lexico_regex):
    """Aplica léxico nos comentários. Retorna lista de dict com codificação binária."""
    # Categorias do léxico
    categorias = list(lexico_regex.keys())
    
    resultados = []
    for c in comentarios:
        texto = c.get("text", "")
        cats_found, termos, n_matches, flag = analisar_texto(texto, lexico_regex)
        
        row = {
            "videoId": c["videoId"],
            "commentId": c.get("id", ""),
            "publishedAt": c.get("publishedAt", ""),
            "authorName": c.get("authorName", ""),
            "likeCount": c.get("likeCount", "0"),
            "isReply": c.get("isReply", "0"),
            "text": texto,
            "n_matches": n_matches,
            "flag_mol": flag,
            "termos_encontrados": "; ".join(sorted(set(termos))),
            "categorias_encontradas": "; ".join(sorted(cats_found.keys())),
        }
        # Codificação binária por categoria
        for cat in categorias:
            row[f"cat_{cat}"] = 1 if cat in cats_found else 0
        
        resultados.append(row)
    
    return resultados, categorias


def analisar_transcricoes(segmentos, lexico_regex):
    """Aplica léxico nas transcrições. Retorna lista de dict com codificação binária."""
    categorias = list(lexico_regex.keys())
    
    resultados = []
    for s in segmentos:
        texto = s.get("texto", "")
        cats_found, termos, n_matches, flag = analisar_texto(texto, lexico_regex)
        
        row = {
            "videoId": s["videoId"],
            "segmento": s.get("segmento", ""),
            "inicio_s": s.get("inicio_s", ""),
            "fim_s": s.get("fim_s", ""),
            "texto": texto,
            "n_matches": n_matches,
            "flag_mol": flag,
            "termos_encontrados": "; ".join(sorted(set(termos))),
            "categorias_encontradas": "; ".join(sorted(cats_found.keys())),
        }
        for cat in categorias:
            row[f"cat_{cat}"] = 1 if cat in cats_found else 0
        
        resultados.append(row)
    
    return resultados, categorias


def gerar_crosstab(resultados, categorias, videos_info, chave="videoId"):
    """Gera crosstab: vídeo × categorias."""
    vid_data = defaultdict(lambda: {
        "total": 0, "flagged": 0, "cats": [0] * len(categorias)
    })
    
    for r in resultados:
        vid = r[chave]
        vid_data[vid]["total"] += 1
        if r["flag_mol"] == 1:
            vid_data[vid]["flagged"] += 1
        for i, cat in enumerate(categorias):
            if r[f"cat_{cat}"] == 1:
                vid_data[vid]["cats"][i] += 1
    
    rows = []
    for vid, data in sorted(vid_data.items(), key=lambda x: -x[1]["flagged"]):
        v = videos_info.get(vid, {})
        pct = (data["flagged"] / data["total"] * 100) if data["total"] > 0 else 0
        row = {
            "videoId": vid,
            "titulo": v.get("videoTitle", "?")[:60],
            "tipo": v.get("tipo", ""),
            "views": v.get("viewCount", ""),
            "total_unidades": data["total"],
            "flagged_mol": data["flagged"],
            "pct_flagged": round(pct, 1),
        }
        for i, cat in enumerate(categorias):
            row[f"cat_{cat}"] = data["cats"][i]
        rows.append(row)
    
    return rows


def gerar_resumo(resultados, categorias, label="comentários"):
    """Gera resumo estatístico."""
    total = len(resultados)
    flagged = sum(1 for r in resultados if r["flag_mol"] == 1)
    
    metrics = [
        ("total_unidades", total),
        ("unidades_flagged", flagged),
        ("unidades_nao_flagged", total - flagged),
        ("pct_flagged", round(flagged / total * 100, 1) if total > 0 else 0),
        ("max_flagged_por_unidade", max((r["n_matches"] for r in resultados), default=0)),
        ("media_matches_por_unidade", round(sum(r["n_matches"] for r in resultados) / total, 2) if total > 0 else 0),
    ]
    
    cat_freq = []
    for cat in categorias:
        count = sum(1 for r in resultados if r[f"cat_{cat}"] == 1)
        pct = round(count / flagged * 100, 1) if flagged > 0 else 0
        cat_freq.append((cat, count, pct))
    
    return metrics, cat_freq


def salvar_csv(rows, path, fieldnames=None):
    """Salva lista de dict em CSV."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not rows:
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Análise léxica MOL v2")
    parser.add_argument("--lexico", default=str(LEXICO_DEFAULT), help="Caminho do léxico CSV")
    args = parser.parse_args()
    
    print("=" * 60)
    print("ANÁLISE LÉXICA MOL — versão 2 (out/2026)")
    print("=" * 60)
    
    # 1. Carregar léxico
    print(f"\n📖 Carregando léxico: {args.lexico}")
    categorias, lexico_regex = carregar_lexico(args.lexico)
    total_termos = sum(len(t) for t in categorias.values())
    print(f"   {len(categorias)} categorias, {total_termos} termos")
    for cat, termos in categorias.items():
        print(f"   • {cat}: {len(termos)} termos")
    
    # 2. Carregar dados
    print(f"\n📥 Carregando comentários...")
    comentarios = carregar_comentarios()
    print(f"   {len(comentarios)} comentários")
    
    print(f"\n📥 Carregando transcrições...")
    segmentos = carregar_transcricoes()
    print(f"   {len(segmentos)} segmentos de transcrição")
    
    print(f"\n📥 Carregando metadados de vídeos...")
    videos_info = carregar_videos()
    print(f"   {len(videos_info)} vídeos")
    
    # 3. Analisar comentários
    print(f"\n🔍 Analisando comentários com léxico MOL...")
    resultados_com, cats = analisar_comentarios(comentarios, lexico_regex)
    flagged_com = sum(1 for r in resultados_com if r["flag_mol"] == 1)
    print(f"   {flagged_com} comentários flagged ({flagged_com/len(resultados_com)*100:.1f}%)")
    
    # 4. Analisar transcrições
    print(f"\n🔍 Analisando transcrições com léxico MOL...")
    resultados_tr, cats_tr = analisar_transcricoes(segmentos, lexico_regex)
    flagged_tr = sum(1 for r in resultados_tr if r["flag_mol"] == 1)
    print(f"   {flagged_tr} segmentos flagged ({flagged_tr/len(resultados_tr)*100:.1f}%)")
    
    # 5. Gerar crosstabs
    print(f"\n📊 Gerando crosstabs...")
    crosstab_com = gerar_crosstab(resultados_com, cats, videos_info)
    crosstab_tr = gerar_crosstab(resultados_tr, cats, videos_info)
    
    # 6. Gerar resumos
    print(f"\n📊 Gerando resumos estatísticos...")
    metrics_com, catfreq_com = gerar_resumo(resultados_com, cats, "comentários")
    metrics_tr, catfreq_tr = gerar_resumo(resultados_tr, cats, "transcrições")
    
    # 7. Salvar tudo
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    salvar_csv(resultados_com, OUTPUT_DIR / "base_analitica_comentarios_mol.csv")
    salvar_csv(resultados_tr, OUTPUT_DIR / "base_analitica_transcricoes_mol.csv")
    salvar_csv(crosstab_com, OUTPUT_DIR / "crosstab_comentarios_video_categorias.csv")
    salvar_csv(crosstab_tr, OUTPUT_DIR / "crosstab_transcricoes_video_categorias.csv")
    
    # Resumo combinado
    resumo_rows = []
    for m, v in metrics_com:
        resumo_rows.append({"dimensao": "comentários", "metrica": m, "valor": v})
    for cat, freq, pct in catfreq_com:
        resumo_rows.append({"dimensao": "comentários", "metrica": f"cat_{cat}", "valor": freq, "pct_flagged": pct})
    for m, v in metrics_tr:
        resumo_rows.append({"dimensao": "transcrições", "metrica": m, "valor": v})
    for cat, freq, pct in catfreq_tr:
        resumo_rows.append({"dimensao": "transcrições", "metrica": f"cat_{cat}", "valor": freq, "pct_flagged": pct})
    salvar_csv(resumo_rows, OUTPUT_DIR / "resumo_estatistico_mol.csv",
               fieldnames=["dimensao", "metrica", "valor", "pct_flagged"])
    
    # Flagged detalhado
    flagged_com_rows = [r for r in resultados_com if r["flag_mol"] == 1]
    flagged_tr_rows = [r for r in resultados_tr if r["flag_mol"] == 1]
    salvar_csv(flagged_com_rows, OUTPUT_DIR / "comentarios_flagged_mol.csv")
    salvar_csv(flagged_tr_rows, OUTPUT_DIR / "transcricoes_flagged_mol.csv")
    
    print(f"\n✅ Arquivos gerados em {OUTPUT_DIR}/:")
    for f in sorted(OUTPUT_DIR.iterdir()):
        print(f"   {f.name} ({f.stat().st_size} bytes)")
    
    # Resumo final
    print(f"\n{'=' * 60}")
    print(f"RESUMO FINAL")
    print(f"{'=' * 60}")
    print(f"COMENTÁRIOS: {len(resultados_com)} total, {flagged_com} flagged ({flagged_com/len(resultados_com)*100:.1f}%)")
    print(f"TRANSCRIÇÕES: {len(resultados_tr)} segmentos, {flagged_tr} flagged ({flagged_tr/len(resultados_tr)*100:.1f}%)")
    print(f"\nCategorias mais frequentes em comentários:")
    for cat, freq, pct in sorted(catfreq_com, key=lambda x: -x[1])[:5]:
        print(f"  {cat}: {freq} ({pct}%)")
    print(f"\nCategorias mais frequentes em transcrições:")
    for cat, freq, pct in sorted(catfreq_tr, key=lambda x: -x[1])[:5]:
        print(f"  {cat}: {freq} ({pct}%)")


if __name__ == "__main__":
    main()