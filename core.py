import requests
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RankingInfo:
    lang: str
    expected_rank: int
    actual_rank: Optional[int]


@dataclass
class EvaluationResult:
    core: str
    name: str
    tp: int
    fp: int
    fn: int
    s1_pre: float
    s1_rec: float
    s1_f1: float
    found_langs: List[str]
    expected_langs: List[str]
    ranking: List[RankingInfo]
    ranking_score: float


def precision(TP, FP):
    """Precision = TP / (TP + FP)"""
    if TP + FP == 0:
        return 0
    return float(TP / (TP + FP))


def recall(TP, FN):
    """Recall = TP / (TP + FN)"""
    if TP + FN == 0:
        return 0
    return float(TP / (TP + FN))


def f1_score(precision, recall):
    """F1-Score = 2 * (precision * recall) / (precision + recall)"""
    if precision + recall == 0:
        return 0
    return float(2 * (precision * recall) / (precision + recall))


def needs_quoting(term: str) -> bool:
    return any(ch.isspace() for ch in term)


def build_solr_query(case):
    return case['name']


def run_solr_query_post(query: str, solr_url: str, rows: int = 30):
    payload = {
        "q":  query,
        "rows": rows,
        "wt": "json",
    }
    resp = requests.post(solr_url, data=payload)
    resp.raise_for_status()
    return resp.json()["response"]["docs"]


def compute_lang_sets(expected_langs, found_langs):
    tp = found_langs & expected_langs
    fp = found_langs - expected_langs
    fn = expected_langs - found_langs
    return tp, fp, fn


def evaluate_ranking(case, found_langs):
    ranking_results = []
    found_ranking = {}
    for i, lang in enumerate(found_langs):
        found_ranking[lang] = i + 1

    for expected in case["expected_langs"]:
        lang = expected["lang"]
        expected_rank = expected["rank"]
        actual_rank = found_ranking.get(lang, None)
        ranking_results.append({
            "lang": lang,
            "expected_rank": expected_rank,
            "actual_rank": actual_rank
        })
    return ranking_results


def compute_normalized_ranking_score(ranking_info):
    """
    Normalisierte Metrik: Durchschnittliche Abweichung geteilt durch
    den höchsten erwarteten Rang.
    """
    total_diff = 0
    count = 0
    max_expected_rank = 0
    for r in ranking_info:
        expected_rank = r["expected_rank"]
        actual_rank = r["actual_rank"]
        if actual_rank is not None:
            total_diff += abs(expected_rank - actual_rank)
            count += 1
        if expected_rank > max_expected_rank:
            max_expected_rank = expected_rank
    if count == 0 or max_expected_rank == 0:
        return 0
    return (total_diff / count) / max_expected_rank


def evaluate_case(case, solr_url, core):
    query = build_solr_query(case)
    docs = run_solr_query_post(query, solr_url)
    expected_langs = {x["lang"] for x in case["expected_langs"]}
    found_langs = {doc.get('title').replace(
        "(programming language)", "").strip() for doc in docs}

    tp_langs, fp_langs, fn_langs = compute_lang_sets(
        expected_langs, found_langs)
    tp, fp, fn = len(tp_langs), len(fp_langs), len(fn_langs)

    pre = precision(tp, fp)
    rec = recall(tp, fn)
    f1 = f1_score(pre, rec)

    # Debug
    # print(f"[{case['name']} @ {core}]")
    # print(f"  Solr-Query = {query}")
    # print(f"  Expected   = {sorted(expected_langs)}")
    # print(f"  Found      = {sorted(found_langs)}")
    # print(f"  TP={tp}, FP={fp}, FN={fn}")
    # print(f"  Precision={pre:.2f}, Recall={rec:.2f}, F1={f1:.2f}\n")

    print("Ranking-Abgleich:")
    ranking_info = evaluate_ranking(case, found_langs)
    ranking_score = compute_normalized_ranking_score(ranking_info)

    return {
        "core": core,
        "name": case["name"],
        "tp": tp, "fp": fp, "fn": fn,
        "s1_pre": pre, "s1_rec": rec, "s1_f1": f1,
        "found_langs": list(found_langs),
        "expected_langs": list(expected_langs),
        "ranking": ranking_info,
        "ranking_score": ranking_score
    }
