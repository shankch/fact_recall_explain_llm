# Artifacts

Experiment inputs (`datasets/`) and outputs (`results/`).

## Committed (small, paper-relevant)

- `datasets/**` — generated benchmark prompt sets and country-fact snapshots
- `results/**` — summary tables (`*summary*.csv`, `*_metrics.csv`, etc.),
  figures (`*.png`), reports (`*.md`), and `summary.json` for every study

## Not committed (large, regenerable)

These are excluded via `.gitignore` to keep the repo lightweight. Rebuild them
by running the `scripts/` entrypoints described in the top-level
[README](../README.md):

- `results/**/*.npz` — raw activation tensors (~700 MB)
- `results/**/*.jsonl` — per-record activation dumps (~1.6 GB)
- `results/**/neuron_scores.csv` — per-neuron score dumps (~280 MB)
- `datasets/counterfact/raw_counterfact.json` — third-party CounterFact dump,
  re-downloaded by `scripts/prepare_counterfact.py`

Result directories are deterministic by config path and output location, so
re-running a study regenerates the exact artifact directory it owns.
