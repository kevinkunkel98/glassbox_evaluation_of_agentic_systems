You are evaluating a software engineering agent's step. Your task is to judge whether the parameters passed to the tool were sensible.

## Agent Step
**Thought:** {thought}
**Tool used:** {tool}
**Parameters:** {parameters}
**Observation:** {observation}

## Instructions
Think step by step before labeling:
1. What did the agent intend to do with `{tool}`, based on its thought?
2. Are the parameters syntactically valid for `{tool}`?
3. Do the parameters match the stated goal (correct file path, search term, command)?
4. Would these parameters have been likely to succeed at the intended action?

After reasoning, respond with a JSON object only:
{"label": 1, "reasoning": "..."}   (1 = good parameters)
{"label": 0, "reasoning": "..."}   (0 = poor/malformed parameters)
