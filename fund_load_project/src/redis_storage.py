from redis import Redis
from redis.commands.json.path import Path
from .transactions import Transaction
from typing import Any


class RedisTimeSeriesStorage:
    """Redis-based time series storage for transactions"""

    def __init__(self, host: str = "redis", port: int = 6379):
        self.redis = Redis(host=host, port=port, decode_responses=True)
        print(f"Connected to Redis at {host}:{port}")

    def store_customer_transaction(self, transaction: Transaction):
        """Store transaction in Redis with time-series indexing"""
        # Store transaction data
        transaction_key = f"tx:{transaction.transaction_id}"
        customer_key = f"customer:{transaction.customer_id}"

        # Store full transaction
        self.redis.json().set(transaction_key, Path.root_path(), transaction.to_dict())

        # Add to customer's sorted set by timestamp
        self.redis.zadd(
            customer_key,
            {transaction_key: transaction.transaction_timetamp},
        )

    def get_customer_transactions(
        self, customer_id: str, min_transaction_time: int, max_transaction_time: int
    ) -> list[Any]:
        """Get customer's transactions from the last week."""

        customer_key = f"customer:{customer_id}"

        # Fetch members scored between min timestamp and max timestamp, reversed for latest first
        tx_keys = self.redis.zrevrangebyscore(  # type: ignore
            customer_key,
            min=min_transaction_time,
            max=max_transaction_time,
        )

        transactions: list[Transaction] = []
        for key in tx_keys:  # type: ignore
            tx_data = self.redis.json().get(key)  # type: ignore

            if not isinstance(tx_data, dict):
                raise TypeError(f"Expected JSON object, got: {type(tx_data).__name__}")

            transactions.append(tx_data)  # type: ignore

        return transactions

    def clear_all_transactions(self):
        """Delete all data from Redis"""

        self.redis.flushdb()  # type: ignore

        print("Cleared all transactions and customer data from Redis")
