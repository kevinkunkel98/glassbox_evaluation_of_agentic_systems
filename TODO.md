# Next TODOs

## 1. Get real trajectory data

The code pipeline is ready but has only run on a two-step fixture. You need actual SWE-agent `.traj` files.

- [ ] Download SWE-agent trajectory files — either from the SWE-bench leaderboard submissions or by running SWE-agent yourself on a small subset of instances
- [ ] Place `.traj` files in `data/raw_traces/`
- [ ] Run the parser and spot-check the output for format surprises:
  ```bash
  python src/parse_traces.py --input data/raw_traces/ --output data/parsed_traces/
  head -n 1 data/parsed_traces/<first>.jsonl | python -m json.tool
  ```
- [ ] The `parse_action` logic may need tuning for the real action format — verify `tool` and `parameters` fields look right across a few steps

## 2. Annotate steps (with inter-rater partner)

Export a shared annotation sheet first:
```bash
python src/export_for_annotation.py \
  --data data/parsed_traces/ \
  --output data/annotations/steps_to_annotate.csv \
  --sample 80 --seed 42
```

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

- [ ] Add a `.gitignore` entry for `data/raw_traces/` (trajectory files can be large) and `results/` (generated outputs)
- [ ] Remove the Hinton and Vaswani placeholder entries from `bibliography.bib` — they are unused
- [ ] Consider a second annotator on ~20 steps to get an inter-annotator kappa as a human upper bound
