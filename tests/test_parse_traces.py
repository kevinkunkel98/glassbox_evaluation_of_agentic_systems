import json
import tempfile
from pathlib import Path
from src.parse_traces import parse_action, parse_traj_file, parse_all


def test_parse_action_bash():
    tool, params = parse_action("bash\nls -la /repo")
    assert tool == "bash"
    assert params["args"] == "ls -la /repo"


def test_parse_action_str_replace_editor():
    tool, params = parse_action("str_replace_editor\nview\n/repo/setup.py")
    assert tool == "str_replace_editor"
    assert "view" in params["args"]
    assert "/repo/setup.py" in params["args"]


def test_parse_action_single_line():
    tool, params = parse_action("submit")
    assert tool == "submit"
    assert params["args"] == ""


def test_parse_traj_file(tmp_path):
    fixture = Path("tests/fixtures/sample.traj")
    steps = parse_traj_file(fixture)
    assert len(steps) == 2

    s0 = steps[0]
    assert s0.instance_id == "django__django-12345"
    assert s0.step_idx == 0
    assert s0.step_id == "django__django-12345_0000"
    assert s0.tool == "bash"
    assert "ls -la /repo" in s0.parameters["args"]
    assert "total 20" in s0.observation
    assert "exploring" in s0.thought

    s1 = steps[1]
    assert s1.step_idx == 1
    assert s1.step_id == "django__django-12345_0001"
    assert s1.tool == "str_replace_editor"


def test_parse_all_writes_jsonl(tmp_path):
    input_dir = tmp_path / "raw"
    output_dir = tmp_path / "parsed"
    input_dir.mkdir()
    output_dir.mkdir()

    fixture = Path("tests/fixtures/sample.traj")
    (input_dir / "sample.traj").write_text(fixture.read_text())

    parse_all(input_dir, output_dir)

    output_file = output_dir / "sample.jsonl"
    assert output_file.exists()
    lines = output_file.read_text().strip().split("\n")
    assert len(lines) == 2
    first = json.loads(lines[0])
    assert first["step_id"] == "django__django-12345_0000"
