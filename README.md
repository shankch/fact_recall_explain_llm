# Prompt Families as Access Operators

This repository contains the code, configurations, paper-relevant result summaries, and paper sources used to study factual recall in small language models through three linked lenses (model weights and large raw artifacts are not committed — see [Large Files Not in Git](#large-files-not-in-git)):

- `prompt access`: which prompt family best retrieves a fact
- `storage vs access`: where prompt-invariant fact structure emerges across layers
- `subspace interventions`: whether early prompt-invariant fact components are necessary or sufficient for later answer formation

The final manuscript is the IEEE Access submission source at [paper/ieee_access_submission.tex](paper/ieee_access_submission.tex), with aligned paper statistics in [paper/paper_stats_access.json](paper/paper_stats_access.json).

## What This README Covers

This README is focused on reproducing the final paper-stage results:

1. multi-model prompt-family study
2. storage/access/competition study
3. controlled subspace intervention study
4. aligned paper statistics
5. final IEEE Access PDF

It also documents the optional capital-prompt visualization demo and the earlier scaffold experiments that remain in the repo.

## Large Files Not in Git

To keep the repository lightweight (and to respect vendor model licenses), large
or regenerable assets are intentionally excluded via `.gitignore`. What you get
after cloning is all of the code, configs, paper sources, and the small result
summaries/figures that back the manuscript. To reproduce the full pipeline you
fetch or regenerate the rest:

- **Model weights (~7.8 GB)** — six Hugging Face checkpoints. Download with
  `python scripts/download_models.py` (see [models/README.md](models/README.md)).
- **Raw activation artifacts (~2.6 GB)** — `*.npz`, `*.jsonl`, and the large
  `neuron_scores.csv` dumps under `artifacts/results/`. Regenerate by running the
  study scripts below (see [artifacts/README.md](artifacts/README.md)).
- **Third-party / downloaded data** — `artifacts/datasets/counterfact/raw_counterfact.json`
  (re-downloaded by `scripts/prepare_counterfact.py`) and `data/MNIST/`.

First-time setup:

```bash
pip install -r requirements.txt
python scripts/download_models.py
```

## Tested Setup

The final experiments were executed on:

- GPU: `NVIDIA GeForce RTX 4050 GPU`
- VRAM: `6141 MiB` reported by `nvidia-smi`
- NVIDIA driver: `560.35.03`
- System CUDA: `12.6`
- Python: `3.11.15`
- PyTorch: `2.6.0+cu124`
- Transformers: `5.3.0`
- NumPy: `2.3.5`
- pandas: `3.0.1`
- PyYAML: `6.0.3`
- FastAPI: `0.135.1`
- Uvicorn: `0.41.0`
- cuDNN: `9.1`

The project was designed to fit on a single 6 GB laptop GPU by running models sequentially.

## Repository Layout

- [configs](configs): experiment configs
- [data](data): curated factual seeds
- [gemma_interp](gemma_interp): experiment library
- [scripts](scripts): runnable entrypoints
- [artifacts](artifacts): generated datasets, metrics, and figures
- [models](models): local Hugging Face checkpoints
- [paper](paper): manuscript sources and compiled PDFs
- [viewer](viewer): React-based activation viewer

## Required Local Model Checkpoints

The final paper compares six local checkpoints:

- `models/gemma-3-270m`
- `models/gemma-3-270m-it`
- `models/Qwen2.5-0.5B`
- `models/Qwen2.5-0.5B-Instruct`
- `models/SmolLM2-360M`
- `models/SmolLM2-360M-Instruct`

The configs assume those exact directories exist.

If you need to fetch them again, the simplest route is the Hugging Face CLI. Example:

```bash
hf download google/gemma-3-270m --local-dir models/gemma-3-270m
hf download google/gemma-3-270m-it --local-dir models/gemma-3-270m-it
hf download Qwen/Qwen2.5-0.5B --local-dir models/Qwen2.5-0.5B
hf download Qwen/Qwen2.5-0.5B-Instruct --local-dir models/Qwen2.5-0.5B-Instruct
hf download HuggingFaceTB/SmolLM2-360M --local-dir models/SmolLM2-360M
hf download HuggingFaceTB/SmolLM2-360M-Instruct --local-dir models/SmolLM2-360M-Instruct
```

Notes:

- Gemma checkpoints require Hugging Face authentication and license acceptance.
- The repo uses local checkpoint paths, not remote model IDs, during experiments.

## Environment

All commands below assume your current working directory is the repository root.

If you have already created a local conda environment for this repo, you can activate it with:

```bash
conda activate ./.conda-env
```

If you prefer not to activate it globally, prepend commands with:

```bash
conda run -p ./.conda-env ...
```

If `.conda-env` does not exist in your clone, create your own Python 3.11 environment and install the packages listed under `Tested Setup`, including a CUDA-enabled PyTorch build that matches your system.

## Quick Sanity Checks

From the project root:

```bash
python -m unittest discover -s tests -v
```

Optional GPU sanity check:

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no-cuda')"
```

## Reproducing the Final Paper Results

Run the following from the repository root in this order.

### 1. Prompt-Family Access Study

This stage builds a 5-relation benchmark from [data/factual_seed_access_revision.json](data/factual_seed_access_revision.json), evaluates 4 prompt families across 6 models, and writes holdout metrics, control summaries, and neuron ablations.

```bash
python scripts/run_prompt_invariance_study.py \
  --config configs/prompt_invariance_access_r2.yaml
```

Key config:

- [configs/prompt_invariance_access_r2.yaml](configs/prompt_invariance_access_r2.yaml)

Main outputs:

- [artifacts/results/prompt_invariance_access_r2/multimodel_family_summary.csv](artifacts/results/prompt_invariance_access_r2/multimodel_family_summary.csv)
- [artifacts/results/prompt_invariance_access_r2/multimodel_control_summary.csv](artifacts/results/prompt_invariance_access_r2/multimodel_control_summary.csv)
- [artifacts/results/prompt_invariance_access_r2/multimodel_family_selection_summary.csv](artifacts/results/prompt_invariance_access_r2/multimodel_family_selection_summary.csv)
- [artifacts/results/prompt_invariance_access_r2/multimodel_prompt_invariance_report.md](artifacts/results/prompt_invariance_access_r2/multimodel_prompt_invariance_report.md)
- [artifacts/results/prompt_invariance_access_r2/multimodel_family_heatmap.png](artifacts/results/prompt_invariance_access_r2/multimodel_family_heatmap.png)
- [artifacts/results/prompt_invariance_access_r2/multimodel_selectivity_heatmap.png](artifacts/results/prompt_invariance_access_r2/multimodel_selectivity_heatmap.png)

### 2. Storage / Access / Competition Study

This stage measures when same-fact prompts become more similar to each other than to other prompts expressing the same relation, at both the subject and pre-answer positions.

```bash
python scripts/run_storage_access_competition_study.py \
  --config configs/storage_access_competition_access_r2.yaml
```

Key config:

- [configs/storage_access_competition_access_r2.yaml](configs/storage_access_competition_access_r2.yaml)

Main outputs:

- [artifacts/results/storage_access_competition_access_r2/multimodel_summary.csv](artifacts/results/storage_access_competition_access_r2/multimodel_summary.csv)
- [artifacts/results/storage_access_competition_access_r2/multimodel_fact_invariance_summary.csv](artifacts/results/storage_access_competition_access_r2/multimodel_fact_invariance_summary.csv)
- [artifacts/results/storage_access_competition_access_r2/multimodel_control_variant_summary.csv](artifacts/results/storage_access_competition_access_r2/multimodel_control_variant_summary.csv)
- [artifacts/results/storage_access_competition_access_r2/multimodel_storage_access_report.md](artifacts/results/storage_access_competition_access_r2/multimodel_storage_access_report.md)
- [artifacts/results/storage_access_competition_access_r2/multimodel_subject_invariance_heatmap.png](artifacts/results/storage_access_competition_access_r2/multimodel_subject_invariance_heatmap.png)
- [artifacts/results/storage_access_competition_access_r2/multimodel_preanswer_invariance_heatmap.png](artifacts/results/storage_access_competition_access_r2/multimodel_preanswer_invariance_heatmap.png)

### 3. Controlled Subspace Intervention Study

This stage estimates an early prompt-invariant fact component and compares target projection / target patching against matched-control and random null directions.

```bash
python scripts/run_subspace_intervention_study.py \
  --config configs/subspace_intervention_access_r2.yaml
```

Key config:

- [configs/subspace_intervention_access_r2.yaml](configs/subspace_intervention_access_r2.yaml)

Main outputs:

- [artifacts/results/subspace_intervention_access_r2/multimodel_subspace_intervention_summary.csv](artifacts/results/subspace_intervention_access_r2/multimodel_subspace_intervention_summary.csv)
- [artifacts/results/subspace_intervention_access_r2/multimodel_subspace_interventions.csv](artifacts/results/subspace_intervention_access_r2/multimodel_subspace_interventions.csv)
- [artifacts/results/subspace_intervention_access_r2/multimodel_layer_strategy_robustness.csv](artifacts/results/subspace_intervention_access_r2/multimodel_layer_strategy_robustness.csv)
- [artifacts/results/subspace_intervention_access_r2/multimodel_subspace_intervention_report.md](artifacts/results/subspace_intervention_access_r2/multimodel_subspace_intervention_report.md)
- [artifacts/results/subspace_intervention_access_r2/multimodel_project_alignment_delta.png](artifacts/results/subspace_intervention_access_r2/multimodel_project_alignment_delta.png)
- [artifacts/results/subspace_intervention_access_r2/multimodel_patch_alignment_gain.png](artifacts/results/subspace_intervention_access_r2/multimodel_patch_alignment_gain.png)

### 4. Build Aligned Paper Statistics

This script reads the three final result directories and writes the paper-ready summary files consumed during manuscript revision.

```bash
python scripts/build_access_paper_stats.py \
  --prompt-dir artifacts/results/prompt_invariance_access_r2 \
  --storage-dir artifacts/results/storage_access_competition_access_r2 \
  --subspace-dir artifacts/results/subspace_intervention_access_r2 \
  --output-json paper/paper_stats_access.json \
  --output-md paper/paper_stats_access.md
```

Outputs:

- [paper/paper_stats_access.json](paper/paper_stats_access.json)
- [paper/paper_stats_access.md](paper/paper_stats_access.md)

### 5. Compile the IEEE Access Paper

The manuscript source is:

- [paper/ieee_access_submission.tex](paper/ieee_access_submission.tex)

Build it with:

```bash
tectonic --keep-logs --keep-intermediates paper/ieee_access_submission.tex
```

If you prefer not to activate the environment:

```bash
conda run -p ./.conda-env \
  tectonic --keep-logs --keep-intermediates paper/ieee_access_submission.tex
```

Output:

- [paper/ieee_access_submission.pdf](paper/ieee_access_submission.pdf)

## Optional: Capital Prompt Activation Demo

This is separate from the final IEEE Access result path, but it is useful for interactive inspection and the live viewer.

### Rebuild the Capital Study

Single-family run:

```bash
python scripts/run_capital_prompt_study.py \
  --model-dir models/gemma-3-270m-it \
  --benchmark-dir artifacts/datasets/capital_prompts \
  --output-dir artifacts/results/capital_study \
  --limit 100 \
  --families raw_question
```

Multi-family run:

```bash
python scripts/run_capital_prompt_study.py \
  --model-dir models/gemma-3-270m-it \
  --benchmark-dir artifacts/datasets/capital_prompts \
  --output-dir artifacts/results/capital_prompt_family_comparison \
  --limit 100 \
  --families raw_question,declarative,qa,chat_template
```

### Run the API

Port `8000` is the default. If it is already taken, use another free port such as `8010`.

```bash
python scripts/run_capital_dashboard_api.py --host 127.0.0.1 --port 8010
```

### Run the React Viewer

In another terminal:

```bash
cd viewer
npm install
VITE_API_TARGET=http://127.0.0.1:8010 npm run dev
```

Then open `http://localhost:5173/`.

Important detail:

- the viewer uses the live backend and real model activations
- it does not visualize changing weights; it visualizes prompt-dependent activations

## Legacy Scaffold Experiments

These earlier scripts remain useful if you want to reproduce the initial single-model scaffold that preceded the final paper:

### CounterFact Dataset Preparation

```bash
python scripts/prepare_counterfact.py --config configs/dataset_counterfact.yaml
```

### Passive Analysis

```bash
python scripts/run_passive_analysis.py \
  --config configs/passive_analysis.yaml \
  --dataset artifacts/datasets/counterfact/prepared_facts.jsonl
```

### Causal Interventions

```bash
python scripts/run_causal_interventions.py \
  --config configs/causal_intervention.yaml \
  --dataset artifacts/datasets/counterfact/prepared_facts.jsonl
```

### Legacy Report

```bash
python scripts/generate_report.py \
  --passive-dir artifacts/results/passive_default \
  --causal-dir artifacts/results/causal_default \
  --output-dir artifacts/results/report_default
```

## Reproducibility Notes

- All final configs use `seed: 13`.
- The final paper benchmark uses 5 relations: `capital`, `official_language`, `currency`, `headquarters`, `birth_place`.
- The final paper configs use `limit_per_relation: 18`, yielding a curated 90-fact benchmark.
- The prompt families are `raw_question`, `declarative`, `qa`, and `chat_template`.
- The pipeline runs models sequentially, so you do not need all six models resident in VRAM at the same time.
- Result directories are deterministic by config path and output location; rerunning a script updates the corresponding artifact directory.

## Suggested Full Reproduction Order

If you want the shortest end-to-end path from a clean checkout to the final PDF:

```bash
conda activate ./.conda-env
python -m unittest discover -s tests -v
python scripts/run_prompt_invariance_study.py --config configs/prompt_invariance_access_r2.yaml
python scripts/run_storage_access_competition_study.py --config configs/storage_access_competition_access_r2.yaml
python scripts/run_subspace_intervention_study.py --config configs/subspace_intervention_access_r2.yaml
python scripts/build_access_paper_stats.py --prompt-dir artifacts/results/prompt_invariance_access_r2 --storage-dir artifacts/results/storage_access_competition_access_r2 --subspace-dir artifacts/results/subspace_intervention_access_r2 --output-json paper/paper_stats_access.json --output-md paper/paper_stats_access.md
tectonic --keep-logs --keep-intermediates paper/ieee_access_submission.tex
```

## Final Outputs to Inspect

For the paper:

- [paper/ieee_access_submission.pdf](paper/ieee_access_submission.pdf)
- [paper/paper_stats_access.md](paper/paper_stats_access.md)

For the experiments:

- [artifacts/results/prompt_invariance_access_r2](artifacts/results/prompt_invariance_access_r2)
- [artifacts/results/storage_access_competition_access_r2](artifacts/results/storage_access_competition_access_r2)
- [artifacts/results/subspace_intervention_access_r2](artifacts/results/subspace_intervention_access_r2)

If you want to capture exact runtime and stdout for archival purposes, run each command with `tee`, for example:

```bash
python scripts/run_prompt_invariance_study.py --config configs/prompt_invariance_access_r2.yaml | tee prompt_invariance_access_r2.log
```
