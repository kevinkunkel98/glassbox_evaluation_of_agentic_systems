from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from sklearn.metrics import accuracy_score, cohen_kappa_score


def load_labels(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df[["step_id", "tool_selection", "parameter_quality", "step_coherence"]]


def load_results(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def merge_for_evaluation(results: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    melted = labels.melt(
        id_vars="step_id",
        value_vars=["tool_selection", "parameter_quality", "step_coherence"],
        var_name="dimension",
        value_name="human_label",
    )
    merged = results.merge(melted, on=["step_id", "dimension"], how="inner")
    merged = merged[merged["label"] != -1]  # drop error rows
    merged = merged.rename(columns={"label": "llm_label"})
    return merged


def compute_metrics(
    human: pd.Series, llm: pd.Series
) -> tuple[float, float]:
    acc = accuracy_score(human, llm)
    kappa = cohen_kappa_score(human, llm) if len(human.unique()) > 1 or len(llm.unique()) > 1 else 0.0
    return round(acc, 4), round(kappa, 4)


def build_metrics_table(result_files: list[Path], labels_file: Path) -> pd.DataFrame:
    labels = load_labels(labels_file)
    all_results = pd.concat([load_results(f) for f in result_files], ignore_index=True)
    merged = merge_for_evaluation(all_results, labels)

    rows = []
    for (dim, variant), group in merged.groupby(["dimension", "variant"]):
        acc, kappa = compute_metrics(group["human_label"], group["llm_label"])
        rows.append({
            "dimension": dim,
            "variant": variant,
            "n": len(group),
            "accuracy": acc,
            "kappa": kappa,
        })
    return pd.DataFrame(rows).sort_values(["dimension", "variant"]).reset_index(drop=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True, nargs="+", type=Path)
    parser.add_argument("--labels", required=True, type=Path)
    parser.add_argument("--output", default="metrics.csv", type=Path)
    args = parser.parse_args()
    table = build_metrics_table(args.results, args.labels)
    print(table.to_string(index=False))
    table.to_csv(args.output, index=False)
    print(f"\nSaved to {args.output}")
