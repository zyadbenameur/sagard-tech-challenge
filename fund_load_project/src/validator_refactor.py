from datetime import datetime, timedelta
from functools import cached_property
from fund_load_project.src._utils import generate_prime_set


class TransactionValidator:
    def __init__(self, prime_limit=1_000_000):
        self.prime_limit = prime_limit

    @cached_property
    def prime_set(self):
        return generate_prime_set(self.prime_limit)

    def is_prime(self, n):
        return str(n) in self.prime_set

    def _get_daily_total(self, chain, current_transactions, customer_id, date_str):
        total = 0.0
        for block in chain:
            for tx in block.transactions:
                if tx.customer_id == customer_id and tx.transaction_date == date_str:
                    total += tx.load_amount
        for tx in current_transactions:
            if tx.customer_id == customer_id and tx.transaction_date == date_str:
                total += tx.load_amount
        return total

    def _get_weekly_total(self, chain, current_transactions, customer_id, date_str):
        total = 0.0
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        week_start = date_obj - timedelta(days=date_obj.weekday())
        week_end = week_start + timedelta(days=6)

        def in_week(tx_date):
            tx_date_obj = datetime.strptime(tx_date, "%Y-%m-%d")
            return week_start <= tx_date_obj <= week_end

        for block in chain:
            for tx in block.transactions:
                if tx.customer_id == customer_id and in_week(tx.transaction_date):
                    total += tx.load_amount
        for tx in current_transactions:
            if tx.customer_id == customer_id and in_week(tx.transaction_date):
                total += tx.load_amount
        return total

    def _get_daily_load_count(self, chain, current_transactions, customer_id, date_str):
        count = 0
        for block in chain:
            for tx in block.transactions:
                if tx.customer_id == customer_id and tx.transaction_date == date_str:
                    count += 1
        for tx in current_transactions:
            if tx.customer_id == customer_id and tx.transaction_date == date_str:
                count += 1
        return count

    def validate_transaction(self, transaction, chain, current_transactions):
        daily_total = self._get_daily_total(
            chain,
            current_transactions,
            transaction.customer_id,
            transaction.transaction_date,
        )
        weekly_total = self._get_weekly_total(
            chain,
            current_transactions,
            transaction.customer_id,
            transaction.transaction_date,
        )
        daily_count = self._get_daily_load_count(
            chain,
            current_transactions,
            transaction.customer_id,
            transaction.transaction_date,
        )

        if self.is_prime(transaction.transaction_id):
            if daily_count >= 1:
                return False
            if daily_total + transaction.load_amount > 9999:
                return False
        else:
            if daily_total + transaction.load_amount > 5000:
                return False
            if daily_count >= 3:
                return False

        if weekly_total + transaction.load_amount > 20000:
            return False

        return True
