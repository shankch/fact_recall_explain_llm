---
pretty_name: Fact Recall in Small LMs — Raw Experiment Artifacts
license: mit
tags:
  - interpretability
  - mechanistic-interpretability
  - factual-recall
  - small-language-models
  - reproducibility
size_categories:
  - 1B<n<10B
---

# Fact Recall in Small LMs — Raw Experiment Artifacts

Companion data for the study **"Prompt Families as Access Operators"** on factual
recall in small language models (Gemma 3 270M, Qwen2.5 0.5B, SmolLM2 360M;
base + instruct).

These are the **large, regenerable raw artifacts** that are intentionally kept
out of the code repository to keep it lightweight:

- `results/**/*.npz` — raw activation tensors
- `results/**/*.jsonl` — per-record activation/profile dumps
- `results/**/neuron_scores.csv` — per-neuron score dumps

The directory layout mirrors the `artifacts/` directory of the code repository.

## Code & paper

All code, configs, paper sources, and the small result summaries/figures live in
the GitHub repository:

- **Code:** https://github.com/shankch/fact_recall_explain_llm

## Usage

From a clone of the code repository:

```bash
pip install huggingface_hub
python scripts/download_artifacts_hf.py --repo-id sch1/fact_recall_explain_llm
```

This restores the files under `artifacts/results/`. Alternatively, every artifact
here is deterministically regenerable by running the study scripts described in
the repository README (all final configs use `seed: 13`).

## Provenance

These artifacts are activation statistics and derived metrics computed from
publicly available open-weight checkpoints. Model weights themselves are **not**
included here; download them from their original Hugging Face sources (see the
code repository's `models/README.md`).
