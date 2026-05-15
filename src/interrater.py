"""
Compute inter-rater agreement (Cohen's kappa) between two annotators.

Usage:
    python src/interrater.py \
        --a data/annotations/labels_kevin.csv \
        --b data/annotations/labels_partner.csv

Both files must have columns: step_id, tool_selection, parameter_quality, step_coherence
(same schema as data/annotations/labels.csv). Only step_ids present in both files are used.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from src.metrics import compute_metrics

DIMENSIONS = ["tool_selection", "parameter_quality", "step_coherence"]


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in ["step_id"] + DIMENSIONS:
        if col not in df.columns:
            raise ValueError(f"{path.name} is missing column '{col}'")
    return df[["step_id"] + DIMENSIONS].dropna(subset=DIMENSIONS)


def run(path_a: Path, path_b: Path) -> None:
    a = load(path_a).rename(columns={d: f"{d}_a" for d in DIMENSIONS})
    b = load(path_b).rename(columns={d: f"{d}_b" for d in DIMENSIONS})

    merged = a.merge(b, on="step_id", how="inner")
    n_total_a = len(load(path_a))
    n_total_b = len(load(path_b))
    n_shared = len(merged)

    print(f"\nAnnotator A ({path_a.name}): {n_total_a} steps")
    print(f"Annotator B ({path_b.name}): {n_total_b} steps")
    print(f"Shared (used for kappa):      {n_shared} steps\n")

    if n_shared == 0:
        print("No overlapping step_ids found. Check that both files annotate the same steps.")
        return

    rows = []
    for dim in DIMENSIONS:
        col_a = merged[f"{dim}_a"].astype(int)
        col_b = merged[f"{dim}_b"].astype(int)
        acc, kappa = compute_metrics(col_a, col_b)
        agree = int((col_a == col_b).sum())
        rows.append({
            "dimension": dim,
            "agreed": agree,
            "disagreed": n_shared - agree,
            "accuracy": acc,
            "kappa": kappa,
        })

    result = pd.DataFrame(rows)
    print(result.to_string(index=False))

    overall_a = merged[[f"{d}_a" for d in DIMENSIONS]].values.flatten().astype(int)
    overall_b = merged[[f"{d}_b" for d in DIMENSIONS]].values.flatten().astype(int)
    import pandas as _pd
    overall_acc, overall_kappa = compute_metrics(
        _pd.Series(overall_a), _pd.Series(overall_b)
    )
    print(f"\nOverall kappa across all dimensions: {overall_kappa:.4f}")
    print(f"Overall accuracy:                    {overall_acc:.4f}")

    print("\nInterpretation of kappa:")
    print("  < 0.20  slight    |  0.20–0.40  fair   |  0.40–0.60  moderate")
    print("  0.60–0.80  substantial  |  >= 0.80  near-perfect")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", required=True, type=Path, help="Annotator A labels CSV")
    parser.add_argument("--b", required=True, type=Path, help="Annotator B labels CSV")
    args = parser.parse_args()
    run(args.a, args.b)
