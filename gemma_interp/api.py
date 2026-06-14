from __future__ import annotations

import json
import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import torch

from .capital_study import analyze_single_capital_prompt
from .modeling import load_model_bundle


class PromptRequest(BaseModel):
    prompt: str
    expected_capital: str | None = None


def create_app(
    model_dir: str = "models/gemma-3-270m-it",
    capital_output_dir: str = "artifacts/results/capital_study",
) -> FastAPI:
    app = FastAPI(title="Gemma Capital Activation API")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    bundle = load_model_bundle(model_dir=model_dir, dtype="auto", require_cuda=False)
    capital_dir = Path(capital_output_dir)
    profiles_path = capital_dir / "capital_prompt_profiles.jsonl"
    summary_path = capital_dir / "summary.json"

    @app.get("/api/architecture")
    def architecture() -> dict:
        config = bundle.model.config
        return {
            "model_name": "gemma-3-270m-it",
            "layers": config.num_hidden_layers,
            "attention_heads": config.num_attention_heads,
            "hidden_size": config.hidden_size,
            "intermediate_size": config.intermediate_size,
            "head_dim": config.head_dim,
            "device": str(bundle.device),
            "dtype": str(bundle.dtype).replace("torch.", ""),
        }

    @app.get("/api/capital-summary")
    def capital_summary() -> dict:
        return json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}

    @app.get("/api/capital-prompts")
    def capital_prompts() -> list[dict]:
        if not profiles_path.exists():
            return []
        rows = []
        with profiles_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    rows.append(json.loads(line))
        return rows

    @app.post("/api/analyze")
    def analyze(request: PromptRequest) -> dict:
        expected = request.expected_capital or ""
        started = time.perf_counter()
        result = analyze_single_capital_prompt(bundle, request.prompt, expected or "Washington, D.C.")
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        result["device"] = str(bundle.device)
        result["dtype"] = str(bundle.dtype).replace("torch.", "")
        result["inference_ms"] = round(elapsed_ms, 2)
        if bundle.device.type == "cuda":
            result["gpu_name"] = torch.cuda.get_device_name(0)
        return result

    if Path("artifacts").exists():
        app.mount("/artifacts", StaticFiles(directory="artifacts"), name="artifacts")
    return app
