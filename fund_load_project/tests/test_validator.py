from ..src.transactions import Transaction
from ..src.redis_storage import RedisTimeSeriesStorage
from ..src.validator import TransactionValidator


def test__is_id_prime():
    """Test the _is_prime helper function."""
    storage = RedisTimeSeriesStorage()
    storage.clear_all_transactions()
    validator = TransactionValidator(storage)

    assert validator._is_prime(4) is False  # type: ignore
    assert validator._is_prime(100) is False  # type: ignore
    assert validator._is_prime(10000) is False  # type: ignore
    assert validator._is_prime(1530) is False  # type: ignore
    assert validator._is_prime(6500) is False  # type: ignore

    assert validator._is_prime(2) is True  # type: ignore
    assert validator._is_prime(3) is True  # type: ignore
    assert validator._is_prime(97) is True  # type: ignore
    assert validator._is_prime(4133) is True  # type: ignore
    assert validator._is_prime(7219) is True  # type: ignore
    assert validator._is_prime(16631) is True  # type: ignore
    assert validator._is_prime(25703) is True  # type: ignore


def test__is_monday():
    """Test the _is_monday helper function."""
    from datetime import date

    storage = RedisTimeSeriesStorage()
    storage.clear_all_transactions()

    validator = TransactionValidator(storage)

    assert validator._is_monday(date(2024, 6, 3)) is True  # Monday # type: ignore
    assert validator._is_monday(date(2024, 6, 4)) is False  # Tuesday # type: ignore
    assert validator._is_monday(date(2024, 6, 5)) is False  # Wednesday # type: ignore
    assert validator._is_monday(date(2024, 6, 6)) is False  # Thursday # type: ignore
    assert validator._is_monday(date(2024, 6, 7)) is False  # Friday # type: ignore
    assert validator._is_monday(date(2024, 6, 8)) is False  # Saturday # type: ignore
    assert validator._is_monday(date(2024, 6, 9)) is False  # Sunday # type: ignore

    assert validator._is_monday(date(2025, 8, 18)) is True  # Monday # type: ignore


def test__get_daily_transactions():

    storage = RedisTimeSeriesStorage()
    storage.clear_all_transactions()

    validator = TransactionValidator(storage)

    # Create sample transactions
    historical_transactions_data = [
        {
            "id": "1",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2000-01-01T00:00:00Z",
        },
        {
            "id": "2",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2000-01-01T10:00:00Z",
        },
        {
            "id": "3",
            "customer_id": "2",
            "load_amount": "$100.00",
            "time": "2000-01-01T00:00:00Z",
        },
    ]

    new_transaction_data = {
        "id": "4",
        "customer_id": "1",
        "load_amount": "$100.00",
        "time": "2000-01-01T11:00:00Z",
    }

    transactions = [Transaction(data) for data in historical_transactions_data]

    # Store historical transactions
    for tx in transactions:
        storage.store_customer_transaction(tx)

    # Store new transaction
    new_transaction = Transaction(new_transaction_data)
    storage.store_customer_transaction(new_transaction)

    daily_transactions = validator._get_daily_transactions(new_transaction)  # type: ignore

    assert len(daily_transactions) == 3

    storage.clear_all_transactions()


def test__get_weekly_transactions():

    storage = RedisTimeSeriesStorage()
    storage.clear_all_transactions()

    validator = TransactionValidator(storage)

    # Create sample transactions
    historical_transactions_data = [
        {
            "id": "1",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2000-01-01T00:00:00Z",
        },
        {
            "id": "2",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2000-01-02T10:00:00Z",
        },
        {
            "id": "3",
            "customer_id": "2",
            "load_amount": "$100.00",
            "time": "2000-01-01T00:00:00Z",
        },
        {
            "id": "4",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2000-01-06T00:00:00Z",
        },
    ]

    new_transaction_data = {
        "id": "5",
        "customer_id": "1",
        "load_amount": "$100.00",
        "time": "2000-01-06T11:00:00Z",
    }

    transactions = [Transaction(data) for data in historical_transactions_data]

    # Store historical transactions
    for tx in transactions:
        storage.store_customer_transaction(tx)

    # Store new transaction
    new_transaction = Transaction(new_transaction_data)
    storage.store_customer_transaction(new_transaction)

    weekly_transactions = validator._get_weekly_transactions(new_transaction)  # type: ignore

    assert len(weekly_transactions) == 4

    storage.clear_all_transactions()


def test__get_daily_transaction_count():

    storage = RedisTimeSeriesStorage()
    storage.clear_all_transactions()

    validator = TransactionValidator(storage)

    # Create sample transactions
    historical_transactions_data = [
        {
            "id": "1",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2000-01-01T00:00:00Z",
        },
        {
            "id": "2",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2000-01-01T10:00:00Z",
        },
        {
            "id": "3",
            "customer_id": "2",
            "load_amount": "$100.00",
            "time": "2000-01-01T00:00:00Z",
        },
    ]

    new_transaction_data = {
        "id": "4",
        "customer_id": "1",
        "load_amount": "$100.00",
        "time": "2000-01-01T11:00:00Z",
    }

    transactions = [Transaction(data) for data in historical_transactions_data]

    # Store historical transactions
    for tx in transactions:
        storage.store_customer_transaction(tx)

    # Store new transaction
    new_transaction = Transaction(new_transaction_data)
    storage.store_customer_transaction(new_transaction)

    daily_transactions = validator._get_daily_transactions(new_transaction)  # type: ignore
    transaction_count = validator._transaction_count(daily_transactions)  # type: ignore

    assert transaction_count == 3

    storage.clear_all_transactions()


