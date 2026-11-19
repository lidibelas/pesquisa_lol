#!/usr/bin/env python3
"""MOL v3: contagem lexical automatizada por vídeo, sem classificação contextual.
Uso: python3 scripts/analise_mol_v3_videos.py
Não modifica transcrições, comentários nem resultados anteriores.
"""
import csv
import json
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEXICO = ROOT / "lexico/mol-lexicon-v3.csv"
VIDEOS = ROOT / "data/videos"
META = ROOT / "data/data_base yiok - videos.csv"
OUT = ROOT / "data/analise/mol_v3"
WORD = re.compile(r"\b\w+\b", re.UNICODE)
STAMP = re.compile(r"\[\s*\d+(?:\.\d+)?\s*-\s*\d+(?:\.\d+)?\s*\]")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")

def normalize(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(ch for ch in s if not unicodedata.combining(ch))

def load_lexicon():
    entries = []
    seen = set()
    with LEXICO.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            term, cat = normalize(row["termo"].strip()), row["categoria"].strip()
            if not term or not cat or (term, cat) in seen:
                continue
            seen.add((term, cat))
            # whitespace-tolerant multiword patterns, full-word boundaries
            expr = r"(?<!\w)" + r"\s+".join(re.escape(p) for p in term.split()) + r"(?!\w)"
            entries.append((term, cat, re.compile(expr)))
    return sorted(entries, key=lambda e: (-len(e[0]), e[0]))

def read_transcript(video_id):
    # CSV segments are preferable because they contain speech without timestamps.
    path = VIDEOS / video_id / (video_id + "_transcricao.csv")
    if path.exists():
        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames or []
            field = next((x for x in ("texto", "text", "transcricao") if x in fields), None)
            if field:
                return " ".join(row.get(field, "") for row in reader), "csv"
    path = VIDEOS / video_id / (video_id + "_transcricao.txt")
    if path.exists():
        return STAMP.sub(" ", path.read_text(encoding="utf-8-sig")), "txt"
    return None, "ausente"

def get_metadata():
    with META.open(encoding="utf-8-sig", newline="") as f:
        return {r["videoId"]: r for r in csv.DictReader(f)}

def write_csv(path, rows, columns):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def main():
    lex = load_lexicon()
    categories = sorted({c for _, c, _ in lex})
    metadata = get_metadata()
    OUT.mkdir(parents=True, exist_ok=True)
    results, occurrences, missing = [], [], []
    now = datetime.now(timezone.utc)
    for vid, meta in sorted(metadata.items()):
        raw, source = read_transcript(vid)
        if raw is None:
            missing.append(vid)
            continue
        txt = normalize(raw)
        n_words = len(WORD.findall(txt))
        candidates = []
        for term, cat, regex in lex:
            for match in regex.finditer(txt):
                candidates.append((match.start(), match.end(), term, cat))
        # Avoid double counting nested expressions, e.g. 'escravo de buceta' and 'buceta'.
        candidates.sort(key=lambda x: (x[0], -(x[1]-x[0]), x[2]))
        chosen = []
        for candidate in candidates:
            a, b = candidate[:2]
            if not any(a < old[1] and b > old[0] for old in chosen):
                chosen.append(candidate)
        by_cat = Counter(cat for _, _, _, cat in chosen)
        views_raw = meta.get("viewCount", "").strip()
        try:
            views = int(float(views_raw))
        except ValueError:
            views = ""
        pub = meta.get("publishedAt", "")
        try:
            published = datetime.fromisoformat(pub.replace("Z", "+00:00"))
            age_days = round((now-published).total_seconds()/86400, 2)
        except ValueError:
            age_days = ""
        duration = meta.get("durationSec", "")
        try:
            duration = int(float(duration))
        except ValueError:
            duration = ""
        n = len(chosen)
        row = {
            "videoId": vid, "titulo": meta.get("videoTitle", ""),
            "tipo": meta.get("tipo", ""), "categoria_video": meta.get("categoria_video", ""),
            "publishedAt": pub, "views": views, "idade_dias_na_execucao": age_days,
            "duracao_segundos": duration, "fonte_transcricao": source,
            "palavras_transcritas": n_words, "ocorrencias_mol_brutas": n,
            "mol_por_1000_palavras": round(1000*n/n_words, 4) if n_words else "",
            "flag_mol": int(n > 0),
        }
        for cat in categories:
            row["n_"+cat] = by_cat[cat]
            row["taxa_"+cat+"_1000"] = round(1000*by_cat[cat]/n_words, 4) if n_words else ""
        results.append(row)
        for a,b,term,cat in sorted(chosen):
            occurrences.append({
                "videoId":vid,"termo":term,"categoria":cat,
                "posicao_caractere":a,
                "trecho":raw[max(0,a-65):b+65].replace("\n"," ") if source=="txt" else txt[max(0,a-65):b+65],
            })
    if not results:
        raise RuntimeError("Nenhuma transcrição encontrada.")
    columns = list(results[0])
    write_csv(OUT/"mol_v3_por_video.csv",results,columns)
    write_csv(OUT/"mol_v3_ocorrencias.csv",occurrences,["videoId","termo","categoria","posicao_caractere","trecho"])
    summary = {
        "versao":"MOL v3 provisório","data_execucao_utc":now.isoformat(),
        "videos_metadados":len(metadata),"videos_analisados":len(results),
        "videos_sem_transcricao":missing,"entradas_lexico":len(lex),
        "total_ocorrencias":sum(r["ocorrencias_mol_brutas"] for r in results),
        "nota":"Correspondência lexical automática, não misoginia validada; sem inferência causal. Visualizações são snapshot dos metadados, não valores atuais.",
        "denominador":"palavras transcritas; por 1000 palavras",
        "observacao":"Shorts e vídeos longos possuem dinâmicas de visualização diferentes; comparar por formato."
    }
    (OUT/"mol_v3_resumo.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Vídeos analisados:",len(results),"/",len(metadata))
    print("Ocorrências lexicais:",summary["total_ocorrencias"])
    print("Resultados em:",OUT)
    if missing: print("SEM TRANSCRIÇÃO:",", ".join(missing))
    if len(results)!=43: print("ATENÇÃO: esperado corpus de 43 vídeos.")
    print("IMPORTANTE: views são os valores salvos no CSV de metadados, não atualizados pela API.")
if __name__=="__main__":
    main()
