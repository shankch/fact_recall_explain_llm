from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass
class PromptMetrics:
    target_rank: int
    target_margin: float
    exact_match: float
    top_prediction: str


def token_rank(logits: torch.Tensor, target_id: int) -> int:
    sorted_ids = torch.argsort(logits, descending=True)
    matches = torch.nonzero(sorted_ids == target_id, as_tuple=False)
    return int(matches[0].item()) + 1 if len(matches) else int(logits.numel())


def target_margin(logits: torch.Tensor, target_id: int, contrast_id: int | None = None) -> float:
    target_logit = logits[target_id].item()
    if contrast_id is None:
        top_two = torch.topk(logits, k=2).values
        best_other = top_two[1].item() if logits.argmax().item() == target_id else top_two[0].item()
    else:
        best_other = logits[contrast_id].item()
    return float(target_logit - best_other)


def greedy_exact_match(bundle, prompt: str, target_text: str, max_new_tokens: int = 8) -> float:
    inputs = bundle.tokenizer(prompt, return_tensors="pt").to(bundle.device)
    output_ids = bundle.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    new_ids = output_ids[0][inputs["input_ids"].shape[1] :]
    generated = bundle.tokenizer.decode(new_ids, skip_special_tokens=True).strip()
    return float(generated.lower().startswith(target_text.lower()))
