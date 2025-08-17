from datetime import date, datetime, timezone
from functools import cached_property
from typing import Any

from .transactions import Transaction

from .redis_storage import RedisTimeSeriesStorage


def generate_prime_set(maximum: int) -> set[int]:
    from math import sqrt

    primes = [2]

    for num in range(3, maximum, 2):
        _is_prime = True
        square_root = sqrt(num)
        for prime in primes:
            if num % prime == 0:
                _is_prime = False
                break
            if prime > square_root:
                break
        if _is_prime:
            primes.append(num)

    return {x for x in primes}


class Success:
    def __init__(self):
        pass


class Failure:
    def __init__(self, message: str):
        self.message = message


Result = Success | Failure


class TransactionValidator:
    def __init__(self, storage: RedisTimeSeriesStorage, prime_limit: int = 1_000_000):
        self.prime_limit = prime_limit
        self.storage = storage

    @cached_property
    def prime_set(self):
        return generate_prime_set(self.prime_limit)

    def _is_prime(self, n: int) -> bool:
        return n in self.prime_set

    def _is_monday(self, date: date) -> bool:
        # Check if the given date is Monday (0 = Monday, 6 = Sunday)
        return date.weekday() == 0

    def _get_daily_transactions(
        self,
        transaction: Transaction,
    ) -> list[Any]:

        # Convert to datetime at 00:00:00 (midnight)
        start_of_day = datetime.combine(
            transaction.transaction_date, datetime.min.time(), tzinfo=timezone.utc
        )

        # Get Unix timestamp in seconds
        min_transaction_time = int(start_of_day.timestamp())
        max_transaction_time = int(transaction.transaction_timetamp)

        current_days_transactions = self.storage.get_customer_transactions(
            customer_id=transaction.customer_id,
            min_transaction_time=min_transaction_time,
            max_transaction_time=max_transaction_time,
        )

        return current_days_transactions

    def _get_weekly_transactions(
        self,
        transaction: Transaction,
    ) -> list[Any]:

        min_transaction_time = int(transaction.transaction_timetamp - 7 * 24 * 3600)
        max_transaction_time = int(transaction.transaction_timetamp)

        current_days_transactions = self.storage.get_customer_transactions(
            customer_id=transaction.customer_id,
            min_transaction_time=min_transaction_time,
            max_transaction_time=max_transaction_time,
        )

        return current_days_transactions

    def _transaction_count(self, transactions: list[dict[str, Any]]) -> int:
        """Return the number of transactions in a list."""
        return len(transactions)

    def _total_load_amount(self, transactions: list[dict[str, Any]]) -> float:
        """Return the sum of 'load_amount' for all transactions.
        If the transaction date is a Monday, double the amount.
        """
        total = 0.0
        for tx in transactions:

            amount = tx.get("load_amount", 0)

            tx_date_str = tx.get("transaction_date")

            if tx_date_str:
                tx_date = datetime.strptime(tx_date_str, "%Y-%m-%d").date()

                # Double the amount if the transaction date is a Monday
                if self._is_monday(tx_date):
                    amount *= 2

            total += amount

        return total

    def validate_transaction(self, transaction: Transaction) -> Result:
        """Validate transaction against business rules."""

        # validate is prime id
        if self._is_prime(transaction.transaction_id):

            # If custumer ID is prime, apply special rules
            daily_transactions = self._get_daily_transactions(transaction)

            daily_count = self._transaction_count(daily_transactions)
            if daily_count > 1:
                return Failure("Prime ID: more than one daily transaction")

            daily_total = self._total_load_amount(daily_transactions)
            if daily_total > 9_999:
                return Failure("Prime ID: daily total exceeds 9,999")

            return Success()

        else:
            # Normal customer ID, apply standard rules
            daily_transactions = self._get_daily_transactions(transaction)

            daily_count = self._transaction_count(daily_transactions)
            if daily_count > 3:
                return Failure("Normal ID: more than three daily transactions")

            daily_total = self._total_load_amount(daily_transactions)
            if daily_total > 5_000:
                return Failure("Normal ID: daily total exceeds 5,000")

            weekly_transactions = self._get_weekly_transactions(transaction)
            weekly_total = self._total_load_amount(weekly_transactions)
            if weekly_total > 20_000:
                return Failure("Normal ID: weekly total exceeds 20,000")

            return Success()
