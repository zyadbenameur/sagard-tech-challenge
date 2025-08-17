# ^           # Start of string
# \d+         # One or more digits (0-9)
# $           # End of string
TRANSACTION_ID_FORMAT = r"^\d+$"

# ^           # Start of string
# \d+         # One or more digits (0-9)
# $           # End of string
CUSTOMER_ID_FORMAT = r"^\d+$"

# ^               # Start of string
# (USD)?          # Optional "USD" prefix
# \$              # Dollar sign
# \d+             # One or more digits (0-9)
# \d{2}           # Exactly two digits (0-9) as flaoting points for cents
# $               # End of string
AMOUNT_PATTERN = r"^(USD)?\$\d+\.\d{2}$"

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

INPUT_FILE = "fund_load_project/inputs/input.txt"

OUTPUT_FOLDER = "fund_load_project/outputs/"
