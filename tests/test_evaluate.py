import json
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from src.evaluate import render_prompt, parse_judge_response, evaluate_step, DIMENSIONS


def test_render_prompt_fills_placeholders():
    template = "Thought: {thought}\nTool: {tool}\nParams: {parameters}\nObs: {observation}"
    context = {
        "thought": "I need to list files.",
        "tool": "bash",
        "parameters": "ls -la",
        "observation": "total 8\n...",
        "next_thought": "",
        "next_action": "",
    }
    result = render_prompt(template, context)
    assert "I need to list files." in result
    assert "bash" in result
    assert "{thought}" not in result


def test_parse_judge_response_valid():
    response_text = '{"label": 1, "reasoning": "Good choice."}'
    label, reasoning = parse_judge_response(response_text)
    assert label == 1
    assert reasoning == "Good choice."


def test_parse_judge_response_with_markdown():
    response_text = '```json\n{"label": 0, "reasoning": "Bad params."}\n```'
    label, reasoning = parse_judge_response(response_text)
    assert label == 0
    assert "Bad params." in reasoning


def test_parse_judge_response_invalid_raises():
    with pytest.raises(ValueError, match="Could not parse"):
        parse_judge_response("I think this is good.")


def test_dimensions_constant():
    assert "tool_selection" in DIMENSIONS
    assert "parameter_quality" in DIMENSIONS
    assert "step_coherence" in DIMENSIONS


def test_evaluate_step_calls_api(tmp_path):
    prompt_file = tmp_path / "zero_shot.md"
    prompt_file.write_text(
        "Thought: {thought}\nTool: {tool}\nParams: {parameters}\nObs: {observation}\n"
        "Next: {next_thought} {next_action}"
    )
    step_context = {
        "step_id": "django__django-12345_0000",
        "thought": "Explore repo.",
        "tool": "bash",
        "parameters": "ls -la",
        "observation": "total 8",
        "next_thought": "Now open setup.py",
        "next_action": "str_replace_editor view /repo/setup.py",
    }
    mock_client = MagicMock()
    mock_client.messages.create.return_value.content = [
        MagicMock(text='{"label": 1, "reasoning": "Correct."}')
    ]

    from src.evaluate import evaluate_step
    result = evaluate_step(mock_client, prompt_file, step_context)

    assert result["label"] == 1
    assert result["reasoning"] == "Correct."
    assert result["step_id"] == "django__django-12345_0000"
    mock_client.messages.create.assert_called_once()
