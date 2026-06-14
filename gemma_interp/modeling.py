from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .utils import set_seed


@dataclass
class ModelBundle:
    model: Any
    tokenizer: Any
    device: torch.device
    dtype: torch.dtype


def choose_dtype(requested: str) -> torch.dtype:
    if requested == "float32":
        return torch.float32
    if requested == "float16":
        return torch.float16
    if requested == "bfloat16":
        return torch.bfloat16
    if torch.cuda.is_available() and torch.cuda.is_bf16_supported():
        return torch.bfloat16
    if torch.cuda.is_available():
        return torch.float16
    return torch.float32


def load_model_bundle(
    model_dir: str | Path,
    seed: int = 13,
    require_cuda: bool = False,
    dtype: str = "auto",
) -> ModelBundle:
    set_seed(seed)
    cuda_available = torch.cuda.is_available()
    if require_cuda and not cuda_available:
        raise RuntimeError("CUDA is required but not available.")

    device = torch.device("cuda" if cuda_available else "cpu")
    selected_dtype = choose_dtype(dtype)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    if tokenizer.pad_token_id is None and tokenizer.eos_token_id is not None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    model = AutoModelForCausalLM.from_pretrained(model_dir, dtype=selected_dtype).to(device)
    if hasattr(model, "generation_config"):
        generation_config = model.generation_config
        generation_config.do_sample = False
        if tokenizer.pad_token_id is not None:
            generation_config.pad_token_id = tokenizer.pad_token_id
        for attribute in ("temperature", "top_p", "top_k"):
            if hasattr(generation_config, attribute):
                setattr(generation_config, attribute, None)
    model.eval()
    return ModelBundle(model=model, tokenizer=tokenizer, device=device, dtype=selected_dtype)


def tokenize_prompt(bundle: ModelBundle, prompt: str) -> dict[str, torch.Tensor]:
    encoded = bundle.tokenizer(prompt, return_tensors="pt")
    return {key: value.to(bundle.device) for key, value in encoded.items()}


def target_token_id(bundle: ModelBundle, target: str) -> int:
    tokens = bundle.tokenizer(" " + target, add_special_tokens=False).input_ids
    if not tokens:
        tokens = bundle.tokenizer(target, add_special_tokens=False).input_ids
    if not tokens:
        raise ValueError(f"Unable to tokenize target {target!r}")
    return int(tokens[0])


def subject_span(bundle: ModelBundle, prompt: str, subject: str) -> tuple[int, int]:
    marker = prompt.rfind(subject)
    if marker == -1:
        return (-1, -1)
    prefix = prompt[:marker]
    upto_subject = prompt[: marker + len(subject)]
    start = len(bundle.tokenizer(prefix, add_special_tokens=False).input_ids)
    end = len(bundle.tokenizer(upto_subject, add_special_tokens=False).input_ids)
    return (start, max(start, end - 1))


def run_forward(bundle: ModelBundle, prompt: str, output_hidden_states: bool = True) -> Any:
    inputs = tokenize_prompt(bundle, prompt)
    with torch.no_grad():
        return bundle.model(**inputs, output_hidden_states=output_hidden_states)
