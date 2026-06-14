import argparse
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local Gemma model on GPU if available")
    parser.add_argument(
        "--model-dir",
        default="models/gemma-3-270m-it",
        help="Path to the local Hugging Face model directory",
    )
    parser.add_argument(
        "--prompt",
        default="Write a short hello message about running Gemma locally on CUDA.",
        help="Prompt to send to the model",
    )
    parser.add_argument("--max-new-tokens", type=int, default=80, help="Maximum new tokens to generate")
    parser.add_argument(
        "--require-cuda",
        action="store_true",
        help="Exit with an error if CUDA is not available",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model_dir = Path(args.model_dir)

    cuda_available = torch.cuda.is_available()
    if args.require_cuda and not cuda_available:
        raise SystemExit("CUDA is not available in this environment.")

    device = torch.device("cuda" if cuda_available else "cpu")
    dtype = torch.bfloat16 if cuda_available and torch.cuda.is_bf16_supported() else torch.float16
    if not cuda_available:
        dtype = torch.float32

    print(f"Loading model from: {model_dir}")
    print(f"CUDA available: {cuda_available}")
    print(f"Using device: {device}")
    if cuda_available:
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"Using dtype: {dtype}")

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForCausalLM.from_pretrained(model_dir, torch_dtype=dtype).to(device)
    model.eval()

    inputs = tokenizer(args.prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=args.max_new_tokens,
            do_sample=False,
        )

    generated = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    print("\nPrompt:")
    print(args.prompt)
    print("\nResponse:")
    print(generated)

    if cuda_available:
        torch.cuda.synchronize()
        print(f"\nPeak CUDA memory: {torch.cuda.max_memory_allocated() / (1024 ** 2):.2f} MB")


if __name__ == "__main__":
    main()
