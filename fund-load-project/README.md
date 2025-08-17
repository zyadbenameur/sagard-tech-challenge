# Fund Load Project
##  Overview

This project processes financial transactions (loading funds) by validating them according to business rules, storing them in Redis, and writing the valid transactions into a simplified blockchain.

---
## Assumptions

This project was developed under the following assumptions to simplify development and align with known constraints:

1. **Prime Number Generation Scope**  
   Prime numbers are generated up to **1,000,000**, based on the observation that the maximum transaction ID in the input data set is **31,986**. We assume this margin is adequate for the scope of the project.

2. **Special Currency Format Handling**  
   The transaction ID `"27963"` appears with the `load_amount` formatted as `"USD$431.04"`. it is currently accepted as a valid format for parsing, but *no* currency conversion logic is implemented—it's treated the same as other amounts, regardless of the `USD$` prefix.


##  Project Structure
  
fund-load-project/  
├── inputs/ # Raw input files  
│ └── input.txt  
│  
├── outputs/ # Generated outputs (JSON, txt, blockchain)  
│ ├── blockchain.json  
│ ├── output_with_detail.jsonl  
│ └── output.txt  
│  
├── src/ # Main application code  
│ ├── _constants.py  
│ ├── _utils.py  
│ ├── blockchain.py  
│ ├── redis_storage.py  
│ ├── transactions.py  
│ ├── validator.py  
│ └── main.py  
│  
├── tests/ # Pytest test modules  
│ ├── conftest.py  
│ ├── test_redis_storage.py  
│ ├── test_transaction.py  
│ └── test_validator.py  
│  
├── pyproject.toml # Dependencies & project metadata  
└── README.md # Project overview and usage  


## Installation & Setup

###  Recommended: GitHub Codespaces (Fully Preconfigured)

This project is developed and tested within GitHub Codespaces using a predefined `devcontainer.json`.  
Everything—from Python 3.11 to Redis—is installed and is running by the time your Codespace is created. You just need to click and go.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/zyadbenameur/sagard-tech-challenge)

When you open a Codespace:
- **All dependencies are pre-installed**
- **Redis service is started via `docker-compose`**
- **The development environment is ready immediately**


##  Usage

```bash
cd fund-load-project
python -m src.main
```

or manually execute `main.py` via the codespace UI.


##  Features
- Validation: Checks based on customer IDs and load amounts, including prime-ID specific rules and Mondays special regulation.

- Persistence: Transaction storage uses Redis time-series.

- Blockchain: Appends validated transactions to a simple JSON-based blockchain.

- Test coverage: Unit tests using pytest, with fixtures for Redis dependencies.
