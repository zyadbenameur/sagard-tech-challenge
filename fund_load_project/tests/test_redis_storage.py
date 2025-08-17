from ..src.transactions import Transaction
from ..src.redis_storage import RedisTimeSeriesStorage


def test__redis_connection(redis_storage: RedisTimeSeriesStorage) -> None:
    assert isinstance(redis_storage, RedisTimeSeriesStorage)


def test_clear_all_transactions(redis_storage: RedisTimeSeriesStorage) -> None:
    redis_storage.clear_all_transactions()

    # `.keys('*')` returns all keys; database should now be empty
    assert redis_storage.redis.keys("*") == []  # type: ignore


def test__store_and_get_transaction(
    redis_storage: RedisTimeSeriesStorage,
) -> None:

    redis_storage.clear_all_transactions()

    # sample transaction
    transaction = Transaction(
        {
            "id": "15887",
            "customer_id": "528",
            "load_amount": "$3318.47",
            "time": "2000-01-01T00:00:00Z",
        }
    )

    # Store a sample transaction
    redis_storage.store_customer_transaction(transaction)

    # Retrieve transactions for the customer within a wide time range
    min_time = int(transaction.transaction_timetamp)
    max_time = int(transaction.transaction_timetamp)

    retrieved_transaction = redis_storage.get_customer_transactions(
        transaction.customer_id, min_time, max_time
    )

    assert len(retrieved_transaction) == 1

    # Check that the stored transaction is in the retrieved list
    assert [tx["id"] == transaction.transaction_id for tx in retrieved_transaction]  # type: ignore

    # Clean up after test
    redis_storage.clear_all_transactions()


def test__get_transaction__date_out_of_range(
    redis_storage: RedisTimeSeriesStorage,
) -> None:

    redis_storage.clear_all_transactions()

    # sample transaction
    transaction = Transaction(
        {
            "id": "15887",
            "customer_id": "528",
            "load_amount": "$3318.47",
            "time": "2000-01-01T00:00:00Z",
        }
    )

    # Store a sample transaction
    redis_storage.store_customer_transaction(transaction)

    # Retrieve transactions for the customer within a wide time range
    min_time = int(transaction.transaction_timetamp) - 10
    max_time = int(transaction.transaction_timetamp) - 1

    retrieved_transaction = redis_storage.get_customer_transactions(
        transaction.customer_id, min_time, max_time
    )

    assert len(retrieved_transaction) == 0

    # Clean up after test
    redis_storage.clear_all_transactions()
