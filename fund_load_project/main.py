import json
import os
import sys
from src.transactions import Transaction

from src.redis_storage import RedisTimeSeriesStorage

# def process_and_report(blockchain, transaction_dict):
#     accepted = blockchain.add_transaction(transaction_dict)
#     output = {
#         "id": transaction_dict["id"],
#         "customer_id": transaction_dict["customer_id"],
#         "accepted": accepted
#     }
#     print(json.dumps(output))

if __name__ == "__main__":
    # blockchain = Blockchain()
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # input_file = os.path.abspath(os.path.join(script_dir, "../inputs/input.txt"))

    # with open(input_file, "r") as f:
    #     for line in f:
    #         line = line.strip()
    #         if not line:
    #             continue
    #         try:
    #             transaction = json.loads(line)
    #             process_and_report(blockchain, transaction)
    #         except Exception as e:
    #             print(f"Error processing line: {line}\n{e}", file=sys.stderr)

    # # print the blockchain
    # computed_blockchain = blockchain.get_chain()
    # # print("Blockchain state:")
    # # write the chain to a json file
    # output_file = os.path.abspath(os.path.join(script_dir, "../outputs/output.json"))
    # with open(output_file, "w") as f:
    #     json.dump(computed_blockchain, f, indent=4)

    # 1. Instantiate the storage
    storage = RedisTimeSeriesStorage()

    # 2. receive a transaction
    transaction = Transaction(
        {
            "id": "14837",
            "customer_id": "86",
            "load_amount": "$312.33",
            "time": "2000-01-25T05:57:38Z",
        }
    )

    print(transaction)

    # 3. Store the transaction
    storage.store_transaction(transaction)
    print("Transaction stored successfully.")

    # 4. Retrieve the latest transaction for a customer
    latest_tx = storage.get_customer_latest_transaction("86")
    if latest_tx:
        print("Latest transaction found:", latest_tx.to_dict())
    else:
        print("No transactions found for that customer.")
