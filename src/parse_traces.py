from __future__ import annotations
import argparse
import json
from pathlib import Path
from src.step import Step


def parse_action(action: str) -> tuple[str, dict]:
    lines = action.strip().split("\n")
    tool = lines[0].strip().split()[0] if lines and lines[0].strip() else "unknown"
    args = "\n".join(lines[1:]) if len(lines) > 1 else ""
    return tool, {"args": args}


def parse_traj_file(path: Path) -> list[Step]:
    data = json.loads(path.read_text())
    instance_id = data.get("info", {}).get("instance_id", path.stem)
    steps = []
    for idx, entry in enumerate(data.get("trajectory", [])):
        action = entry.get("action", "")
        tool, parameters = parse_action(action)
        thought = entry.get("thought", "")
        if not thought:
            response = entry.get("response", "")
            thought = response.split("```")[0].strip()
        step = Step(
            step_id=f"{instance_id}_{idx:04d}",
            instance_id=instance_id,
            step_idx=idx,
            thought=thought,
            tool=tool,
            parameters=parameters,
            raw_action=action,
            observation=entry.get("observation", ""),
        )
        steps.append(step)
    return steps


def parse_all(input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for traj_file in sorted(input_dir.glob("*.traj")):
        steps = parse_traj_file(traj_file)
        out = output_dir / traj_file.with_suffix(".jsonl").name
        out.write_text("".join(s.to_json_line() for s in steps))
        print(f"Parsed {traj_file.name}: {len(steps)} steps → {out.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    parse_all(args.input, args.output)
