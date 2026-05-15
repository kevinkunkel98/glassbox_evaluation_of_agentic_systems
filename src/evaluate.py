from __future__ import annotations
import argparse
import csv
import json
import re
import time
from pathlib import Path
import anthropic
from src.step import Step

DIMENSIONS = ["tool_selection", "parameter_quality", "step_coherence"]
VARIANTS = ["zero_shot", "few_shot", "chain_of_thought"]
MODEL = "claude-haiku-4-5-20251001"


def render_prompt(template: str, context: dict) -> str:
    result = template
    for key, value in context.items():
        result = result.replace(f"{{{key}}}", str(value))
    return result


def parse_judge_response(text: str) -> tuple[int, str]:
    cleaned = re.sub(r"```(?:json)?\n?", "", text).strip().rstrip("`").strip()
    try:
        data = json.loads(cleaned)
        return int(data["label"]), str(data["reasoning"])
    except (json.JSONDecodeError, KeyError):
        pass
    match = re.search(r'"label"\s*:\s*([01])', text)
    if match:
        label = int(match.group(1))
        reason_match = re.search(r'"reasoning"\s*:\s*"([^"]+)"', text)
        reasoning = reason_match.group(1) if reason_match else ""
        return label, reasoning
    raise ValueError(f"Could not parse judge response: {text[:200]}")


def build_context(step: Step, next_step: Step | None) -> dict:
    params_str = json.dumps(step.parameters.get("args", step.parameters), ensure_ascii=False)
    next_thought = next_step.thought if next_step else ""
    next_action = next_step.raw_action.split("\n")[0] if next_step else "(end of trajectory)"
    return {
        "thought": step.thought,
        "tool": step.tool,
        "parameters": params_str,
        "observation": step.observation,
        "next_thought": next_thought,
        "next_action": next_action,
    }


def evaluate_step(client: anthropic.Anthropic, prompt_file: Path, context: dict) -> dict:
    template = prompt_file.read_text()
    prompt = render_prompt(template, context)
    response = client.messages.create(
        model=MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    label, reasoning = parse_judge_response(response.content[0].text)
    return {
        "step_id": context["step_id"],
        "label": label,
        "reasoning": reasoning,
    }


def load_steps(jsonl_path: Path) -> list[Step]:
    steps = []
    for line in jsonl_path.read_text().strip().split("\n"):
        if line.strip():
            steps.append(Step.from_dict(json.loads(line)))
    return steps


def run_evaluation(
    steps_dir: Path,
    prompts_dir: Path,
    output_dir: Path,
    sleep_between: float = 0.5,
) -> None:
    client = anthropic.Anthropic()
    output_dir.mkdir(parents=True, exist_ok=True)
    fieldnames = ["step_id", "dimension", "variant", "label", "reasoning"]

    for jsonl_file in sorted(steps_dir.glob("*.jsonl")):
        steps = load_steps(jsonl_file)
        out_path = output_dir / jsonl_file.with_suffix(".csv").name
        with out_path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for i, step in enumerate(steps):
                next_step = steps[i + 1] if i + 1 < len(steps) else None
                context = build_context(step, next_step)
                context["step_id"] = step.step_id
                for dim in DIMENSIONS:
                    for variant in VARIANTS:
                        prompt_file = prompts_dir / dim / f"{variant}.md"
                        if not prompt_file.exists():
                            continue
                        try:
                            result = evaluate_step(client, prompt_file, context)
                            writer.writerow({
                                "step_id": step.step_id,
                                "dimension": dim,
                                "variant": variant,
                                "label": result["label"],
                                "reasoning": result["reasoning"],
                            })
                        except Exception as e:
                            print(f"Error on {step.step_id} / {dim} / {variant}: {e}")
                            writer.writerow({
                                "step_id": step.step_id,
                                "dimension": dim,
                                "variant": variant,
                                "label": -1,
                                "reasoning": f"ERROR: {e}",
                            })
                        time.sleep(sleep_between)
        print(f"Results written to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", required=True, type=Path)
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    run_evaluation(args.data, args.prompts, args.output)
