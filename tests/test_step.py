import json
from src.step import Step


def test_step_roundtrip():
    step = Step(
        step_id="django__django-12345_0000",
        instance_id="django__django-12345",
        step_idx=0,
        thought="I should look at the error first.",
        tool="bash",
        parameters={"args": "cat traceback.txt"},
        raw_action="bash\ncat traceback.txt",
        observation="Traceback (most recent call last):\n  ...",
    )
    data = step.to_dict()
    restored = Step.from_dict(data)
    assert restored == step


def test_step_to_json_line():
    step = Step(
        step_id="astropy__astropy-1_0001",
        instance_id="astropy__astropy-1",
        step_idx=1,
        thought="Let me check the imports.",
        tool="str_replace_editor",
        parameters={"args": "view\n/repo/astropy/__init__.py"},
        raw_action="str_replace_editor\nview\n/repo/astropy/__init__.py",
        observation="Here's the content...",
    )
    line = step.to_json_line()
    assert json.loads(line)["step_id"] == "astropy__astropy-1_0001"
    assert "\n" not in line.rstrip("\n")
