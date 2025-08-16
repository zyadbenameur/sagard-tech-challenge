from src.blockchain.blockchain import Blockchain

def test__accept_valied_transaction():
    blockchain = Blockchain()
    tx = {"id": "1001", "customer_id": "1", "load_amount": "$100.00", "time": "2024-07-29T00:00:00Z"}
    assert blockchain.add_transaction(tx) is True

def test__reject_transaction_over_daily_limit():
    blockchain = Blockchain()
    tx1 = {"id": "1002", "customer_id": "1", "load_amount": "$4000.00", "time": "2024-07-29T00:00:00Z"}
    tx2 = {"id": "1003", "customer_id": "1", "load_amount": "$2000.00", "time": "2024-07-29T00:00:00Z"}
    blockchain.add_transaction(tx1)
    assert blockchain.add_transaction(tx2) is False

def test__reject_transaction_over_weekly_limit():
    blockchain = Blockchain()
    tx1 = {"id": "1004", "customer_id": "1", "load_amount": "$15000.00", "time": "2024-07-29T00:00:00Z"}
    tx2 = {"id": "1005", "customer_id": "1", "load_amount": "$6000.00", "time": "2024-07-30T00:00:00Z"}
    blockchain.add_transaction(tx1)
    assert blockchain.add_transaction(tx2) is False

def test__reject_transaction_over_daily_count_limit():
    blockchain = Blockchain()
    tx1 = {"id": "1006", "customer_id": "1", "load_amount": "$1000.00", "time": "2024-07-29T00:00:00Z"}
    tx2 = {"id": "1007", "customer_id": "1", "load_amount": "$2000.00", "time": "2024-07-29T00:00:00Z"}
    tx3 = {"id": "1008", "customer_id": "1", "load_amount": "$3000.00", "time": "2024-07-29T00:00:00Z"}
    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)
    assert blockchain.add_transaction(tx3) is False

def test__accept_prime_transaction():
    blockchain = Blockchain()
    tx1 = {"id": "1009", "customer_id": "1", "load_amount": "$5000.00", "time": "2024-07-29T00:00:00Z"}
    tx2 = {"id": "1010", "customer_id": "1", "load_amount": "$4000.00", "time": "2024-07-30T00:00:00Z"}
    assert blockchain.add_transaction(tx1) is True
    assert blockchain.add_transaction(tx2) is False  # Daily limit for prime ID exceeded

def test__reject_prime_transaction_over_daily_limit():
    blockchain = Blockchain()
    tx1 = {"id": "1011", "customer_id": "1", "load_amount": "$9999.00", "time": "2024-07-29T00:00:00Z"}
    tx2 = {"id": "1012", "customer_id": "1", "load_amount": "$1000.00", "time": "2024-07-30T00:00:00Z"}
    assert blockchain.add_transaction(tx1) is True
    assert blockchain.add_transaction(tx2) is False  # Daily limit for prime ID exceeded


def test__double_amount_on_monday():
    blockchain = Blockchain()
    tx1 = {"id": "1013", "customer_id": "1", "load_amount": "$100.00", "time": "2024-07-29T00:00:00Z"}  # Monday
    tx2 = {"id": "1014", "customer_id": "1", "load_amount": "$200.00", "time": "2024-07-30T00:00:00Z"}  # Tuesday
    assert blockchain.add_transaction(tx1) is True
    assert blockchain.add_transaction(tx2) is True
