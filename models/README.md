# Local model checkpoints (not committed)

The experiments load six local Hugging Face checkpoints from this directory.
They are **not** stored in git: together they are ~7.8 GB, and some vendor
licenses (notably Google Gemma) restrict redistribution.

Download all six with the helper script:

```bash
python scripts/download_models.py
```

…or fetch them individually with the Hugging Face CLI:

| Local directory                 | Hugging Face repo                     |
| ------------------------------- | ------------------------------------- |
| `models/gemma-3-270m`           | `google/gemma-3-270m`                 |
| `models/gemma-3-270m-it`        | `google/gemma-3-270m-it`              |
| `models/Qwen2.5-0.5B`           | `Qwen/Qwen2.5-0.5B`                   |
| `models/Qwen2.5-0.5B-Instruct`  | `Qwen/Qwen2.5-0.5B-Instruct`          |
| `models/SmolLM2-360M`           | `HuggingFaceTB/SmolLM2-360M`          |
| `models/SmolLM2-360M-Instruct`  | `HuggingFaceTB/SmolLM2-360M-Instruct` |

```bash
hf download google/gemma-3-270m --local-dir models/gemma-3-270m
hf download google/gemma-3-270m-it --local-dir models/gemma-3-270m-it
hf download Qwen/Qwen2.5-0.5B --local-dir models/Qwen2.5-0.5B
hf download Qwen/Qwen2.5-0.5B-Instruct --local-dir models/Qwen2.5-0.5B-Instruct
hf download HuggingFaceTB/SmolLM2-360M --local-dir models/SmolLM2-360M
hf download HuggingFaceTB/SmolLM2-360M-Instruct --local-dir models/SmolLM2-360M-Instruct
```

Gemma checkpoints require `huggingface-cli login` and acceptance of the Gemma
license on the model page. The configs reference these exact local directory
names, not remote model IDs.
