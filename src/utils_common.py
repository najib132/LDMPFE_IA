import random
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def get_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")

    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")

    return torch.device("cpu")


def append_row_to_csv(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        df = pd.read_csv(path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(path, index=False)


def save_image_grid(
    images: torch.Tensor,
    path: Path,
    title: str,
    max_images: int = 8,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    images = images.detach().cpu().clamp(0.0, 1.0)
    n = min(images.shape[0], max_images)

    fig, axes = plt.subplots(1, n, figsize=(2 * n, 2.5))

    if n == 1:
        axes = [axes]

    for i in range(n):
        image = images[i, 0].numpy()
        axes[i].imshow(image, cmap="gray")
        axes[i].axis("off")

    fig.suptitle(title)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close(fig)


def save_metric_curve(
    csv_path: Path,
    columns: List[str],
    output_path: Path,
    title: str,
    xlabel: str = "epoch",
) -> None:
    if not csv_path.exists():
        print(f"Fichier introuvable : {csv_path}")
        return

    df = pd.read_csv(csv_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))

    for column in columns:
        if column in df.columns:
            plt.plot(df[xlabel], df[column], label=column)

    plt.xlabel(xlabel)
    plt.ylabel("valeur")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()