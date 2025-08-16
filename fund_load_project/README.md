# Python Blockchain for Financial Transactions

This project implements a simple blockchain for managing financial transaction records. It is designed to demonstrate the basic principles of blockchain technology and how it can be applied to financial transactions.

## Project Structure

```
python-blockchain
├── src
│   ├── blockchain.py       # Contains the Blockchain class
│   ├── transaction.py      # Contains the Transaction class
│   └── utils.py            # Contains utility functions
├── tests
│   └── test_blockchain.py  # Unit tests for the Blockchain class
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Installation

To get started with this project, you need to have Python installed on your machine. You can then install the required dependencies using pip. 

1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-blockchain
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To use the blockchain, you can create instances of the `Blockchain` and `Transaction` classes from the `src` directory. Here’s a brief overview of how to create a transaction and add it to the blockchain:

1. Import the necessary classes:
   ```python
   from src.blockchain import Blockchain
   from src.transaction import Transaction
   ```

2. Create a blockchain instance:
   ```python
   blockchain = Blockchain()
   ```

3. Create a transaction:
   ```python
   transaction = Transaction(sender="Alice", recipient="Bob", amount=50)
   ```

4. Add the transaction to the blockchain:
   ```python
   blockchain.add_block(transaction)
   ```

5. Check the blockchain:
   ```python
   print(blockchain.get_chain())
   ```

## Running Tests

To ensure that everything is working correctly, you can run the unit tests provided in the `tests` directory. Use the following command:

```
pytest tests/test_blockchain.py
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.