import json
from pathlib import Path
from typing import Any
from .transactions import Transaction
from .validator import Failure, Result, Success


def append_validation_result(
    folder_path: Path, transaction: Transaction, accepted: Result
):
    # Prepare dict in required format
    result: dict[str, Any] = {
        "id": transaction.transaction_id,
        "customer_id": transaction.customer_id,
        "accepted": True if isinstance(accepted, Success) else False,
    }

    filepath = folder_path / "transaction_validation_results.jsonl"

    # Append JSON line to file
    with open(filepath, "a") as f:
        f.write(json.dumps(result) + "\n")

    # Prepare dict for detailed results
    detailed_results: dict[str, Any] = {
        **result,
        "details": (
            accepted.message if isinstance(accepted, Failure) else "Transaction valid"
        ),
    }

    filepath = folder_path / "transaction_detailed_validation_results.jsonl"

    # Append JSON line to file
    with open(filepath, "a") as f:
        f.write(json.dumps(detailed_results) + "\n")


def clean_directory(path: Path) -> None:
    """Utility to clean a directory by removing all files in it."""
    import os
    import shutil

    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)

    print(f"Cleaned and created directory: {path}")
