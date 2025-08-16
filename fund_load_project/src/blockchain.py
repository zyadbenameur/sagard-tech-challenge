from datetime import datetime, timedelta
import json
import os
from typing import List, Optional
from abc import ABC, abstractmethod
from src.transactions.transactions import Transaction
from fund_load_project.src.validator import TransactionValidator


class Block:
    def __init__(self, index, previous_hash, timestamp, transactions):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
        }

    @classmethod
    def from_dict(cls, data: dict):
        transactions = [Transaction.from_dict(tx) for tx in data["transactions"]]
        return cls(
            index=data["index"],
            previous_hash=data["previous_hash"],
            timestamp=data["timestamp"],
            transactions=transactions,
        )


class BaseBlockchain(ABC):
    def __init__(
        self,
        storage_path: str,
        batch_size: int = 100,
        batch_interval: timedelta = timedelta(hours=1),
    ):
        self.storage_path = storage_path
        self.batch_size = batch_size
        self.batch_interval = batch_interval
        self.chain = self._load_chain()
        self.current_transactions = []
        self.last_block_time = datetime.now()

        if not self.chain:
            self.create_block(previous_hash="1", timestamp=0)

    def _load_chain(self) -> List[Block]:
        """Load blockchain from storage"""
        if not os.path.exists(self.storage_path):
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            return []

        try:
            with open(self.storage_path, "r") as f:
                chain_data = json.load(f)
                return [Block.from_dict(block_data) for block_data in chain_data]
        except FileNotFoundError:
            return []

    def _save_chain(self):
        """Save blockchain to storage"""
        chain_data = [block.to_dict() for block in self.chain]
        with open(self.storage_path, "w") as f:
            json.dump(chain_data, f, indent=2)

    def create_block(self, previous_hash, timestamp) -> Optional[Block]:
        if not self.current_transactions:
            return None

        block = Block(
            index=len(self.chain) + 1,
            previous_hash=previous_hash,
            timestamp=timestamp,
            transactions=self.current_transactions,
        )
        self.current_transactions = []
        self.chain.append(block)
        self._save_chain()
        self.last_block_time = datetime.now()
        return block

    def should_create_block(self) -> bool:
        """Determine if a new block should be created based on conditions"""
        time_condition = datetime.now() - self.last_block_time >= self.batch_interval
        size_condition = len(self.current_transactions) >= self.batch_size
        return time_condition or size_condition

    def get_chain(self):
        return [block.to_dict() for block in self.chain]

    @abstractmethod
    def add_transaction(self, transaction_dict):
        pass


class ValidatedBlockchain(BaseBlockchain):
    def __init__(
        self,
        validator: TransactionValidator,
        storage_path: str,
        batch_size: int = 100,
        batch_interval: timedelta = timedelta(hours=1),
    ):
        super().__init__(storage_path, batch_size, batch_interval)
        self.validator = validator

    def add_transaction(self, transaction_dict):
        transaction = Transaction(
            transaction_id=transaction_dict["id"],
            customer_id=transaction_dict["customer_id"],
            transaction_date=transaction_dict["time"][:10],
            transaction_time=transaction_dict["time"][11:],
            transaction_datetime=transaction_dict["time"],
            load_amount=float(
                transaction_dict["load_amount"].replace("$", "").replace(",", "")
            ),
        )

        if not self.validator.validate_transaction(
            transaction, self.chain, self.current_transactions
        ):
            return False

        self.current_transactions.append(transaction)

        if self.should_create_block():
            previous_hash = self.chain[-1].previous_hash if self.chain else "1"
            timestamp = int(datetime.now().timestamp())
            self.create_block(previous_hash=previous_hash, timestamp=timestamp)

        return True


@classmethod
def create_default(
    cls,
    storage_path: str,
    batch_size: int = 100,
    batch_interval: timedelta = timedelta(hours=1),
    prime_limit: int = 1_000_000,
) -> "ValidatedBlockchain":
    """Create a blockchain with default configuration."""
    validator = TransactionValidator(prime_limit=prime_limit)
    return cls(
        validator=validator,
        storage_path=storage_path,
        batch_size=batch_size,
        batch_interval=batch_interval,
    )
