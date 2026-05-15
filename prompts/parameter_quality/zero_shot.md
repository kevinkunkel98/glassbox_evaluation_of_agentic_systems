You are evaluating a software engineering agent's step. Your task is to judge whether the parameters passed to the tool were sensible.

## Agent Step
**Thought:** {thought}
**Tool used:** {tool}
**Parameters:** {parameters}
**Observation:** {observation}

## Task
Were the parameters passed to `{tool}` well-formed and appropriate for achieving the goal in the thought?

Respond with a JSON object only:
{"label": 1, "reasoning": "..."}   (1 = good parameters)
{"label": 0, "reasoning": "..."}   (0 = poor/malformed parameters)
