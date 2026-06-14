from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
import json
import random
import urllib.request

from .config import DatasetConfig
from .utils import ensure_dir, read_jsonl, write_json, write_jsonl


@dataclass
class FactExample:
    case_id: int
    relation_id: str
    subject: str
    target_true: str
    target_new: str
    canonical_prompt: str
    paraphrase_prompts: list[str]
    neighborhood_prompts: list[str]
    attribute_prompts: list[str]
    generation_prompts: list[str]
    split: str


def download_counterfact(config: DatasetConfig) -> Path:
    output_dir = ensure_dir(config.output_dir)
    raw_path = output_dir / config.raw_file
    if raw_path.exists():
        return raw_path
    with urllib.request.urlopen(config.raw_url) as response:
        payload = json.load(response)
    write_json(raw_path, payload)
    return raw_path


def _clean_prompt_list(values: Iterable[str], limit: int, min_prompt_words: int) -> list[str]:
    cleaned: list[str] = []
    for value in values:
        prompt = " ".join(value.split())
        if len(prompt.split()) < min_prompt_words:
            continue
        if prompt not in cleaned:
            cleaned.append(prompt)
        if len(cleaned) >= limit:
            break
    return cleaned


def _assign_split(index: int, total: int, ratios: dict[str, float]) -> str:
    dev_cutoff = int(total * ratios["dev"])
    eval_cutoff = dev_cutoff + int(total * ratios["eval"])
    if index < dev_cutoff:
        return "dev"
    if index < eval_cutoff:
        return "eval"
    return "stress"


def prepare_counterfact(config: DatasetConfig) -> Path:
    raw_path = download_counterfact(config)
    with raw_path.open("r", encoding="utf-8") as handle:
        raw_records = json.load(handle)

    random.Random(config.seed).shuffle(raw_records)
    limited = raw_records[: config.limit]
    prepared: list[FactExample] = []

    for idx, row in enumerate(limited):
        rewrite = row["requested_rewrite"]
        subject = rewrite["subject"]
        canonical_prompt = rewrite["prompt"].format(subject)
        prepared.append(
            FactExample(
                case_id=row["case_id"],
                relation_id=rewrite["relation_id"],
                subject=subject,
                target_true=rewrite["target_true"]["str"],
                target_new=rewrite["target_new"]["str"],
                canonical_prompt=canonical_prompt,
                paraphrase_prompts=_clean_prompt_list(
                    row.get("paraphrase_prompts", []),
                    config.paraphrases_per_fact,
                    config.min_prompt_words,
                ),
                neighborhood_prompts=_clean_prompt_list(
                    row.get("neighborhood_prompts", []),
                    config.neighborhood_controls_per_fact,
                    config.min_prompt_words,
                ),
                attribute_prompts=_clean_prompt_list(
                    row.get("attribute_prompts", []),
                    config.attribute_controls_per_fact,
                    config.min_prompt_words,
                ),
                generation_prompts=_clean_prompt_list(
                    row.get("generation_prompts", []),
                    max(2, config.paraphrases_per_fact),
                    config.min_prompt_words,
                ),
                split=_assign_split(idx, len(limited), config.split_ratios),
            )
        )

    output_dir = ensure_dir(config.output_dir)
    prepared_path = output_dir / config.prepared_file
    write_jsonl(prepared_path, [asdict(item) for item in prepared])
    return prepared_path


def load_prepared_dataset(path: str | Path) -> list[FactExample]:
    return [FactExample(**row) for row in read_jsonl(path)]


def split_examples(examples: list[FactExample]) -> dict[str, list[FactExample]]:
    output: dict[str, list[FactExample]] = {"dev": [], "eval": [], "stress": []}
    for example in examples:
        output.setdefault(example.split, []).append(example)
    return output
