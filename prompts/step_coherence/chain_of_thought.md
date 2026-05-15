You are evaluating whether an agent's next action follows logically from the current step's observation.

## Current Step
**Thought:** {thought}
**Tool:** {tool}
**Parameters:** {parameters}
**Observation:** {observation}

**Next thought:** {next_thought}
**Next action:** {next_action}

## Instructions
Think step by step before labeling:
1. What key information does the observation reveal? (errors, file contents, search results, etc.)
2. What would be the most logical next action given this information?
3. Does the agent's actual next thought correctly interpret the observation?
4. Does the next action follow from that interpretation?

After reasoning, respond with a JSON object only:
{"label": 1, "reasoning": "..."}   (1 = coherent transition)
{"label": 0, "reasoning": "..."}   (0 = incoherent transition)
