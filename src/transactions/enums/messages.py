from enum import Enum


class TransactionMessages(Enum):
    CREATE_TRANSACTION_SUCCESSFULLY = "Transaction was created successfully"
    SOURCE_AMOUNT_MUST_BE_POSITIVE = "Source amount must be positive"