def test__daily_total_load_amount__no_mondays():

    storage = RedisTimeSeriesStorage()
    storage.clear_all_transactions()

    validator = TransactionValidator(storage)

    # Create sample transactions
    historical_transactions_data = [
        {
            "id": "1",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2025-08-15T00:00:00Z",
        },
        {
            "id": "2",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2025-08-16T00:00:00Z",
        },
        {
            "id": "3",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2025-08-16T10:00:00Z",
        },
        {
            "id": "4",
            "customer_id": "2",
            "load_amount": "$100.00",
            "time": "2025-08-16T00:00:00Z",
        },
    ]

    new_transaction_data = {
        "id": "5",
        "customer_id": "1",
        "load_amount": "$100.00",
        "time": "2025-08-16T11:00:00Z",
    }

    transactions = [Transaction(data) for data in historical_transactions_data]

    # Store historical transactions
    for tx in transactions:
        storage.store_customer_transaction(tx)

    # Store new transaction
    new_transaction = Transaction(new_transaction_data)
    storage.store_customer_transaction(new_transaction)

    daily_transactions = validator._get_daily_transactions(new_transaction)  # type: ignore
    daily_total = validator._total_load_amount(daily_transactions)  # type: ignore

    assert daily_total == 300

    storage.clear_all_transactions()


def test__daily_total_load_amount__with_mondays():

    storage = RedisTimeSeriesStorage()
    storage.clear_all_transactions()

    validator = TransactionValidator(storage)

    # Create sample transactions
    historical_transactions_data = [
        {
            "id": "1",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2025-08-16T00:00:00Z",
        },
        {
            "id": "2",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2025-08-18T00:00:00Z",
        },
        {
            "id": "3",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2025-08-18T10:00:00Z",
        },
        {
            "id": "4",
            "customer_id": "2",
            "load_amount": "$100.00",
            "time": "2025-08-18T00:00:00Z",
        },
    ]

    new_transaction_data = {
        "id": "5",
        "customer_id": "1",
        "load_amount": "$100.00",
        "time": "2025-08-18T11:00:00Z",
    }

    transactions = [Transaction(data) for data in historical_transactions_data]

    # Store historical transactions
    for tx in transactions:
        storage.store_customer_transaction(tx)

    # Store new transaction
    new_transaction = Transaction(new_transaction_data)
    storage.store_customer_transaction(new_transaction)

    daily_transactions = validator._get_daily_transactions(new_transaction)  # type: ignore
    daily_total = validator._total_load_amount(daily_transactions)  # type: ignore

    assert daily_total == 600

    storage.clear_all_transactions()


def test__weekly_total_load_amount__no_mondays():

    storage = RedisTimeSeriesStorage()
    storage.clear_all_transactions()

    validator = TransactionValidator(storage)

    # Create sample transactions
    historical_transactions_data = [
        {
            "id": "1",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2025-08-10T00:00:00Z",
        },
        {
            "id": "2",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2025-08-12T00:00:00Z",
        },
        {
            "id": "3",
            "customer_id": "2",
            "load_amount": "$100.00",
            "time": "2025-08-16T00:00:00Z",
        },
        {
            "id": "4",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2025-08-15T00:00:00Z",
        },
    ]

    new_transaction_data = {
        "id": "5",
        "customer_id": "1",
        "load_amount": "$100.00",
        "time": "2025-08-16T00:00:00Z",
    }

    transactions = [Transaction(data) for data in historical_transactions_data]

    # Store historical transactions
    for tx in transactions:
        storage.store_customer_transaction(tx)

    # Store new transaction
    new_transaction = Transaction(new_transaction_data)
    storage.store_customer_transaction(new_transaction)

    weekly_transactions = validator._get_weekly_transactions(new_transaction)  # type: ignore
    weekly_total = validator._total_load_amount(weekly_transactions)  # type: ignore

    assert weekly_total == 400

    storage.clear_all_transactions()


def test__weekly_total_load_amount__with_mondays():

    storage = RedisTimeSeriesStorage()
    storage.clear_all_transactions()

    validator = TransactionValidator(storage)

    # Create sample transactions
    historical_transactions_data = [
        {
            "id": "1",
            "customer_id": "1",
            "load_amount": "$100.00",  # Amount is doubled on Mondays
            "time": "2025-08-11T00:00:00Z",  # Monday
        },
        {
            "id": "2",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2025-08-12T00:00:00Z",
        },
        {
            "id": "3",
            "customer_id": "2",
            "load_amount": "$100.00",
            "time": "2025-08-16T00:00:00Z",
        },
        {
            "id": "4",
            "customer_id": "1",
            "load_amount": "$100.00",
            "time": "2025-08-15T00:00:00Z",
        },
    ]

    new_transaction_data = {
        "id": "5",
        "customer_id": "1",
        "load_amount": "$100.00",
        "time": "2025-08-16T00:00:00Z",
    }

    transactions = [Transaction(data) for data in historical_transactions_data]

    # Store historical transactions
    for tx in transactions:
        storage.store_customer_transaction(tx)

    # Store new transaction
    new_transaction = Transaction(new_transaction_data)
    storage.store_customer_transaction(new_transaction)

    weekly_transactions = validator._get_weekly_transactions(new_transaction)  # type: ignore
    weekly_total = validator._total_load_amount(weekly_transactions)  # type: ignore

    assert weekly_total == 500

    storage.clear_all_transactions()
