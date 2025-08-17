import json
from pathlib import Path
from src._constants import INPUT_FILE, OUTPUT_FOLDER
from src._utils import (
    append_validation_result,
    clean_directory,
)
from src.transactions import Transaction
from src.validator import Success, TransactionValidator
from src.redis_storage import RedisTimeSeriesStorage
from src.blockchain import BaseBlockchain


def process_transaction_line(
    line: str,
    storage: RedisTimeSeriesStorage,
    validator: TransactionValidator,
    output_folder: Path,
    blockchain: BaseBlockchain,
) -> None:
    """Parse a line as a transaction, validate it, store result, and append to blockchain if valid."""

    # Parse JSON line to dictionary
    transaction_dict = json.loads(line)

    # Create Transaction object
    transaction = Transaction(transaction_dict)

    # Store transaction in Redis
    storage.store_customer_transaction(transaction)

    # Validate transaction
    result = validator.validate_transaction(transaction)

    # Append to JSONL file with accepted status
    append_validation_result(output_folder, transaction, result)

    # If transaction is valid, add to blockchain
    if isinstance(result, Success):
        blockchain.add_transaction(transaction)


def main() -> None:
    """Main entry point: orchestrates reading, validating, and recording transactions."""

    output_folder = Path(OUTPUT_FOLDER)

    # clean output folder and start fresh
    clean_directory(output_folder)

    storage = RedisTimeSeriesStorage()
    storage.clear_all_transactions()

    validator = TransactionValidator(storage)

    blockchain = BaseBlockchain(
        storage_path=OUTPUT_FOLDER + "blockchain.json",
    )

    print("Starting transaction processing...")

    with open(INPUT_FILE, "r") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            process_transaction_line(
                line, storage, validator, output_folder, blockchain
            )

    print("Finished processing all transactions.")


if __name__ == "__main__":

    main()
