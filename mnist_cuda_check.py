import argparse
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms


class SimpleMNISTNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.model = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28 * 28, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 10),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple MNIST CUDA check with PyTorch")
    parser.add_argument("--data-dir", default="data", help="Directory to store MNIST data")
    parser.add_argument("--epochs", type=int, default=1, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=256, help="Training batch size")
    parser.add_argument(
        "--require-cuda",
        action="store_true",
        help="Exit with an error if CUDA is not available",
    )
    parser.add_argument(
        "--train-samples",
        type=int,
        default=10000,
        help="Number of training samples to use for a quick smoke test",
    )
    parser.add_argument(
        "--test-samples",
        type=int,
        default=2000,
        help="Number of test samples to use for evaluation",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=2,
        help="Number of DataLoader worker processes",
    )
    return parser.parse_args()


def build_dataloaders(
    data_dir: Path,
    batch_size: int,
    train_samples: int,
    test_samples: int,
    num_workers: int,
) -> tuple[DataLoader, DataLoader]:
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,)),
        ]
    )

    train_dataset = datasets.MNIST(root=data_dir, train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST(root=data_dir, train=False, download=True, transform=transform)

    train_subset = Subset(train_dataset, range(min(train_samples, len(train_dataset))))
    test_subset = Subset(test_dataset, range(min(test_samples, len(test_dataset))))

    pin_memory = torch.cuda.is_available()
    train_loader = DataLoader(
        train_subset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )
    test_loader = DataLoader(
        test_subset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )
    return train_loader, test_loader


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: torch.device,
) -> float:
    model.train()
    running_loss = 0.0

    for images, labels in loader:
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        optimizer.zero_grad(set_to_none=True)
        logits = model(images)
        loss = criterion(logits, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)

    return running_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model: nn.Module, loader: DataLoader, device: torch.device) -> float:
    model.eval()
    correct = 0
    total = 0

    for images, labels in loader:
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)
        logits = model(images)
        predictions = torch.argmax(logits, dim=1)
        correct += (predictions == labels).sum().item()
        total += labels.size(0)

    return correct / total


def main() -> None:
    args = parse_args()

    cuda_available = torch.cuda.is_available()
    if args.require_cuda and not cuda_available:
        raise SystemExit("CUDA is not available in this environment.")

    device = torch.device("cuda" if cuda_available else "cpu")

    print(f"Torch version: {torch.__version__}")
    print(f"CUDA available: {cuda_available}")
    if cuda_available:
        print(f"CUDA device count: {torch.cuda.device_count()}")
        print(f"Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("Falling back to CPU.")

    train_loader, test_loader = build_dataloaders(
        data_dir=Path(args.data_dir),
        batch_size=args.batch_size,
        train_samples=args.train_samples,
        test_samples=args.test_samples,
        num_workers=args.num_workers,
    )

    model = SimpleMNISTNet().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    print(f"Model device: {next(model.parameters()).device}")
    for epoch in range(1, args.epochs + 1):
        loss = train_one_epoch(model, train_loader, optimizer, criterion, device)
        accuracy = evaluate(model, test_loader, device)
        print(f"Epoch {epoch}: loss={loss:.4f}, accuracy={accuracy * 100:.2f}%")

    if cuda_available:
        torch.cuda.synchronize()
        peak_memory_mb = torch.cuda.max_memory_allocated() / (1024 ** 2)
        print(f"Peak CUDA memory allocated: {peak_memory_mb:.2f} MB")


if __name__ == "__main__":
    main()
