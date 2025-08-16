from datetime import datetime
import re
from ._constants import (
    TRANSACTION_ID_FORMAT,
    CUSTOMER_ID_FORMAT,
    AMOUNT_PATTERN,
    DATETIME_FORMAT,
)


class Transaction:

    def __init__(self, transaction_data: dict[str, str]):
        """
        Initialize Transaction from dictionary data.

        Args:
            transaction_data: Dictionary containing transaction details

        Raises:
            ValueError: If required fields are missing or invalid
        """
        # Validate all fields are present
        self._validate_required_fields(transaction_data)

        # Process transaction ID
        self.transaction_id = int(
            self._validate_transaction_id(str(transaction_data["id"]))
        )

        # Process customer ID
        self.customer_id = self._validate_customer_id(
            str(transaction_data["customer_id"])
        )

        # Process timestamp
        date_part, time_part, full_timestamp = self._process_timestamp_field(
            transaction_data["time"]
        )
        self.transaction_date = date_part
        self.transaction_time = time_part
        self.transaction_datetime = full_timestamp

        # Process amount
        self.load_amount = self._process_amount_field(transaction_data["load_amount"])

        self.transaction_data_dict = self.to_dict()

    @classmethod
    def _validate_required_fields(cls, data: dict[str, str]) -> None:
        """Validate presence of required fields."""

        required_fields = ["id", "customer_id", "time", "load_amount"]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

    @classmethod
    def _validate_transaction_id(cls, transaction_id: str) -> str:
        """Clean and validate transaction ID."""

        if not re.match(TRANSACTION_ID_FORMAT, transaction_id):
            raise ValueError(f"Invalid transaction ID format: {transaction_id}")

        return transaction_id

    @classmethod
    def _validate_customer_id(cls, customer_id: str) -> str:
        """Clean and validate customer ID."""

        if not re.match(CUSTOMER_ID_FORMAT, customer_id):
            raise ValueError(f"Invalid customer ID format: {customer_id}")

        return customer_id

    @classmethod
    def _process_timestamp_field(
        cls, transaction_datetime: str
    ) -> tuple[str, str, str]:
        """Clean and validate timestamp, returns (date, time, full_timestamp)."""

        try:
            datetime.strptime(transaction_datetime, DATETIME_FORMAT)
        except ValueError:
            raise ValueError(f"Invalid timestamp format: {transaction_datetime}")

        transaction_date = transaction_datetime[:10]
        transaction_time = transaction_datetime[11:]

        return (transaction_date, transaction_time, transaction_datetime)

    @classmethod
    def _process_amount_field(cls, transaction_amount: str) -> float:
        """Clean and validate amount."""

        if not re.match(AMOUNT_PATTERN, transaction_amount):
            raise ValueError(f"Invalid amount format: {transaction_amount}")

        clean_transaction_amount = float(transaction_amount.replace("$", ""))

        return clean_transaction_amount

    def to_dict(self) -> dict[str, str | int | float]:
        """Convert transaction to dictionary format."""
        return {
            "id": self.transaction_id,
            "customer_id": self.customer_id,
            "transaction_date": self.transaction_date,
            "transaction_time": self.transaction_time,
            "transaction_datetime": self.transaction_datetime,
            "load_amount": self.load_amount,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """
        Create a Transaction instance from a dictionary with keys:
        'id', 'customer_id', 'transaction_date', 'transaction_time',
        'transaction_datetime', 'load_amount'

        This method reformats the input to match what __init__ expects.
        """
        # Validate required fields in input
        required = [
            "id",
            "customer_id",
            "transaction_datetime",
            "load_amount",
        ]
        for field in required:
            if field not in data:
                raise ValueError(f"Missing required field in from_dict: {field}")

        # Prepare the data in the format expected by __init__
        transformed_data = {
            "id": data["id"],
            "customer_id": data["customer_id"],
            "time": data["transaction_datetime"],
            "load_amount": "$" + str(data["load_amount"]),
        }

        # Now create the instance using __init__
        return cls(transformed_data)
