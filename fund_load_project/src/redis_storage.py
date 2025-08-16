from typing import Optional
from redis import Redis
from redis.commands.json.path import Path
from datetime import datetime

from src.transactions import Transaction
from ._constants import DATETIME_FORMAT


class RedisTimeSeriesStorage:
    """Redis-based time series storage for transactions"""

    def __init__(self, host="redis", port=6379):
        self.redis = Redis(host=host, port=port, decode_responses=True)

    def store_transaction(self, transaction: Transaction):
        """Store transaction in Redis with time-series indexing"""
        # Store transaction data
        transaction_key = f"tx:{transaction.transaction_id}"
        customer_key = f"customer:{transaction.customer_id}"
        date_key = f"date:{transaction.transaction_date}"

        # Store full transaction
        self.redis.json().set(transaction_key, Path.root_path(), transaction.to_dict())

        # Add to customer's sorted set by timestamp
        self.redis.zadd(
            customer_key,
            {
                transaction_key: datetime.strptime(
                    transaction.transaction_datetime, DATETIME_FORMAT
                ).timestamp()
            },
        )

        # Add to date index
        self.redis.sadd(date_key, transaction_key)

    def get_customer_latest_transaction(
        self, customer_id: str
    ) -> Optional[Transaction]:
        """Get customer's latest transaction"""
        customer_key = f"customer:{customer_id}"
        # Get latest transaction key using ZREVRANGE
        latest = self.redis.zrevrange(customer_key, 0, 0)
        if not latest:
            return None

        # Get transaction data
        tx_data = self.redis.json().get(latest[0])
        return Transaction.from_dict(tx_data)
