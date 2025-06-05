from scipy.stats import spearmanr
import numpy as np


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


def compute_spearman_correlation(ranking_info):
    """
    Spearman's Rangkorrelationskoeffizient.
    Bewertet die Korrelation zwischen erwartetem und tatsächlichem Ranking.
    Werte zwischen -1 und 1 (1 = perfekte Übereinstimmung).
    """

    # Extrahiere nur die Paare, wo beide Ränge vorhanden sind
    pairs = [(r["expected_rank"], r["actual_rank"])
             for r in ranking_info if r["actual_rank"] is not None]

    if len(pairs) < 2:  # Spearman braucht mindestens 2 Punkte
        return 0

    expected_ranks, actual_ranks = zip(*pairs)
    correlation, _ = spearmanr(expected_ranks, actual_ranks)
    return correlation


def compute_ndcg(ranking_info, k=10):
    """
    Normalized Discounted Cumulative Gain (NDCG).
    Bewertet die Qualität des Rankings mit Fokus auf die Top-k Ergebnisse.
    Werte zwischen 0 und 1 (1 = ideal).
    """

    # Ideale Reihenfolge für DCG
    ideal_order = sorted(ranking_info, key=lambda x: x["expected_rank"])

    # Tatsächliche Reihenfolge
    actual_order = sorted([r for r in ranking_info if r["actual_rank"] is not None],
                          key=lambda x: x["actual_rank"])

    if not actual_order:
        return 0

    # DCG für die tatsächliche Reihenfolge berechnen
    dcg = 0
    for i, item in enumerate(actual_order[:k]):
        # Relevanz wird umgekehrt berechnet: niedrigerer Rang = höhere Relevanz
        relevance = max(1, len(ranking_info) - item["expected_rank"] + 1)
        # DCG-Formel: (2^rel - 1) / log2(i+2)
        dcg += (2**relevance - 1) / np.log2(i + 2)

    # IDCG für die ideale Reihenfolge berechnen
    idcg = 0
    for i, item in enumerate(ideal_order[:k]):
        relevance = max(1, len(ranking_info) - item["expected_rank"] + 1)
        idcg += (2**relevance - 1) / np.log2(i + 2)

    if idcg == 0:
        return 0

    return dcg / idcg


def compute_weighted_rank_deviation(ranking_info):
    """
    Gewichtete Rangabweichung - Abweichungen bei Top-Rankings werden stärker bestraft.
    Je niedriger der Wert, desto besser (0 = ideal).
    """
    total_weighted_diff = 0
    count = 0

    for r in ranking_info:
        expected_rank = r["expected_rank"]
        actual_rank = r["actual_rank"]

        if actual_rank is not None:
            # Wichtung basierend auf erwartetem Rang: frühere Ränge wiegen mehr
            weight = 1.0 / expected_rank
            total_weighted_diff += abs(expected_rank - actual_rank) * weight
            count += 1

    if count == 0:
        return 0

    return total_weighted_diff / count


def compute_mrr(ranking_info, expected_top_k=5):
    """
    Mean Reciprocal Rank (MRR).
    Bewertet die Position der ersten erwarteten Top-k Sprachen.
    Werte zwischen 0 und 1 (1 = ideal).
    """
    # Berücksichtige nur die Top-k erwarteten Sprachen
    top_langs = sorted([r for r in ranking_info if r["expected_rank"] <= expected_top_k],
                       key=lambda x: x["expected_rank"])

    reciprocal_ranks = []
    for r in top_langs:
        if r["actual_rank"] is not None:
            reciprocal_ranks.append(1.0 / r["actual_rank"])
        else:
            reciprocal_ranks.append(0)  # Nicht gefunden = 0

    if not reciprocal_ranks:
        return 0

    return sum(reciprocal_ranks) / len(reciprocal_ranks)
