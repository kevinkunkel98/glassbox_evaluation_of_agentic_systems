You are evaluating whether an agent's next action follows logically from the current step's observation.

## Examples

**Example 1 (coherent)**
Observation: "Error: ImportError: cannot import name 'validate' from 'utils'"
Next thought: I see the import is failing. Let me check what's actually in utils.py.
Next action: str_replace_editor view /repo/utils.py
Label: {"label": 1, "reasoning": "The agent correctly identifies the import error and investigates the source file."}

**Example 2 (incoherent)**
Observation: "File /repo/validators.py, line 42\n    if user.is_valid():\nAttributeError: 'NoneType' object has no attribute 'is_valid'"
Next thought: Great, the tests are passing now. Let me submit the patch.
Next action: submit
Label: {"label": 0, "reasoning": "The observation shows an error, but the agent incorrectly concludes the tests are passing. The transition ignores the observation."}

## Current Step
**Thought:** {thought}
**Tool:** {tool}
**Parameters:** {parameters}
**Observation:** {observation}

**Next thought:** {next_thought}
**Next action:** {next_action}

Respond with a JSON object only:
{"label": 1, "reasoning": "..."}
{"label": 0, "reasoning": "..."}
