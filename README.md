# glass-box-eval

Automated component-level evaluation of software engineering agents using LLM-as-Judge.

## Overview

Current agent evaluation focuses on end-to-end task success, which hides where errors originate. This project evaluates individual agent steps using LLM-based judges, comparing automated judgements against human-annotated ground truth across three dimensions:

- **Tool Selection** — did the agent choose the right tool?
- **Parameter Quality** — were the parameters sensible?
- **Step Coherence** — was the next step logical given the observation?

## Repository Structure

```
glass-box-eval/
├── data/
│   ├── raw_traces/          # SWE-agent JSON traces
│   ├── parsed_traces/       # parsed step objects
│   └── annotations/         # manual ground truth labels (labels.csv)
├── src/
│   ├── parse_traces.py      # trace → step objects
│   ├── evaluate.py          # run LLM judge on steps
│   └── metrics.py           # accuracy, cohen's kappa
├── prompts/
│   ├── tool_selection.md
│   ├── parameter_quality.md
│   └── step_coherence.md
├── notebooks/
│   └── analysis.ipynb       # evaluation & plots
├── docs/
│   └── rubric.md            # annotation rubric
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/your-username/glass-box-eval
cd glass-box-eval
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...
```

## Data

Traces are sourced from [SWE-bench](https://github.com/SWE-bench/SWE-bench).
Download and place them in `data/raw_traces/` before running.

Ground truth labels are in `data/annotations/labels.csv`.
The annotation rubric is documented in `docs/rubric.md`.

## Reproduce Results

```bash
# 1. parse raw traces into step objects
python src/parse_traces.py --input data/raw_traces/ --output data/parsed_traces/

# 2. run all prompt variants against all steps
python src/evaluate.py --prompts prompts/ --data data/parsed_traces/ --output results/

# 3. compute metrics vs ground truth
python src/metrics.py --results results/ --labels data/annotations/labels.csv

# 4. open analysis notebook
jupyter notebook notebooks/analysis.ipynb
```

## Requirements

```
anthropic>=0.20.0
pandas>=2.0.0
scikit-learn>=1.3.0
jupyter>=1.0.0
matplotlib>=3.7.0
```

## Citation

Seminar: Prompting, Agents, and RAG in Software Engineering — Universität Leipzig 2026
