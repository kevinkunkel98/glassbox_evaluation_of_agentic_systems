"""
Export parsed steps to a human-readable CSV for annotation in Google Sheets / Excel.

Usage:
    python src/export_for_annotation.py \
        --data data/parsed_traces/ \
        --output data/annotations/steps_to_annotate.csv \
        --sample 80          # optional: random sample of N steps
        --seed 42            # for reproducibility

The output CSV has one row per step with full content (thought, tool, parameters,
observation, next_thought) plus empty label columns ready to be filled in.
Both annotators should work from the same CSV file independently.
"""
from __future__ import annotations
import argparse
import csv
import json
import random
from pathlib import Path
from src.step import Step

TRUNCATE_CHARS = 400

FIELDNAMES = [
    "step_id",
    "instance_id",
    "step_idx",
    "tool",
    "thought",
    "parameters",
    "observation",
    "next_thought",
    "next_tool",
    # label columns — fill these in
    "tool_selection",
    "parameter_quality",
    "step_coherence",
    "notes",
]


def truncate(text: str, n: int = TRUNCATE_CHARS) -> str:
    text = text.replace("\n", " ").strip()
    return text if len(text) <= n else text[:n] + "…"


def load_steps_from_dir(data_dir: Path) -> list[Step]:
    steps = []
    for jsonl_file in sorted(data_dir.glob("*.jsonl")):
        for line in jsonl_file.read_text().strip().split("\n"):
            if line.strip():
                steps.append(Step.from_dict(json.loads(line)))
    return steps


def build_rows(steps: list[Step]) -> list[dict]:
    rows = []
    for i, step in enumerate(steps):
        next_step = steps[i + 1] if i + 1 < len(steps) and steps[i + 1].instance_id == step.instance_id else None
        rows.append({
            "step_id": step.step_id,
            "instance_id": step.instance_id,
            "step_idx": step.step_idx,
            "tool": step.tool,
            "thought": truncate(step.thought),
            "parameters": truncate(step.parameters.get("args", str(step.parameters))),
            "observation": truncate(step.observation),
            "next_thought": truncate(next_step.thought) if next_step else "(end of trajectory)",
            "next_tool": next_step.tool if next_step else "(end)",
            "tool_selection": "",
            "parameter_quality": "",
            "step_coherence": "",
            "notes": "",
        })
    return rows


def export(data_dir: Path, output_path: Path, sample: int | None, seed: int) -> None:
    steps = load_steps_from_dir(data_dir)
    if not steps:
        raise ValueError(f"No steps found in {data_dir} — run parse_traces.py first.")

    if sample is not None:
        random.seed(seed)
        steps = random.sample(steps, min(sample, len(steps)))
        steps.sort(key=lambda s: (s.instance_id, s.step_idx))

    rows = build_rows(steps)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported {len(rows)} steps → {output_path}")
    print("Share this file with your co-annotator.")
    print("Both of you fill in tool_selection, parameter_quality, step_coherence (0 or 1) independently.")
    print("Save as: labels_kevin.csv and labels_<partner>.csv")
    print("Then run: python src/interrater.py --a data/annotations/labels_kevin.csv --b data/annotations/labels_<partner>.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export steps for human annotation.")
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--sample", type=int, default=None)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    export(args.data, args.output, args.sample, args.seed)
