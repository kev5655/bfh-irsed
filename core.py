import requests
from dataclasses import dataclass
from typing import Any, List, Optional

from ranking import *


@dataclass
class RankingInfo:
    lang: str
    expected_rank: int
    actual_rank: Optional[int]


@dataclass
class EvaluationResult:
    core: str
    name: str
    solr_query: dict[str, Any]
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


def run_solr_query_post(case, solr_url, rows=30, **additional_params):
    payload = {
        "rows": rows,
        "wt": "json"
    }

    is_dismax = additional_params.get('defType') in ['dismax', 'edismax']

    if is_dismax:
        # Für DisMax/eDisMax: Nur den Suchbegriff verwenden
        query = case.get('query', '')

        # Boost-Faktor hinzufügen, falls vorhanden
        if 'boost' in case and case['boost']:
            query = f"{query}^{case['boost']}"

        # Filterabfrage hinzufügen, falls vorhanden
        if 'filter_query' in case and case['filter_query']:
            payload['fq'] = case['filter_query']

        payload["q"] = query
        payload.update(additional_params)

    else:
        payload["q"] = case.get('standard_query') or case.get('query')

    print(f"DEBUG - Sending to Solr: {payload}")

    resp = requests.post(solr_url, data=payload)
    resp.raise_for_status()
    return resp.json()["response"]["docs"], payload


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


def evaluate_case(case, solr_url, core, **query_params):
    docs, query_payload = run_solr_query_post(
        case, solr_url, 30, **query_params)
    expected_langs = {x["lang"] for x in case["expected_langs"]}
    found_langs = []
    for doc in docs:
        lang = doc.get('title').replace("(programming language)", "").strip()
        found_langs.append(lang)

    found_langs_set = set(found_langs)

    tp_langs, fp_langs, fn_langs = compute_lang_sets(
        expected_langs, found_langs_set)
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
        "name": case.get('standard_query') or case.get('query', ''),
        "solr_query": query_payload,
        "tp": tp, "fp": fp, "fn": fn,
        "s1_pre": pre, "s1_rec": rec, "s1_f1": f1,
        "found_langs": list(found_langs),
        "expected_langs": list(expected_langs),
        "ranking": ranking_info,
        "ranking_score": ranking_score,
        "ranking_score_sperman": compute_spearman_correlation(ranking_info),
        "ranking_score_ndcg": compute_ndcg(ranking_info),
        "ranking_score_weighted": compute_weighted_rank_deviation(ranking_info),
        "ranking_score_mrr": compute_mrr(ranking_info)
    }
