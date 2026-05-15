You are evaluating a software engineering agent's step. Your task is to judge whether the agent's next action follows logically from the current observation.

## Current Step
**Thought:** {thought}
**Tool used:** {tool}
**Parameters:** {parameters}
**Observation:** {observation}

## Task
Does the agent's next action (shown in the next_thought and next_action fields below) follow logically from the observation above?

**Next thought:** {next_thought}
**Next action:** {next_action}

Respond with a JSON object only:
{"label": 1, "reasoning": "..."}   (1 = coherent transition)
{"label": 0, "reasoning": "..."}   (0 = incoherent transition)
