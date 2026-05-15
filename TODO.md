# Next TODOs

## 1. Get real trajectory data

- [x] Download SWE-agent trajectory files — 4 demonstration trajectories of `marshmallow-code/marshmallow-1867` from the SWE-agent GitHub repo (default, cursors, function_calling, xml prompt variants), placed in `data/raw_traces/`
- [x] Run the parser: 48 steps across 4 files parsed into `data/parsed_traces/`
- [x] Spot-checked output — `tool`, `thought`, `observation` fields populated correctly
- [x] Note: trajectories use the old SWE-agent bash-style ACI (`open`, `create`, `edit`, `ls`, `python`, etc.) — prompt templates updated to match this tool set

**Limitation:** all 4 trajectories solve the same instance with different prompt configs. For a stronger study, source trajectories from ≥5 distinct SWE-bench instances (e.g., by running SWE-agent, or downloading from a leaderboard submission that publishes trajectories).

## 2. Annotate steps (with inter-rater partner)

Export a shared annotation sheet first (already done — 48 steps, all available):
```bash
python -m src.export_for_annotation \
  --data data/parsed_traces/ \
  --output data/annotations/steps_to_annotate.csv \
  --sample 48 --seed 42
```

- [x] `data/annotations/steps_to_annotate.csv` generated (48 steps)
- [ ] Share `steps_to_annotate.csv` with your partner (Google Sheets works well)
- [ ] Both of you read `docs/rubric.md` independently before starting
- [ ] Each annotate the same 80 steps independently — **do not share labels until both are done**
- [ ] Save your labels as `data/annotations/labels_kevin.csv` and ask partner to send theirs as `labels_<partner>.csv`
- [ ] For step coherence: the label goes on the *current* row but judges the *next* step's transition (the `next_thought` / `next_tool` columns in the sheet are there for this)
- [ ] Flag ambiguous cases in `notes` rather than skipping

Compute inter-rater kappa once both are done:
```bash
python src/interrater.py \
  --a data/annotations/labels_kevin.csv \
  --b data/annotations/labels_<partner>.csv
```

This gives per-dimension kappa and overall — report these in the paper as the human upper bound.

## 3. Run the evaluation

```bash
export ANTHROPIC_API_KEY=sk-...
python src/evaluate.py \
  --prompts prompts/ \
  --data data/parsed_traces/ \
  --output results/
```

- [ ] Check `results/*.csv` for any `label == -1` rows (API errors) and re-run or investigate
- [ ] Budget: 9 judge calls per step (3 dimensions × 3 variants) — estimate cost before running on all steps

## 4. Compute metrics and generate figures

```bash
python src/metrics.py \
  --results results/*.csv \
  --labels data/annotations/labels.csv \
  --output results/metrics.csv
```

- [ ] Open `notebooks/analysis.ipynb` and run all cells
- [ ] Save `results/metrics_heatmap.png` and `results/metrics_bar.png` — these go into the paper

## 5. Fill in the paper

- [ ] Replace `[TODO]` markers in `= Conclusion` with real findings
- [ ] Write `= Results` subsections with actual numbers from the metrics table
- [ ] Write `= Discussion` subsections based on where kappa is high vs. low
- [ ] Fill `@tab-dataset` with real instance / step / annotation counts
- [ ] Fill `@tab-results` with real accuracy and kappa values
- [ ] Replace the placeholder `image.png` for `@fig-pipeline` with an actual pipeline diagram
- [ ] Replace the placeholder `image.png` for `@fig-heatmap` with `results/metrics_heatmap.png`

## 6. Housekeeping

- [x] Add a `.gitignore` entry for `data/raw_traces/` (trajectory files can be large) and `results/` (generated outputs)
- [x] Remove the Hinton and Vaswani placeholder entries from `bibliography.bib` — they are unused
- [ ] Consider a second annotator on ~20 steps to get an inter-annotator kappa as a human upper bound
