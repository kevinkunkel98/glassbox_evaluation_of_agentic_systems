You are evaluating a software engineering agent's step. Your task is to judge whether the agent chose the right tool.

## Available tools
- bash: execute shell commands
- str_replace_editor: view/edit files (subcommands: view, create, str_replace, insert)
- find_file: find a file by name
- search_file: search for a string within a specific file
- search_dir: search for a string across a directory
- submit: submit the final patch
- exit_forfeit: give up on the task

## Agent Step
**Thought:** {thought}
**Tool used:** {tool}
**Parameters:** {parameters}
**Observation:** {observation}

## Instructions
Think step by step before labeling:
1. What goal was the agent trying to achieve, based on its thought?
2. Which tool(s) from the list above would be most appropriate for that goal?
3. Is `{tool}` among the best choices, or is there a clearly better option?

After reasoning, respond with a JSON object only:
{"label": 1, "reasoning": "..."}   (1 = good tool choice)
{"label": 0, "reasoning": "..."}   (0 = poor tool choice)
