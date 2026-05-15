# Annotation Rubric

Label each step across three binary dimensions. For each dimension:
- **1** = appropriate / good
- **0** = inappropriate / poor

## Dimension 1: Tool Selection

**Question:** Given the agent's current goal (expressed in `thought`) and the available tools, was the chosen tool the most appropriate one?

**Label 1 (good) if:**
- The tool directly serves the stated goal
- No obviously better tool exists for this purpose

**Label 0 (poor) if:**
- A different tool would clearly have been more effective
- The tool choice is a mismatch with the stated goal (e.g., using `bash` to read a file when `str_replace_editor view` is available)

**Ignore:** Whether the parameters were correct or the outcome was successful.

---

## Dimension 2: Parameter Quality

**Question:** Were the parameters passed to the chosen tool sensible and well-formed?

**Label 1 (good) if:**
- Parameters match the tool's expected format
- The target (file path, command, search term) is specific and appropriate

**Label 0 (poor) if:**
- Parameters are malformed, empty when they shouldn't be, or clearly wrong
- The command/path/argument has an obvious mistake

**Ignore:** Whether the tool itself was a good choice.

---

## Dimension 3: Step Coherence

**Question:** Given the observation from this step, does the *next* step's thought/action follow logically?

**Label 1 (coherent) if:**
- The next step's thought acknowledges or builds on the current observation
- The transition makes sense in context

**Label 0 (incoherent) if:**
- The next step ignores a key finding from the observation
- The next step repeats what was just done without cause
- The agent clearly misread or hallucinated from the observation

**Note:** For the final step in a trajectory, annotate step coherence as 1 if the submission/exit follows logically from the last observation.

---

## Annotation Process

1. Open `data/parsed_traces/` and load a `.jsonl` file
2. For each line (one step), fill in the three labels in `data/annotations/labels.csv`
3. If a step is ambiguous, add a note in the `notes` column and label your best guess
4. Aim for 50–100 steps across 3–5 diverse instances for a useful ground-truth set
