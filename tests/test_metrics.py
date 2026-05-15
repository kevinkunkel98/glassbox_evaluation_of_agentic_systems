import pandas as pd
import pytest
from src.metrics import compute_metrics, load_results, load_labels, merge_for_evaluation


def make_labels_df():
    return pd.DataFrame([
        {"step_id": "inst_0000", "tool_selection": 1, "parameter_quality": 1, "step_coherence": 1},
        {"step_id": "inst_0001", "tool_selection": 0, "parameter_quality": 1, "step_coherence": 0},
        {"step_id": "inst_0002", "tool_selection": 1, "parameter_quality": 0, "step_coherence": 1},
        {"step_id": "inst_0003", "tool_selection": 0, "parameter_quality": 0, "step_coherence": 0},
    ])


def make_results_df():
    rows = []
    # tool_selection / zero_shot: predict all 1 → gets 2/4 correct (agrees with label on inst_0000, inst_0002)
    for step_id, pred in [("inst_0000", 1), ("inst_0001", 1), ("inst_0002", 1), ("inst_0003", 1)]:
        rows.append({"step_id": step_id, "dimension": "tool_selection", "variant": "zero_shot", "label": pred, "reasoning": ""})
    # tool_selection / few_shot: perfect
    for step_id, pred in [("inst_0000", 1), ("inst_0001", 0), ("inst_0002", 1), ("inst_0003", 0)]:
        rows.append({"step_id": step_id, "dimension": "tool_selection", "variant": "few_shot", "label": pred, "reasoning": ""})
    return pd.DataFrame(rows)


def test_merge_for_evaluation():
    labels = make_labels_df()
    results = make_results_df()
    merged = merge_for_evaluation(results, labels)
    assert "human_label" in merged.columns
    assert "llm_label" in merged.columns
    assert len(merged) > 0


def test_compute_metrics_perfect():
    labels = make_labels_df()
    results = make_results_df()
    merged = merge_for_evaluation(results, labels)
    perfect = merged[(merged["dimension"] == "tool_selection") & (merged["variant"] == "few_shot")]
    acc, kappa = compute_metrics(perfect["human_label"], perfect["llm_label"])
    assert acc == 1.0
    assert kappa == 1.0


def test_compute_metrics_all_positive():
    labels = make_labels_df()
    results = make_results_df()
    merged = merge_for_evaluation(results, labels)
    all_pos = merged[(merged["dimension"] == "tool_selection") & (merged["variant"] == "zero_shot")]
    acc, kappa = compute_metrics(all_pos["human_label"], all_pos["llm_label"])
    assert acc == 0.5
    assert kappa <= 0.0  # no agreement beyond chance


def test_compute_metrics_returns_table(tmp_path):
    labels_file = tmp_path / "labels.csv"
    results_file = tmp_path / "results.csv"
    make_labels_df().to_csv(labels_file, index=False)
    make_results_df().to_csv(results_file, index=False)

    from src.metrics import build_metrics_table
    table = build_metrics_table([results_file], labels_file)
    assert "dimension" in table.columns
    assert "variant" in table.columns
    assert "accuracy" in table.columns
    assert "kappa" in table.columns
    assert len(table) == 2  # tool_selection x {zero_shot, few_shot}
