from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


@dataclass
class ValidationState:
    """Represents the latest validation state for a customer"""

    last_transaction_date: str
    daily_total: float
    weekly_total: float
    weekly_reset_date: str
    daily_count: int


class TransactionValidator:
    def __init__(self, prime_limit=1_000_000):
        self.prime_limit = prime_limit

    def _get_latest_validation_state(
        self, chain: list, customer_id: str
    ) -> Optional[ValidationState]:
        """
        Get the latest validation state for a customer from the blockchain.
        Returns None if customer has no transactions.
        """
        # Traverse chain in reverse to find latest transaction
        for block in reversed(chain):
            for tx in reversed(block.transactions):
                if tx.customer_id == customer_id:
                    return ValidationState(
                        last_transaction_date=tx.transaction_date,
                        daily_total=tx.daily_total,
                        weekly_total=tx.weekly_total,
                        daily_count=tx.daily_count,
                    )
        return None

    def validate_transaction(self, transaction, chain, current_transactions):
        """Validate transaction using latest state from blockchain"""
        latest_state = self._get_latest_validation_state(chain, transaction.customer_id)

        if latest_state:
            # If transaction is on the same day as latest transaction
            if transaction.transaction_date == latest_state.last_transaction_date:
                daily_total = latest_state.daily_total
                daily_count = latest_state.daily_count
            else:
                # New day, reset daily counts
                daily_total = 0
                daily_count = 0

            # Check if we're still in the same week
            tx_date = datetime.strptime(transaction.transaction_date, "%Y-%m-%d")
            latest_date = datetime.strptime(
                latest_state.last_transaction_date, "%Y-%m-%d"
            )
            same_week = (
                tx_date.isocalendar()[1] == latest_date.isocalendar()[1]
                and tx_date.year == latest_date.year
            )

            weekly_total = latest_state.weekly_total if same_week else 0
        else:
            # No previous transactions
            daily_total = 0
            weekly_total = 0
            daily_count = 0

        # Add current transaction
        new_daily_total = daily_total + transaction.load_amount
        new_weekly_total = weekly_total + transaction.load_amount
        new_daily_count = daily_count + 1

        # Perform validations
        if self.is_prime(transaction.transaction_id):
            if new_daily_count > 1:
                return False
            if new_daily_total > 9999:
                return False
        else:
            if new_daily_total > 5000:
                return False
            if new_daily_count > 3:
                return False

        if new_weekly_total > 20000:
            return False

        # Store validation results in transaction
        transaction.daily_total = new_daily_total
        transaction.weekly_total = new_weekly_total
        transaction.daily_count = new_daily_count

        return True
