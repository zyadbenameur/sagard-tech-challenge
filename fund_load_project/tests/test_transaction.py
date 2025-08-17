import re
import pytest
from ..src.transactions import Transaction


def test__valid_transaction():

    # Create a sample valid transaction
    valid_transaction_data = {
        "id": "15887",
        "customer_id": "528",
        "load_amount": "$3318.47",
        "time": "2000-01-01T00:00:00Z",
    }

    transaction = Transaction(valid_transaction_data)

    assert isinstance(transaction, Transaction)


def test__valid_transaction__usd_sign():

    # Create a sample valid transaction
    valid_transaction_data = {
        "id": "15887",
        "customer_id": "528",
        "load_amount": "USD$3318.47",
        "time": "2000-01-01T00:00:00Z",
    }

    transaction = Transaction(valid_transaction_data)

    assert isinstance(transaction, Transaction)


def test__invalid_transaction__missing_id_field():

    # Create a sample valid transaction
    invalid_transaction_data = {
        "customer_id": "528",
        "load_amount": "$3318.47",
        "time": "2000-01-01T00:00:00Z",
    }

    with pytest.raises(ValueError, match="Missing required field: id"):
        Transaction(invalid_transaction_data)


def test__invalid_transaction__missing_customer_id_field():

    # Create a sample valid transaction
    invalid_transaction_data = {
        "id": "15887",
        "load_amount": "$3318.47",
        "time": "2000-01-01T00:00:00Z",
    }

    with pytest.raises(ValueError, match="Missing required field: customer_id"):
        Transaction(invalid_transaction_data)


def test__invalid_transaction__missing_load_amount_field():

    # Create a sample valid transaction
    invalid_transaction_data = {
        "id": "15887",
        "customer_id": "528",
        "time": "2000-01-01T00:00:00Z",
    }

    with pytest.raises(ValueError, match="Missing required field: load_amount"):
        Transaction(invalid_transaction_data)


def test__invalid_transaction__missing_time_field():

    # Create a sample valid transaction
    invalid_transaction_data = {
        "id": "15887",
        "customer_id": "528",
        "load_amount": "$3318.47",
    }

    with pytest.raises(ValueError, match="Missing required field: time"):
        Transaction(invalid_transaction_data)


def test__invalid_transaction__invalid_id_field():

    # Create a sample valid transaction
    invalid_transaction_data = {
        "id": "15887s",  # invalid ID with letter
        "customer_id": "528",
        "load_amount": "$3318.47",
        "time": "2000-01-01T00:00:00Z",
    }

    with pytest.raises(
        ValueError,
        match=f"Invalid transaction ID format: {invalid_transaction_data['id']}",
    ):
        Transaction(invalid_transaction_data)


def test__invalid_transaction__invalid_customer_id_field():

    # Create a sample valid transaction
    invalid_transaction_data = {
        "id": "15887",
        "customer_id": "C528",  # invalid customer ID with letter
        "load_amount": "$3318.47",
        "time": "2000-01-01T00:00:00Z",
    }

    with pytest.raises(
        ValueError,
        match=f"Invalid customer ID format: {invalid_transaction_data['customer_id']}",
    ):
        Transaction(invalid_transaction_data)


def test__invalid_transaction__invalid_load_amount_field__no_dollar_sign():

    # Create a sample valid transaction
    invalid_transaction_data = {
        "id": "15887",
        "customer_id": "528",
        "load_amount": "3318.47",  # missing '$' sign
        "time": "2000-01-01T00:00:00Z",
    }

    with pytest.raises(
        ValueError,
        match=f"Invalid amount format: {invalid_transaction_data['load_amount']}",
    ):
        Transaction(invalid_transaction_data)


def test__invalid_transaction__invalid_load_amount_field__comma():

    # Create a sample valid transaction
    invalid_transaction_data = {
        "id": "15887",
        "customer_id": "528",
        "load_amount": "$3318,47",  # invalid amount with comma instead of dot
        "time": "2000-01-01T00:00:00Z",
    }

    with pytest.raises(
        ValueError,
        match=re.escape(
            rf"Invalid amount format: {invalid_transaction_data['load_amount']}"
        ),
    ):
        Transaction(invalid_transaction_data)


def test__invalid_transaction__invalid_time_field():

    # Create a sample valid transaction
    invalid_transaction_data = {
        "id": "15887",
        "customer_id": "528",
        "load_amount": "$3318.47",
        "time": "2000-01-01T00:00:00",  # missing 'Z' at the end
    }

    with pytest.raises(
        ValueError,
        match=f"Invalid timestamp format: {invalid_transaction_data['time']}",
    ):
        Transaction(invalid_transaction_data)
