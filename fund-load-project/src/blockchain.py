from datetime import datetime
import json
import os
from typing import Any, List, Optional
from abc import ABC
from transactions import Transaction


class Block:
    def __init__(
        self,
        index: int,
        previous_hash: str,
        timestamp: int,  # store timestamp as int (Unix epoch) for serialization
        transactions: List[Transaction],  # should be a list, not single transaction
    ):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Block":
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
        batch_size: int = 1,
    ):
        self.storage_path = storage_path
        self.batch_size = batch_size
        self.chain: List[Block] = self._load_chain()
        self.current_transactions: List[Transaction] = []
        self.last_block_time = datetime.now()

        if not self.chain:
            # Genesis block with timestamp as int Unix epoch
            self.create_block(
                previous_hash="1", timestamp=int(datetime.now().timestamp())
            )

        print(f"Initialized blockchain with {len(self.chain)} blocks.")

    def _load_chain(self) -> List[Block]:
        """Load blockchain from storage"""
        if not os.path.exists(self.storage_path):
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            return []

        try:
            with open(self.storage_path, "r") as f:
                chain_data = json.load(f)
                return [Block.from_dict(block_data) for block_data in chain_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_chain(self):
        """Save blockchain to storage"""
        chain_data = [block.to_dict() for block in self.chain]
        with open(self.storage_path, "w") as f:
            json.dump(chain_data, f, indent=2)

    def create_block(self, previous_hash: str, timestamp: int) -> Optional[Block]:
        if not self.current_transactions:
            return None

        block = Block(
            index=len(self.chain) + 1,
            previous_hash=previous_hash,
            timestamp=timestamp,
            transactions=self.current_transactions.copy(),
        )
        self.current_transactions = []
        self.chain.append(block)
        self.save_chain()
        self.last_block_time = datetime.now()
        return block

    def should_create_block(self) -> bool:
        """Determine if a new block should be created based on conditions"""
        size_condition = len(self.current_transactions) >= self.batch_size
        return size_condition

    def get_chain(self):
        return [block.to_dict() for block in self.chain]

    def add_transaction(self, transaction: Transaction) -> bool:
        # For example, just add transaction without validation
        self.current_transactions.append(transaction)

        if self.should_create_block():
            previous_hash = self.chain[-1].previous_hash if self.chain else "1"
            timestamp = int(datetime.now().timestamp())
            self.create_block(previous_hash=previous_hash, timestamp=timestamp)

        return True
